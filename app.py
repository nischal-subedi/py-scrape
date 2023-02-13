import os
import requests
import argparse
from bs4 import BeautifulSoup

# Create a command-line argument parser
parser = argparse.ArgumentParser()
parser.add_argument("base_url", help="URL of the first level")
parser.add_argument("level1_keyword", help="Keyword to look for in the first-level links")
parser.add_argument("level2_keyword", help="Keyword to look for in the second-level links")
parser.add_argument("level3_keyword", help="Keyword to look for in the third-level links")
args = parser.parse_args()

# Get the command-line arguments
base_url = args.base_url
level1_keyword = args.level1_keyword
level2_keyword = args.level2_keyword
level3_keyword = args.level3_keyword

# Make a request to the first-level URL and get the HTML content
response = requests.get(base_url)
html_content = response.text

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, "html.parser")

# Find all the second-level URLs that contain the keyword
level2_links = [link["href"] for link in soup.find_all("a") if level1_keyword in link.text.lower() and level2_keyword in link["href"].lower()]

# Create the directory structure, if it doesn't already exist
base_directory = "pdfs"
if not os.path.exists(base_directory):
    os.makedirs(base_directory)

# Download the PDF files and save them to the local file system
for level2_link in level2_links:
    level2_url = base_url + level2_link
    level2_response = requests.get(level2_url)
    level2_html_content = level2_response.text
    level2_soup = BeautifulSoup(level2_html_content, "html.parser")

    # Find all the third-level URLs that contain the keyword
    pdf_links = [link["href"] for link in level2_soup.find_all("a") if level3_keyword in link.text.lower() and link["href"].endswith(".pdf")]

    # Download each PDF file
    for pdf_link in pdf_links:
        pdf_response = requests.get(pdf_link)
        pdf_content = pdf_response.content
        pdf_filename = os.path.join(base_directory, pdf_link.split("/")[-1])
        with open(pdf_filename, "wb") as pdf_file:
            pdf_file.write(pdf_content)

