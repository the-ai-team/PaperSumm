from io import StringIO
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import tiktoken

# Load the cl100k_base tokenizer which is designed to work with the ada-002 model
tokenizer = tiktoken.encoding_for_model("gpt-3.5-turbo")


def link_parser(url):
    """
    Get the html page from the arxiv link
    """
    id = url.split("/")[-1]
    HTML_url = f"https://ar5iv.labs.arxiv.org/html/{id}"
    return HTML_url


def get_page(url):
    """
    First sends a GET request to the website link using the requests library, 
    and then creates a BeautifulSoup object from the HTML content of the page.
    """
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    return soup


def clean_text(raw_text):
    clean_text = re.sub(r'\[\d+(?:,\s*\d+)*\]', '', raw_text).replace('\n',
                                                                      ' ')  # remove citations and new line characters
    return clean_text


def create_chunks(context, max_tokens=2048):
    """
    create chunks of cintext which is suitable to pass to the model
    """
    sentences = context.split('. ')  # Split the text into sentences
    n_tokens = [len(tokenizer.encode(" " + sentence)) for sentence in
                sentences]  # Get the number of tokens for each sentence

    chunks = []
    tokens_so_far = 0
    chunk = ""

    # Loop through the sentences and tokens joined together in a tuple
    for sentence, token in zip(sentences, n_tokens):

        if tokens_so_far + token < max_tokens:
            chunk += sentence + ". "
            tokens_so_far += token
        else:
            chunks.append(chunk)
            chunk = sentence
            tokens_so_far = token

    return chunks


def extract_context(soup):
    """
    extract and join text wrapped with p tags
    clean text and return in a dataframe as sentences
    """
    p_tags = soup.find_all(
        "p")  # Find all p tags that are not inside table tags
    context = " ".join([p.get_text() for p in p_tags if
                        # Join all the text in p tags & exclude table data
                        not p.find_parents("table")])

    context_cleaned = clean_text(context)  # clean context

    df = pd.DataFrame()
    df['Text'] = create_chunks(context_cleaned)

    return df


def extract_diagrams(soup):
    """
    extract tables, charts and diagrams of the paper and save in a dataframe
    """
    df = pd.DataFrame(columns=['Figure', 'Type', 'Text']
                      )  # Create an empty DataFrame with the desired column names

    # Find all the figure tags in the HTML
    figure_tags = soup.find_all('figure')

    for figure in figure_tags:

        if figure.find('img'):  # get images
            img_src = []
            img_tags = figure.find_all('img')
            [img_src.append('https://ar5iv.labs.arxiv.org' + img_tag['src'])
             for img_tag in img_tags]
            caption = figure.find('figcaption').get_text()

            row = pd.DataFrame({'Figure': [img_src], 'Type': [
                               'img'], 'Text': [caption]}, index=[0])
            df = pd.concat([df, row], ignore_index=True)

        elif figure.find('table'):
            table = []
            table_HTMLs = figure.find_all('table')
            [table.append(pd.read_html(StringIO(str(table_HTML)))[0].to_markdown())
             for table_HTML in table_HTMLs]
            caption = figure.find('figcaption').get_text()

            row = pd.DataFrame({'Figure': [table], 'Type': [
                               'img'], 'Text': [caption]}, index=[0])
            df = pd.concat([df, row], ignore_index=True)

    return df


def Extract(url):
    """
    Main function to extract content
    """
    HTML_url = link_parser(url)
    soup = get_page(HTML_url)

    content_df = extract_context(soup)
    diagrams_df = extract_diagrams(soup)

    return content_df, diagrams_df
