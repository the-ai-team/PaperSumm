import asyncio
import copy
import json
from random import sample
from core.embeddings import openai
import concurrent.futures
import time

from openai.embeddings_utils import distances_from_embeddings


def get_related_info(keyword, context):
    """
    Extract related information from the context
    """
    response = openai.ChatCompletion.create(  # Create a completions using the keyword and context
        messages=[
            {
                "role": "user",
                "content": f"""
                    Extract information most related to {keyword} of the following context which was taken from a research paper\n
                    context : {context}\n
                    points :
                    """,
            }
        ],
        temperature=0.5,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        model="gpt-3.5-turbo",
    )
    return response["choices"][0]["message"]["content"].strip()


def generate_content_with_stream(
    context, keyword, model="gpt-3.5-turbo", stop_sequence=None
):
    print("Generating content")

    """
    Generate content based on the generated points of the paper
    """
    responses = openai.ChatCompletion.create(  # Create a completions using the keyword and context
        # TODO: remove text limit
        messages=[
            {
                "role": "user",
                "content": f"""
                Organize the following points related to {keyword} of a research by dividing into suitable subtopics. 
                Generate a summarized paragraph for each subtopic.\n\n use this format,\n ## generated subtopic ##\n 
                <Summarized paragraph under the subtopic>\n\n points: {context} 
                organized document:
                 """,
            }
        ],
        temperature=0.5,
        max_tokens=2048,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=stop_sequence,
        model=model,
        stream=True,
    )

    for response in responses:
        data = response["choices"][0]["delta"]
        if "content" in data:
            content = data["content"]
            yield content


class ContentMetadata:
    def __init__(self):
        self.content_dicts = []
        self.content_dict_temp = {}
        self.content_type = {0: "title", 1: "paragraph"}
        self.content_type_selected = 1
        self.content_temp = ""
        self.titles_count = 0
        self.paragraphs_count = 0


def generate_content_dict_stream(content, content_metadata):
    """
    Create a dictionary of generated content by sections

    Chunk format -
    {
        content_type: 'title' OR 'para',
        text: ''
        index: {number}
    }

    Paragaph delimiter (between sections) format -
    {
        content_type: 'delimeter'
    }
    """
    content = content.replace("\n", "")

    output = []

    for string_chunk in content.split(" "):
        if string_chunk == "##":
            # Add block of temporary stored content to the dictionary
            if content_metadata.content_temp != "":
                content_metadata.content_dict_temp[
                    content_metadata.content_type[
                        content_metadata.content_type_selected
                    ]
                ] = content_metadata.content_temp
                if content_metadata.content_type_selected == 1:
                    content_metadata.content_dicts.append(
                        copy.deepcopy(content_metadata.content_dict_temp)
                    )

            # Reset temporary content
            content_metadata.content_temp = ""

            # Toggle content type
            content_metadata.content_type_selected = (
                1 if content_metadata.content_type_selected == 0 else 0
            )

            # Increment counters
            if content_metadata.content_type_selected == 0:
                content_metadata.titles_count += 1
            else:
                content_metadata.paragraphs_count += 1

            continue
        else:
            # output content
            if string_chunk == "":
                content_metadata.content_temp += " "

                output_data = {
                    "content_type": content_metadata.content_type[
                        content_metadata.content_type_selected
                    ],
                    "text": " ",
                    "index": content_metadata.titles_count
                    if content_metadata.content_type_selected == 0
                    else content_metadata.paragraphs_count,
                }
                output.append(output_data)

            else:
                content_metadata.content_temp += string_chunk

                output_data = {
                    "content_type": content_metadata.content_type[
                        content_metadata.content_type_selected
                    ],
                    "text": string_chunk,
                    "index": content_metadata.titles_count
                    if content_metadata.content_type_selected == 0
                    else content_metadata.paragraphs_count,
                }
                output.append(output_data)

    return output


def match_diagrams(diagrams_df, generated_content_dict, threshold=0.15):
    """
    match diagrams for each generated section
    """
    for section in generated_content_dict:
        content_embeddings = openai.Embedding.create(
            input=section["paragraph"], engine="text-embedding-ada-002"
        )["data"][0][
            "embedding"
        ]  # Get Embeddings
        diagrams_df["Distances"] = distances_from_embeddings(
            content_embeddings,
            diagrams_df["Embeddings"].values,
            distance_metric="cosine",
        )  # Get the distances from the embeddings

        diagrams_df = diagrams_df.sort_values(
            "Distances", ascending=True
        )  # sort ascending as distances

        if diagrams_df["Distances"][0] < threshold:
            section["diagrams"] = {
                "type": diagrams_df["Type"][0],
                "figure": diagrams_df["Figure"][0],
                "description": diagrams_df["Text"][0],
            }
            # diagrams_df = diagrams_df.drop(index = 0)

    return generated_content_dict


def Generate(content_df, diagrams_df, keyword):
    """
    Main function for generating
    """
    information = [None] * len(content_df)  # Initialize the list with None values
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {}
        for i, row in content_df.iterrows():
            context = row["Text"]
            keyword = keyword
            futures[
                executor.submit(get_related_info, context, keyword)
            ] = i  # Use a dictionary to associate each future with an index
        for future in concurrent.futures.as_completed(futures):
            i = futures[future]  # Get the index associated with the completed future
            information[
                i
            ] = future.result()  # Add the result to the appropriate index in the list

    related_information = ("\n").join(information)
    # print(related_information)

    generated_content = generate_content_with_stream(related_information, keyword)
    # print(generated_content)

    content_metadata = ContentMetadata()
    for generated_content_chunk in generated_content:
        generated_content_output = generate_content_dict_stream(
            generated_content_chunk, content_metadata
        )
        output = {"type": "content", "content": generated_content_output}
        yield output

    full_output = {
        "type": "full-content",
        "content": match_diagrams(
            diagrams_df, content_metadata.content_dicts
        ),  # match diagrams
    }
    yield full_output
