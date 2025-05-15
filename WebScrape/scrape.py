# Importing required modules from Selenium
from selenium.webdriver import Remote, ChromeOptions
# Importing a low-level remote connection handler for Chromium-based browsers
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
# BeautifulSoup is used to parse and navigate HTML content
from bs4 import BeautifulSoup
# Load environment variables from a .env file
from dotenv import load_dotenv
# Standard library module for interacting with the operating system
import os

# Load all environment variables from a .env file into the environment
load_dotenv()

# Fetch the value of 'SBR_WEBDRIVER' from environment variables
# This is expected to be a URL or connection string to the Scraping Browser
SBR_WEBDRIVER = os.getenv("SBR_WEBDRIVER")

# Function to scrape a website using Scraping Browser infrastructure
def scrape_website(website):
    print("Connecting to Scraping Browser...")

    # Create a remote connection to the Scraping Browser using Chromium protocol
    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, "goog", "chrome")

    # Create a Remote WebDriver session using the Scraping Browser connection
    # ChromeOptions is passed to configure Chrome-specific options (can be empty)
    with Remote(sbr_connection, options=ChromeOptions()) as driver:
        # Navigate to the target website URL
        driver.get(website)

        print("Waiting captcha to solve...")

        # Execute a custom DevTools Protocol command to wait for CAPTCHA solving
        # This is specific to Scraping Browser that supports this custom CDP command
        solve_res = driver.execute(
            "executeCdpCommand",
            {
                "cmd": "Captcha.waitForSolve",  # Custom CDP command
                "params": {"detectTimeout": 10000},  # Wait up to 10 seconds
            },
        )

        # Print the status of CAPTCHA solving
        print("Captcha solve status:", solve_res["value"]["status"])

        print("Navigated! Scraping page content...")

        # Get the full HTML source of the page after CAPTCHA is solved and loaded
        html = driver.page_source

        # Return the HTML content for further processing
        return html

# Function to extract just the <body> content from an HTML page
def extract_body_content(html_content):
    # Parse the full HTML using BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Extract the <body> tag and its content
    body_content = soup.body

    # If body content exists, return it as a string
    if body_content:
        return str(body_content)

    # If no <body> tag found, return an empty string
    return ""

# Function to clean extracted <body> content by removing scripts/styles and extra whitespace
def clean_body_content(body_content):
    # Parse the body HTML using BeautifulSoup
    soup = BeautifulSoup(body_content, "html.parser")

    # Remove all <script> and <style> elements to avoid unwanted content
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    # Extract plain text from the remaining HTML, using line breaks as separators
    cleaned_content = soup.get_text(separator="\n")

    # Strip each line and remove empty lines
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )

    # Return cleaned text
    return cleaned_content

# Function to split large content into chunks of a defined maximum length
def split_dom_content(dom_content, max_length=6000):
    # Use list slicing to break the content into smaller pieces of 'max_length'
    return [
        dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)
    ]
