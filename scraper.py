import requests
from bs4 import BeautifulSoup

# データを取得する対象
URL = "https://www.ai-yuma.com/"


class Scraper:
    def __init__(self):
        self.response = requests.get(URL)

    def get_header_txt(self):
        self.response.encoding = self.response.apparent_encoding
        soup = BeautifulSoup(self.response.text, "html.parser")
        target_soups = soup.find_all("div", class_="entry-inner")

        for target_soup in target_soups:
            if target_soup.header.find(
                    "a", class_="entry-category-link category-地方競馬") is not None:  # 地方競馬ならスキップ
                continue
            return str(
                target_soup.header.find(
                    "a", class_="entry-title-link bookmark").string)

        return None

    def get_png_url(self):
        self.response.encoding = self.response.apparent_encoding
        soup = BeautifulSoup(self.response.text, "html.parser")
        target_soups = soup.find_all("div", class_="entry-inner")

        for target_soup in target_soups:
            if target_soup.header.find(
                    "a", class_="entry-category-link category-地方競馬") is not None:  # 地方競馬ならスキップ
                continue
            return str(
                target_soup.find(
                    "img",
                    class_="hatena-fotolife")['src'])
