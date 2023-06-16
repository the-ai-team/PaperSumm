from numpy import diag
import openai

from core.scraper import *
from core.embeddings import *
from core.generator import *


def Generate_summary(url, keyword):
    """
    Main fuction
    """
    try:
        # TODO: reenable this
        # content_df, diagrams_df = Extract(url)

        # diagrams_df = Embeddings(diagrams_df)  # Get embeddings
        content_df = "This is a test"
        diagrams_df = "This is a test"

        generated_content = Generate(
            content_df, diagrams_df, keyword
        )  # Generate content

        for chunk in generated_content:
            yield chunk

    except requests.exceptions.HTTPError as e:
        error = {
            "type": "error",
            "content": "Document or Ar5iv article not found. Please verify the document URL and check if the article "
            "is available on Ar5iv in HTML format. Visit https://ar5iv.labs.arxiv.org/ to check "
            "availability. ",
        }
        print(f"Papersumm (HTTP error): {e}")
        yield error

    except openai.error.RateLimitError as e:
        error = {
            "type": "error",
            "content": "We are currently experiencing a high volume of requests. Please try again later.",
        }
        print(f"Papersumm (Open AI Rate limit error): {e}")
        yield error

    except openai.error.ServiceUnavailableError as e:
        error = {
            "type": "error",
            "content": "GPT servers are currently busy. Please try again later.",
        }
        print(f"Papersumm (Open AI Service unavailable error): {e}")
        yield error

    except openai.OpenAIError as e:
        error = {
            "type": "error",
            "content": "Server error. Please try again later.",
        }
        print(f"Papersumm (Open AI other errors): {e}")
        yield error

    except Exception as e:
        error = {
            "type": "error",
            "content": "Something went wrong. Please try again later.",
        }
        print(f"Papersumm (Other errors): {e}")
        yield error


# summary = Generate_summary('https://arxiv.org/abs/1512.03385', 'Experiments and results')
# for i in summary:
#     # print(i)
#     pass
