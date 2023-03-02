from scraper import *
from embeddings import *
from generator import *

def Generate_summary(url,keyword):
    """
    Main fuction
    """
    content_df,diagrams_df = Extract(url)

    diagrams_df = Embeddings(diagrams_df)
    content_df = Embeddings(content_df) #get embeddings

    generated_content_dict = Generate(content_df,diagrams_df,keyword) #Generate content

    return(generated_content_dict)




