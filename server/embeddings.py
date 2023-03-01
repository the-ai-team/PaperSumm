import tensorflow as tf
from transformers import AutoTokenizer, TFBertModel
import tiktoken

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased") # load tokenizer
model = TFBertModel.from_pretrained("bert-base-uncased") # load model

# Load the cl100k_base tokenizer which is designed to work with the davinci-003 model
tokenizer_davinci = tiktoken.encoding_for_model("text-davinci-003")

def get_embeddings(text):
    """
    Get embeddings of a text sequence
    """
    n_tokens = len(tokenizer_davinci.encode(text)) #no of teokens in the sequence

    tokens = tokenizer.encode(text, add_special_tokens=True, return_tensors='tf') # Tokenize the input text
    outputs = model(tokens) # Pass the tokens through the BERT model
    cls_embedding = outputs.last_hidden_state[:, 0, :] # Extract the last hidden state of the BERT model for the [CLS] token
    return n_tokens, cls_embedding.numpy() # Convert the embedding to a NumPy array and return it

def Embeddings(df,text_column = 'Text'):
    """
    Main function to get embeddings
    """
    df['N_tokens'], df['Embeddings'] = zip(*df[text_column].apply(get_embeddings) )# Apply the function to the text column to create a new embeddings column
    return df
