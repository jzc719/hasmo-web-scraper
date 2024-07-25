import scrapy
from bs4 import BeautifulSoup

# Author: Jeffrey Chen

class Phillippines_Market_Trends(scrapy.Spider):

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'ROBOTSTXT_OBEY': False,  # Disable robots.txt obeying for testing
    }

    # Name of the spider
    # This is used when running in terminal, not the file name
    name = 'phillippines_market_trends'

    # URL(s) to start crawling at
    start_urls = [
        'https://www.bworldonline.com',
        'https://www.inquirer.net',
        'https://www.rappler.com',
        'https://insuranceasia.com',
        'https://www.philstar.com'
    ]

    # To prevent offsite crawling
    allowed_domains = [
        'bworldonline.com',
        'inquirer.net',
        'rappler.com',
        'insuranceasia.com',
        'philstar.com'
    ]

    # Keywords to extract data
    data_keywords = ['market', 'financ', 'analysis', 'econom', 'trend', 'report', 'industry', 'insurance']

    def parse(self, response):
        # Extract all links on the page
        links = response.css('a::attr(href)').getall()
        
        # Visit each link once
        for link in links:
            yield response.follow(link, self.parse_link)

    def parse_link(self, response):
        # Use BeautifulSoup to parse the page content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Dictionary to store the extracted data
        data_dict = {keyword: [] for keyword in self.data_keywords}
        found_any_keyword = False

        # Extract data based on keywords
        for keyword in self.data_keywords:
            elements = soup.find_all(string=lambda text: text and keyword.lower() in text.lower())
            for element in elements:
                parent = element.find_parent()
                data_text = parent.get_text(separator=' ', strip=True)
                data_dict[keyword].append(data_text)
                found_any_keyword = True

        # If any data keywords were found, print the dictionary
        if found_any_keyword:
            print(f"URL: {response.url}")
            print(data_dict)
            print('---')

            # Yield the data dictionary 
            yield {
                "url": response.url,
                "data": data_dict
            }
