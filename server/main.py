from server.scraper import *
from server.embeddings import *
from server.generator import *

def Generate_summary(url,keyword):
    """
    Main fuction
    """
    try:
        content_df,diagrams_df = Extract(url)

        diagrams_df = Embeddings(diagrams_df) #get embeddings

        generated_content_dict = Generate(content_df,diagrams_df,keyword) #Generate content

        return (generated_content_dict)
    except Exception:
        Error = [{'Title':'An Unexpected Error Occurred','Content':'This error might be caused by exceeding the Rate Limits of the openAI API. We are looking forward to scaling our tool. So sincerely try another link or try after some time'}]
        return Error




