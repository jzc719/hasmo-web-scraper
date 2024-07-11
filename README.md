Author: Jeffrey Chen

Developed for the purposes and usage of Hasmo Consulting. 

Project contains various spiders for web crawling. Spiders are all saved under the "spiders" folder.

To execute, make sure the scrapy and BeautifulSoup packages are installed. Run "scrapy crawl _____" in terminal, fill in the blank with the spider name.

Attach "-o" flag to specify output, i.e. "scrapy crawl _____ -o output.json".

User can change parameters at the top of each spider, including starting URLs, allowed domains, and link and data keywords.
