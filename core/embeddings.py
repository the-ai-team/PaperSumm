from openai import OpenAI
from dotenv import load_dotenv
import os
import tiktoken

load_dotenv()  # Load the environment variables from the .env file

client = OpenAI()
embedding_model = "text-embedding-3-large"  # The model to use for embeddings

# Load the cl100k_base tokenizer which is designed to work with the ada-002 model
tokenizer = tiktoken.get_encoding("cl100k_base")


def Embeddings(df, text_column='Text'):
    """
    Main function to get embeddings
    """
    df['Embeddings'] = df[text_column].apply(lambda x: client.embeddings.create(
        input=[x], model=embedding_model).data[0].embedding)  # get embeddings
    # Tokenize the text and save the number of tokens to a new column
    df['N_tokens'] = df[text_column].apply(lambda x: len(tokenizer.encode(x)))

    return df
