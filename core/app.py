import openai

from core.scraper import *
from core.embeddings import *
from core.generator import *

def Generate_summary(url,keyword):
    """
    Main fuction
    """
    try:
        content_df, diagrams_df = Extract(url)

        diagrams_df = Embeddings(diagrams_df)  # Get embeddings

        generated_content = Generate(content_df, diagrams_df, keyword)  # Generate content

        for output in generated_content:
            print(output)

        return generated_content

    except Exception as e:
        error = {
            "type": "error",
            "content": "Something went wrong. Please try again later."
        }
        print(e)
        return error


summary = Generate_summary('https://arxiv.org/abs/1512.03385', 'Experiments and results')
print(summary)
