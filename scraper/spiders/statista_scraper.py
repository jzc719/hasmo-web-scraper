import scrapy
from bs4 import BeautifulSoup

class MySpider(scrapy.Spider):

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'ROBOTSTXT_OBEY': False,  # Disable robots.txt obeying for testing
    }
    name = 'statista_scraper'
    start_urls = [
        'https://statista.com',
    ]
    allowed_domains = [
        'statista.com',
    ]

    # Keywords to filter links
    link_keywords = ['market', 'financ', 'analysis', 'econom']

    # Keywords to extract data
    data_keywords = ['market', 'financ', 'analysis', 'econom']

    def parse(self, response):
        # Extract all links on the page
        links = response.css('a::attr(href)').getall()
        
        # Filter links based on keywords
        filtered_links = [link for link in links if any(keyword in link for keyword in self.link_keywords)]
        
        # Visit each filtered link once
        for link in filtered_links:
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

            # Yield the data dictionary (optional)
            yield {
                "url": response.url,
                "data": data_dict
            }
