import os
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver


class OddsManager:
    def __init__(self, tan_odds_list, fuku_min_odds_list, umaren_odds_list):
        self.tan_odds_list = tan_odds_list
        self.fuku_min_odds_list = fuku_min_odds_list
        self.umaren_odds_list = umaren_odds_list


class Odds:
    def __init__(self, umano, odds):
        self.umano = umano
        self.odds = odds

    def to_string(self):
        return 'Odds=[umano={}, odds={}]'.format(
            self.umano, self.odds)


def get_odds_manager(opdt, race_course, rno):
    netkeiba_race_id = get_netkeiba_race_id(opdt, race_course, rno)
    return OddsManager(get_tan_odds_list(netkeiba_race_id),
                       get_fuku_min_odds_list(netkeiba_race_id),
                       get_umaren_odds_list(netkeiba_race_id))


# netkeibaのrace_idを取得
def get_netkeiba_race_id(opdt, race_course, rno):
    year = opdt[0:4]
    month = int(opdt[4:6])  # 0落ちさせる
    date = opdt[4:8]
    jra_url = f'https://www.jra.go.jp/keiba/calendar{year}/{year}/{month}/{date}.html'
    response = requests.get(jra_url)
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.text, 'html.parser')

    tables = soup.find_all('table', class_='narrow-xy')
    for table in tables:
        kaisai_info = table.find('div', class_='main').text
        if race_course.name in kaisai_info:
            kaisai_kai = kaisai_info[:kaisai_info.find('回')]
            kaisai_nichi = kaisai_info[kaisai_info.find(race_course.name) + 2:kaisai_info.find('日')]

    netkeiba_race_id = f'{year}{race_course.cd}{kaisai_kai.zfill(2)}{kaisai_nichi.zfill(2)}{rno}'
    return netkeiba_race_id


# 単勝オッズを取得
def get_tan_odds_list(netkeiba_race_id):
    url = f'https://race.netkeiba.com/odds/index.html?type=b1&race_id={netkeiba_race_id}&rf=shutuba_submenu'

    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument('--headless')

    driver = get_webdriver(options)
    driver.get(url)

    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup(html, "html.parser")

    time.sleep(2)

    blocks = soup.find('div', id='odds_tan_block').find_all('td', class_='Odds')

    tan_odds_list = []
    for index, block in enumerate(blocks):
        odds = block.span

        # 出走取り消しなどでオブジェクトが取得できない時はオッズを0にセットする
        if odds is None:
            tan_odds_list.append(Odds(str(index + 1).zfill(2), 0))
            continue

        # オッズを取得
        tan_odds = float(odds.string)
        tan_odds_list.append(Odds(str(index + 1).zfill(2), tan_odds))

    driver.quit()

    return tan_odds_list


# 複勝下限オッズを取得
def get_fuku_min_odds_list(netkeiba_race_id):
    url = f'https://race.netkeiba.com/odds/index.html?type=b1&race_id={netkeiba_race_id}&rf=shutuba_submenu'

    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument('--headless')

    driver = get_webdriver(options)
    driver.get(url)

    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup(html, "html.parser")

    time.sleep(2)

    blocks = soup.find('div', id='odds_fuku_block').find_all('td', class_='Odds')

    fuku_min_odds_list = []
    for index, block in enumerate(blocks):
        odds = block.span

        # 出走取り消しなどでオブジェクトが取得できない時はオッズを0にセットする
        if odds is None:
            fuku_min_odds_list.append(Odds(str(index + 1).zfill(2), 0))
            continue

        # オッズを取得
        fuku_min_odds = float(odds.string.split(" ")[0])
        fuku_min_odds_list.append(Odds(str(index + 1).zfill(2), fuku_min_odds))

    driver.quit()

    return fuku_min_odds_list


# 馬連オッズを取得
def get_umaren_odds_list(netkeiba_race_id):
    umaren_odds_list = []
    url = f'https://race.netkeiba.com/odds/index.html?type=b4&race_id={netkeiba_race_id}&housiki=c0'

    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument('--headless')

    driver = get_webdriver(options)
    driver.get(url)

    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup(html, "html.parser")

    time.sleep(2)

    jiku_blocks = soup.find_all('table', class_='Odds_Table')

    for index, jiku_block in enumerate(jiku_blocks):
        jiku_umano = str(index + 1).zfill(2)
        himo_numbers = jiku_block.find_all('td', class_='Waku_Normal')
        himo_odds = jiku_block.find_all('span', class_='transition-color')
        for i in range(len(himo_numbers)):
            himo_umano = himo_numbers[i].string.zfill(2)
            odds = float(himo_odds[i].string)
            umaren_odds_list.append(Odds(f'{jiku_umano}-{himo_umano}', odds))

    driver.quit()

    return umaren_odds_list


def get_webdriver(options):
    if os.name == 'nt':
        return webdriver.Chrome(
            options=options,
            executable_path='./driver/chromedriver.exe')

    if os.name == 'posix':
        return webdriver.Chrome(
            options=options,
            executable_path='./driver/chromedriver')

    return None
