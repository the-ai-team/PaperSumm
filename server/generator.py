from server.embeddings import openai
from server.embeddings import Embeddings
import pandas as pd
from openai.embeddings_utils import distances_from_embeddings


def match_context(
    keywords, df, max_len=1800
):
    """
    match context for a keyword by finding the most similar context from the dataframe
    """

    k_embeddings = openai.Embedding.create(input=keywords, engine='text-embedding-ada-002')['data'][0]['embedding'] # Get the embeddings for the keyword
    df['Distances'] = distances_from_embeddings(k_embeddings, df['Embeddings'].values, distance_metric='cosine')  # Get the distances from the embeddings

    returns = []
    cur_len = 0

    for i, row in df.sort_values('Distances', ascending=True).iterrows():  # Sort by distance and add the text to the context until the context is too long
        
        cur_len += row['N_tokens'] + 4 # Add the length of the text to the current length
        
        if cur_len > max_len: # If the context is too long, break
            break
        
        returns.append(row["Text"]) # Else add it to the text that is being returned

    return "\n\n###\n\n".join(returns)  # Return the context

def generate_content(
    df,
    keyword,
    model="gpt-3.5-turbo",
    max_len=1800,
    debug=False,
    stop_sequence=None
):
    """
    Generate content based on the most similar context from the dataframe texts
    """
    context = match_context(
        keyword,
        df,
        max_len=max_len
    )
    if debug:
        print("Context:\n" + context) # If debug, print the raw model response
        print("\n\n")

    try: 
        response = openai.ChatCompletion.create(  # Create a completions using the keyword and context
            messages = [{
                "role":"user",
                "content": f"""
                    generate a structured document under generated subtopics for the following context that extracts the information related on {keyword}.\n Use maximum of 5 subtopics\n.
                    use readable notation\n\n
                    context : {context}\n\n
                    use this format\n
                    ## Generated Subtopic ##\n
                    <Generated paragraph of the subtopic>\n\n
                    structured document in passive voice:
                    """
            }],
            temperature=0.5,
            max_tokens = 2048,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=stop_sequence,
            model=model,
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(e)
        return ""


def content_dict(txt):
    """
    Create a dictionary of generated content by sections
    """
    txt = txt.replace('\n','')
    sections = txt.split('##') # split the text into topics and content using the '##' delimiter
    topics = sections[1::2]
    content = sections[2::2]

    dict = [{'Title': topics[i], 'Content': content[i]} for i in range(len(topics))] # Create a list of dictionaries using a list comprehension

    return dict

def match_diagrams(diagrams_df,generated_content_dict,threshold = 0.12):
    """
    match diagrams for each generated section
    """
    for section in generated_content_dict:
        content_embeddings = openai.Embedding.create(input=section['Content'], engine='text-embedding-ada-002')['data'][0]['embedding'] #Get Embeddings
        diagrams_df['Distances'] = distances_from_embeddings(content_embeddings, diagrams_df['Embeddings'].values, distance_metric='cosine')  # Get the distances from the embeddings

        diagrams_df = diagrams_df.sort_values('Distances', ascending=True) # sort ascending as distances
        
        if diagrams_df['Distances'][0] < threshold:
            section['Diagrams'] = {'Type':diagrams_df['Type'][0],'Figure':diagrams_df['Figure'][0],'Description':diagrams_df['Text'][0]}

    return generated_content_dict


def Generate(content_df,diagrams_df,keyword):
    """
    Main function for generating
    """
    generated_content = generate_content(content_df,keyword=keyword) # generate content
    generated_content_dict = content_dict(generated_content) # create dictionary

    generated_content_dict = match_diagrams(diagrams_df,generated_content_dict) # match diagrams

    return generated_content_dict