import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import html2text
import random
import json
import re
from urllib.parse import urlparse
import os
from rich.console import Console
from rich.logging import RichHandler
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from rich.traceback import install
install()


console = Console()

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(console=console)]
)

logger = logging.getLogger("rich")

class WebClient:

    def get_soup_response(self, url):
        """get HTML response of an URL"""
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        ]
        self.headers = {
            'User-Agent': random.choice(user_agents)
        }
        response = requests.get(url, headers=self.headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        return soup

    def get_rendered_soup_response(self, url):
        """get rendered HTML response of an URL"""

        options = Options()
        options.add_argument("--headless")  # Run in headless mode
        options.add_argument("--disable-blink-features=AutomationControlled")

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(url)

        page_source = driver.page_source  # Get rendered HTML
        driver.quit()

        soup = BeautifulSoup(page_source, "html.parser")

        return soup


class HtmlCleaner:

        

    def clean_content(self, soup):
        """Clean extracted content"""
    
        # Remove unwanted elements (ads, images, etc.)
        for element in soup.find_all(['script', 'style', 'img', 'svg', 'noscript', 'header', 'footer', 'nav']):
            element.decompose()
            
        # Remove elements with common ad-related class names or ids
        ad_patterns = ['ad', 'ads', 'advertisement', 'banner', 'popup', 'modal', 'cookie']
        # for pattern in ad_patterns:
        #     for element in soup.find_all(class_=re.compile(pattern, re.IGNORECASE)):
        #         element.decompose()
        #     for element in soup.find_all(id=re.compile(pattern, re.IGNORECASE)):
        #         element.decompose()

        # the regex removed everything

        for element in soup.find_all(ad_patterns):
            element.decompose()

        return soup
        
    def get_meta_data(self, soup):
        """Extract meta data"""
        # Extract metadata
        title = soup.title.text.strip() if soup.title else "No Title"        
        
        # Try to get a description from meta tags
        description = ""
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and 'content' in meta_desc.attrs:
            description = meta_desc['content']
        
        return title, description
    def extract_main_content(self, soup):
        """Extracts main content from a webpage and converts it into Markdown"""
        
        # Find the main content container
        main_container = soup.find('main') or soup.find('article') or soup.find('body')
        
        if not main_container:
            print(soup.prettify())
            raise Exception("Could not find main content container or body")

        # Convert HTML to Markdown
        markdown_converter = html2text.HTML2Text()
        markdown_converter.ignore_links = False  # Set to True if you don't want links
        markdown_content = markdown_converter.handle(str(main_container))

        return markdown_content
    



    def extract_content(self, soup):
        """Extract relevant content from a URL"""

        # Clean content
        soup = self.clean_content(soup)


        # Extract meta data
        title, description = self.get_meta_data(soup) 


        # Extract main content
        main_content = self.extract_main_content(soup)   

        
        return {
            'title': title,
            'description': description,
            'main_content': main_content,
            'content_length': len(main_content),
            'scrape_timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        }
            

class WebScraper:
    def __init__(self, output_dir="scraped_data"):
        self.web_client = WebClient()
        self.html_cleaner = HtmlCleaner()
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
    




    def extract_domain(self, url):
        """Extract domain name from URL"""
        parsed_uri = urlparse(url)
        return parsed_uri.netloc
    
    def scrape_urls(self, urls, delay=2):
        """Scrape a list of URLs with a delay between requests"""
        results = []
        
        for url in urls:
            logger.info(f"Scraping: {url}")
            try:
                # soup = self.web_client.get_soup_response(url)
                soup = self.web_client.get_rendered_soup_response(url)
                soup = self.html_cleaner.clean_content(soup)
                                
                                
                # <DEBUGGING> --------------------------------------------------------
                # print(soup)
                # main_container = soup.find('main') or soup.find('article') or soup.find('body')
                # if not main_container:
                #     print(soup.prettify())

                #     raise Exception("Could not find main content container or body")


                # # print(main_container.prettify())
                # # print('*'*300)
                # print(main_container.text)
                # print('*'*300)
                # # Convert HTML to Markdown
                # markdown_converter = html2text.HTML2Text()
                # markdown_converter.ignore_links = True  # Set to True if you don't want links
                # markdown_content = markdown_converter.handle(str(main_container))
                # print(markdown_content)
                # print('*'*300)


                # print('main_container not None')
                # break 
                # # </ DEBUGGING> --------------------------------------------------------
                
                data = self.html_cleaner.extract_content(soup)       
                # Save individual result as text file
                if data['main_content']:
                    # Add data to results
                    results.append(data)
                    domain = self.extract_domain(url)
                    filename = f"{self.output_dir}/{domain} - {data['title']}.txt"
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(f"URL: {url}\n")
                        # add the sraping time to the file
                        f.write(f"SCRAPING TIME: {data['scrape_timestamp']}\n")
                        f.write(f"TITLE: {data['title']}\n")
                        f.write(f"DESCRIPTION: {data['description']}\n")
                        f.write(f"\n")
                        f.write(data['main_content'])
                            
                    with open(filename.replace('.txt', '.md'), 'w', encoding='utf-8') as f:
                        f.write(data['main_content'])
                
                # Be respectful with a delay between requests
                time.sleep(delay)
            except requests.exceptions.RequestException as e:
                logger.error(f"Request error {e}")
                console.print_exception()
            except Exception as e:
                logger.error(f"{e}")
                console.print_exception()

        # Create DataFrame and save as CSV
        df = pd.DataFrame(results)

        csv_path = f"{self.output_dir}/scraped_data.csv"

        df.to_csv(csv_path, index=False)
        
        console.print(f"Scraping completed. Data saved to {csv_path}")

        return results



if __name__ == "__main__":
    main_dir = "main-html2text-output/scrapped_data"
    os.makedirs(main_dir, exist_ok=True)

    urls_JSON = json.load(open('input/urls.json'))
    for key in urls_JSON:
        urls_to_scrape = urls_JSON[key]['links']
        scraper = WebScraper(output_dir=f"{main_dir}/{key}")
        results = scraper.scrape_urls(urls_to_scrape, delay=3)