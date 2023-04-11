import openai
from dotenv import load_dotenv
import os
import tiktoken

load_dotenv() # Load the environment variables from the .env file

openai_api_key = os.getenv('OPEN_AI') # Get the value of the API key
openai.api_key=openai_api_key


tokenizer = tiktoken.get_encoding("cl100k_base") # Load the cl100k_base tokenizer which is designed to work with the davinci-003 model


def Embeddings(df,text_column = 'Text'):
    """
    Main function to get embeddings
    """
    df['Embeddings'] = df[text_column].apply(lambda x: openai.Embedding.create(input=x, engine='text-embedding-ada-002')['data'][0]['embedding']) #get embeddings
    df['N_tokens'] = df[text_column].apply(lambda x: len(tokenizer.encode(x))) # Tokenize the text and save the number of tokens to a new column

    return df
