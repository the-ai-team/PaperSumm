from core.scraper import *
from core.embeddings import *
from core.generator import *

def Generate_summary(url,keyword):
    """
    Main fuction
    """
    try:
        content_df,diagrams_df = Extract(url)

        diagrams_df = Embeddings(diagrams_df) #get embeddings

        generated_content_dict = Generate(content_df,diagrams_df,keyword) #Generate content

        return (generated_content_dict)
    except Exception as e:
        Error = [{'Error': str(e) }]
        return Error




