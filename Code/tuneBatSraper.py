from bs4 import BeautifulSoup as bs
import pandas as pd
pd.set_option('display.max_colwidth', 500)
import time
import requests
import random

page = requests.get("https://tunebat.com/")
page
# <Response [200]>