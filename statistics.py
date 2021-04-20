import requests
import numpy as np
import pandas as pd
import time
import os
from bs4 import BeautifulSoup
from datetime import date

filename = date.today().strftime('%Y-%m-%d.csv')
df = pd.read_csv(filename)
print(df.head(10))