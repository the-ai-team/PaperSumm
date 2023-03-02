from embeddings import openai
import pandas as pd
from openai.embeddings_utils import distances_from_embeddings


def create_context(
    keywords, df, max_len=1800
):
    """
    Create a context for a keyword by finding the most similar context from the dataframe
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
    model="text-davinci-003",
    max_len=1800,
    debug=False,
    stop_sequence=None
):
    """
    Generate content based on the most similar context from the dataframe texts
    """
    context = create_context(
        keyword,
        df,
        max_len=max_len
    )
    if debug:
        print("Context:\n" + context) # If debug, print the raw model response
        print("\n\n")

    try: 
        response = openai.Completion.create(  # Create a completions using the keyword and context
            prompt=f"""
                    generate a structured document for the following context that extracts the information related on {keyword}.\n Use maximum of 5 subtopics\n.
                    use readable equations and fomulas\n\n
                    context : {context}\n\n
                    use this format\n
                    ## Subtopic ##\n
                    <Summerized paragraph of the subtopic>\n\n
                    structured document in passive voice:
                    """,
            temperature=0,
            max_tokens = 2048,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=stop_sequence,
            model=model,
        )
        return response["choices"][0]["text"].strip()
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

    df = pd.DataFrame({'Title': topics, 'Content': content}) # store the topics and content in a pandas dataframe

    return df

