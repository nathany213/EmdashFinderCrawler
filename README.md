# EmdashFinderCrawler
So you know how literally anything you search up now, you get at least one ai-generated website with ai generated text? 
Well I made a crawler that checks for em dashes in a website and its related pages' text for em dashes (common identifier of ai if you didnt know already). You just have to input a site url, and the code will check that site along with sites with the same path of the original.

https://youtu.be/xO85eEyAfAM to see it working on a website

## Libraries
It uses 4 main libraries:
- requests (https://pypi.org/project/requests/)
- beautiful soup (https://pypi.org/project/beautifulsoup4/)
- urllib.parse (included)
- time (includeD)
~~~
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import time
~~~
<img width="941" height="482" alt="image" src="https://github.com/user-attachments/assets/12cfe9d6-bf3f-4f6c-9983-a845deab5fb7" />
