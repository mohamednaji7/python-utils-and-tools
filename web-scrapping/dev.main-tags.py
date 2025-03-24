import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
from urllib.parse import urlparse
import os
from rich.console import Console
from rich.logging import RichHandler
import logging
import json
import random 

console = Console()

logging.basicConfig(
    level=logging.DEBUG,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(console=console)]
)

logger = logging.getLogger("rich")

class WebScraper:
    def __init__(self, output_dir="scraped_data"):
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        ]
        self.headers = {
            'User-Agent': random.choice(user_agents)
        }
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
    def extract_domain(self, url):
        """Extract domain name from URL"""
        parsed_uri = urlparse(url)
        return parsed_uri.netloc
        
    def clean_text(self, text):
        """Clean extracted text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        # Remove script and style content that might be left
        text = re.sub(r'<script.*?</script>', '', text, flags=re.DOTALL)
        text = re.sub(r'<style.*?</style>', '', text, flags=re.DOTALL)
        return text
    
    def clean_content(self, soup):
        """Clean extracted content"""
    
        # Remove unwanted elements (ads, images, etc.)
        for element in soup.find_all(['script', 'style', 'img', 'svg', 'noscript', 'header', 'footer', 'nav']):
            element.decompose()
            
        # Remove elements with common ad-related class names or ids
        ad_patterns = ['ad', 'ads', 'advertisement', 'banner', 'popup', 'modal', 'cookie']
        for pattern in ad_patterns:
            for element in soup.find_all(class_=re.compile(pattern, re.IGNORECASE)):
                element.decompose()
            for element in soup.find_all(id=re.compile(pattern, re.IGNORECASE)):
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
        """Extract main content"""
        # Find the main content container
        main_container = soup.find('main')  # Many websites use <main> for primary content
        if not main_container:
            main_container = soup.find('article')  # Fallback to <article>
        if not main_container:
            main_container = soup.find('body')  # As a last resort, extract from <body>
        if not main_container:
            print(soup.prettify())
            raise Exception("Could not find main content container or body")
        
        # logger.debug(f"Content areas: {content_areas}")
        
        paragraphs = []
        for tag in main_container.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li','span']):
            if tag.text.strip():
                paragraphs.append(tag.text.strip())
        # Join paragraphs with newlines
        main_content = '\n\n'.join(paragraphs)
        main_content = self.clean_text(main_content)

        # logger.debug(f"Main content: {main_content}")     
        videos = []
        for iframe in main_container.find_all(['iframe']):
            if iframe.get('src') and 'youtube' in iframe.get('src'):
                video_url = iframe.get('src')
                video_title = iframe.get('title') or ''
                videos.append({'url': video_url, 'title': video_title})




        return main_content, videos

    def get_content(self, url):
        """Extract relevant content from a URL"""
        response = requests.get(url, headers=self.headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')

        # Clean content
        soup = self.clean_content(soup)


        # Extract meta data
        title, description = self.get_meta_data(soup) 
            
        # Extract main content
        main_content, videos = self.extract_main_content(soup)   
        
        
        return {
            'url': url,
            'domain': self.extract_domain(url),
            'title': title,
            'description': description,
            'main_content': main_content,
            'content_length': len(main_content),
            'videos': videos   ,
            'scrape_timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        }
            

    
    def scrape_urls(self, urls, delay=2):
        """Scrape a list of URLs with a delay between requests"""
        results = []
        
        for url in urls:
            logger.info(f"Scraping: {url}")
            try:
                data = self.get_content(url)
        
                

                
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
                        f.write(f"VIDEOS: {data['videos']}\n")
                        f.write(f"\n")
                        f.write(data['main_content'])
                
                # Be respectful with a delay between requests
                time.sleep(delay)
            except requests.exceptions.RequestException as e:
                logger.error(f"Request error {e}")
            except Exception as e:
                logger.error(f"{e}")

        # Create DataFrame and save as CSV
        df = pd.DataFrame(results)

        csv_path = f"{self.output_dir}/scraped_data.csv"

        df.to_csv(csv_path, index=False)
        
        console.print(f"Scraping completed. Data saved to {csv_path}")

        return results


if __name__ == "__main__":
    main_dir = "main-tags-output/scrapped_data"
    os.makedirs(main_dir, exist_ok=True)

    urls_JSON = json.load(open('input/urls.json'))
    for key in urls_JSON:
        urls_to_scrape = urls_JSON[key]['links']
        scraper = WebScraper(output_dir=f"{main_dir}/{key}")
        results = scraper.scrape_urls(urls_to_scrape, delay=3)