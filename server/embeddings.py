import tensorflow as tf
from transformers import AutoTokenizer, TFBertModel

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased") # load tokenizer
model = TFBertModel.from_pretrained("bert-base-uncased") # load model

def get_embeddings(text):
    """
    Get embeddings of a text sequence
    """
    tokens = tokenizer.encode(text, add_special_tokens=True, return_tensors='tf') # Tokenize the input text
    outputs = model(tokens) # Pass the tokens through the BERT model
    cls_embedding = outputs.last_hidden_state[:, 0, :] # Extract the last hidden state of the BERT model for the [CLS] token
    return cls_embedding.numpy() # Convert the embedding to a NumPy array and return it

def Embeddings(df,text_column = 'Text'):
    """
    Main function to get embeddings
    """
    df['Embeddings'] = df[text_column].apply(get_embeddings) # Apply the function to the text column to create a new embeddings column
    return df
