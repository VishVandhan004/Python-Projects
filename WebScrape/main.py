# Import the Streamlit library to build the web UI
import streamlit as st

# Import scraping and DOM processing functions from a local module called `scrape.py`
from scrape import (
    scrape_website,          # Function to connect to Scraping Browser and retrieve page HTML
    extract_body_content,    # Function to extract <body> section from HTML
    clean_body_content,      # Function to remove scripts, styles, and whitespace from body
    split_dom_content,       # Function to break large text into smaller chunks
)

# Import a parsing function from a local module called `parse.py`
from parse import parse_with_ollama  # This function likely uses an LLM to interpret content

# -------- Streamlit Web Interface Starts -------- #

# Set the title at the top of the web app
st.title("AI Web Scraper")

# Input field where the user types the URL of the website to scrape
url = st.text_input("Enter Website URL")

# -------- Step 1: Scrape the Website -------- #

# When the user clicks the "Scrape Website" button
if st.button("Scrape Website"):
    # Check if the URL input is not empty
    if url:
        # Notify the user that scraping is in progress
        st.write("Scraping the website...")

        # Call the scraping function to get the raw HTML
        dom_content = scrape_website(url)

        # Extract only the <body> tag content from the HTML
        body_content = extract_body_content(dom_content)

        # Clean the <body> content by removing scripts, styles, and formatting
        cleaned_content = clean_body_content(body_content)

        # Save the cleaned content into Streamlit's session state for later use
        st.session_state.dom_content = cleaned_content

        # Provide an expandable section to preview the scraped content
        with st.expander("View DOM Content"):
            # Show the cleaned DOM content in a read-only text area
            st.text_area("DOM Content", cleaned_content, height=300)

# -------- Step 2: Parse the DOM Content Using Natural Language -------- #

# Check if we already have DOM content stored in session state (i.e., scraping was successful)
if "dom_content" in st.session_state:
    # Provide a text area where the user can describe what they want to extract/understand
    parse_description = st.text_area("Describe what you want to parse")

    # When the user clicks the "Parse Content" button
    if st.button("Parse Content"):
        # Make sure the description is not empty
        if parse_description:
            # Notify the user that parsing is in progress
            st.write("Parsing the content...")

            # Break the cleaned DOM content into smaller chunks to process incrementally
            dom_chunks = split_dom_content(st.session_state.dom_content)

            # Pass the content and user description to the LLM-based parser
            parsed_result = parse_with_ollama(dom_chunks, parse_description)

            # Display the result of parsing to the user
            st.write(parsed_result)
