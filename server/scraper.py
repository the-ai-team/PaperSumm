import requests
from bs4 import BeautifulSoup
import re
import pandas as pd


def get_page(url):
    """
    First sends a GET request to the website link using the requests library, 
    and then creates a BeautifulSoup object from the HTML content of the page.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup

def clean_text(raw_text):
    clean_text = re.sub(r'\[\d+(?:,\s*\d+)*\]', '', raw_text).replace('\n',' ') #remove citations and new line characters
    return clean_text

def extract_context(soup):
    """
    extract and join text wrapped with p tags
    clean text and return in a dataframe as sentences
    """
    p_tags = soup.find_all("p") # Find all p tags that are not inside table tags
    context = " ".join([p.get_text() for p in p_tags if not p.find_parents("table")]) # Join all the text in p tags & exclude table data

    context_cleaned = clean_text(context) #clean context

    df = pd.DataFrame()
    df['Text'] = context_cleaned.split('. ')
    
    return df

def extract_diagrams(soup):
    """
    extract tables, charts and diagrams of the paper and save in a dataframe
    """
    df = pd.DataFrame(columns=['Figure', 'Type','Text']) # Create an empty DataFrame with the desired column names

    figure_tags = soup.find_all('figure') # Find all the figure tags in the HTML

    for figure in figure_tags:

        if figure.find('img'): #get images
            img_src= []
            img_tags = figure.find_all('img')
            [img_src.append('https://ar5iv.labs.arxiv.org' + img_tag['src']) for img_tag in img_tags]
            caption = figure.find('figcaption').get_text()

            row = pd.DataFrame({'Figure': [img_src], 'Type': ['img'], 'Text': [caption]}, index=[0])
            df = pd.concat([df, row], ignore_index=True)

        elif figure.find('table'):
            table = []
            table_HTMLs = figure.find_all('table')
            [table.append(pd.read_html(str(table_HTML))[0].to_markdown()) for table_HTML in table_HTMLs]
            caption = figure.find('figcaption').get_text()

            row = pd.DataFrame({'Figure': [table], 'Type': ['img'], 'Text': [caption]}, index=[0])
            df = pd.concat([df, row], ignore_index=True)

    return df


def Extract(url):
    """
    Main function to extract content
    """
    soup = get_page(url)

    content_df = extract_context(soup)
    diagrams_df = extract_diagrams(soup)

    return content_df,diagrams_df




    
