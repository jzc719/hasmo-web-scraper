import scrapy
from bs4 import BeautifulSoup

# Author: Jeffrey Chen

class BCGSpider(scrapy.Spider):

    # Name of the spider
    # This is used when running in terminal, not the file name
    name = 'bcg_scraper'

    # URL(s) to start crawling at
    start_urls = [
        'https://bcg.com',
    ]

    # To prevent offsite crawling
    allowed_domains = [
        'bcg.com',
    ]

    # Keywords to filter links
    link_keywords = ['service', 'case-studies', 'client-testimonials', 'leadership', 'insight']

    # Keywords to extract data
    data_keywords = ['service', 'case stud', 'quote', 'thought leadership', 'insight']

    def parse(self, response):
        # Extract all links on the page
        links = response.css('a::attr(href)').getall()
        
        # Filter and follow links based on keywords
        for link in links:
            if any(keyword in link for keyword in self.link_keywords):
                yield response.follow(link, self.parse)

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
