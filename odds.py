import os
import time
import config
import requests
from bs4 import BeautifulSoup
from selenium import webdriver


class OddsManager:
    def __init__(self, tan_odds_list, fuku_min_odds_list, umaren_odds_list, wide_min_odds_list, umatan_odds_list, trio_odds_list):
        self.tan_odds_list = tan_odds_list
        self.fuku_min_odds_list = fuku_min_odds_list
        self.umaren_odds_list = umaren_odds_list
        self.wide_min_odds_list = wide_min_odds_list
        self.umatan_odds_list = umatan_odds_list
        self.trio_odds_list = trio_odds_list


class Odds:
    def __init__(self, umano, odds):
        self.umano = umano
        self.odds = odds

    def to_string(self):
        return 'Odds=[umano={}, odds={}]'.format(
            self.umano, self.odds)


def get_odds_manager(opdt, race_course, rno):
    print('オッズ取得中...')
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    # options.add_argument('--headless')

    driver = get_webdriver(options)

    # netkeibaのrace_idを取得
    netkeiba_race_id = get_netkeiba_race_id(opdt, race_course, rno)

    # netkeibaにログイン
    login_netkeiba(driver)

    # オッズをスクレイピング
    tan_odds_list = get_tan_odds_list(netkeiba_race_id, driver)
    fuku_min_odds_list = get_fuku_min_odds_list(netkeiba_race_id, driver)
    umaren_odds_list = get_umaren_odds_list(netkeiba_race_id, driver)
    wide_min_odds_list = get_wide_min_odds_list(netkeiba_race_id, driver)
    umatan_odds_list = get_umatan_odds_list(netkeiba_race_id, driver)
    trio_odds_list = get_trio_odds_list(netkeiba_race_id, len(tan_odds_list), driver)

    driver.quit()

    return OddsManager(tan_odds_list, fuku_min_odds_list, umaren_odds_list, wide_min_odds_list, umatan_odds_list, trio_odds_list)


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

    netkeiba_race_id = f'{year}{race_course.cd}{kaisai_kai.zfill(2)}{kaisai_nichi.zfill(2)}{rno.zfill(2)}'
    return netkeiba_race_id


def login_netkeiba(driver):
    url = 'https://regist.netkeiba.com/account/?pid=login'
    driver.get(url)

    # ログイン情報を入力
    driver.find_element_by_name('login_id').send_keys(config.NETKEIBA_LOGIN_ID)
    driver.find_element_by_name('pswd').send_keys(config.NETKEIBA_LOGIN_PASSWORD)
    driver.find_element_by_css_selector('input[alt="ログイン"]').click()

    time.sleep(3)

# 単勝オッズを取得
def get_tan_odds_list(netkeiba_race_id, driver):
    url = f'https://race.netkeiba.com/odds/index.html?type=b1&race_id={netkeiba_race_id}&rf=shutuba_submenu'

    driver.get(url)
    time.sleep(3)

    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')

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

    return tan_odds_list


# 複勝下限オッズを取得
def get_fuku_min_odds_list(netkeiba_race_id, driver):
    url = f'https://race.netkeiba.com/odds/index.html?type=b1&race_id={netkeiba_race_id}&rf=shutuba_submenu'

    driver.get(url)
    time.sleep(3)

    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')

    blocks = soup.find('div', id='odds_fuku_block').find_all('td', class_='Odds')

    fuku_min_odds_list = []
    for index, block in enumerate(blocks):
        odds = block.span

        # 出走取り消しなどでオブジェクトが取得できない時はオッズを0にセットする
        if odds is None:
            fuku_min_odds_list.append(Odds(str(index + 1).zfill(2), 0))
            continue

        # オッズを取得
        fuku_min_odds = float(odds.string.split(' ')[0])
        fuku_min_odds_list.append(Odds(str(index + 1).zfill(2), fuku_min_odds))

    return fuku_min_odds_list


# 馬連オッズを取得
def get_umaren_odds_list(netkeiba_race_id, driver):
    umaren_odds_list = []
    url = f'https://race.netkeiba.com/odds/index.html?type=b4&race_id={netkeiba_race_id}&housiki=c0'

    driver.get(url)
    time.sleep(3)

    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')

    jiku_blocks = soup.find_all('table', class_='Odds_Table')

    for index, jiku_block in enumerate(jiku_blocks):
        jiku_umano = str(index + 1).zfill(2)
        himo_numbers = jiku_block.find_all('td', class_='Waku_Normal')
        himo_odds = jiku_block.find_all('span', class_='transition-color')
        for i in range(len(himo_numbers)):
            himo_umano = himo_numbers[i].string.zfill(2)
            odds = float(himo_odds[i].string)
            umaren_odds_list.append(Odds(f'{jiku_umano}-{himo_umano}', odds))

    return umaren_odds_list


# ワイド下限オッズを取得
def get_wide_min_odds_list(netkeiba_race_id, driver):
    wide_min_odds_list = []
    url = f'https://race.netkeiba.com/odds/index.html?type=b5&race_id={netkeiba_race_id}&housiki=c0&rf=shutuba_submenu'

    driver.get(url)
    time.sleep(3)

    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')

    jiku_blocks = soup.find_all('table', class_='Odds_Table')

    for index, jiku_block in enumerate(jiku_blocks):
        jiku_umano = str(index + 1).zfill(2)
        himo_numbers = jiku_block.find_all('td', class_='Waku_Normal')
        umaren_odds = jiku_block.find_all('span', class_='transition-color')
        for i in range(len(himo_numbers)):
            himo_umano = himo_numbers[i].string.zfill(2)
            odds = float(umaren_odds[i].string)
            wide_min_odds_list.append(Odds(f'{jiku_umano}-{himo_umano}', odds))

    return wide_min_odds_list


# 馬単オッズを取得
def get_umatan_odds_list(netkeiba_race_id, driver):
    umatan_odds_list = []
    url = f'https://race.netkeiba.com/odds/index.html?type=b6&race_id={netkeiba_race_id}&housiki=c0&rf=shutuba_submenu'

    driver.get(url)

    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')

    time.sleep(3)

    jiku_blocks = soup.find_all('table', class_='Odds_Table')

    for index, jiku_block in enumerate(jiku_blocks):
        jiku_umano = str(index + 1).zfill(2)
        himo_numbers = jiku_block.find_all('td', class_='Waku_Normal')
        umatan_odds = jiku_block.find_all('span', class_='transition-color')
        for i in range(len(himo_numbers)):
            himo_umano = himo_numbers[i].string.zfill(2)
            odds = float(umatan_odds[i].string)
            umatan_odds_list.append(Odds(f'{jiku_umano}-{himo_umano}', odds))

    return umatan_odds_list


# 3連複オッズを取得
def get_trio_odds_list(netkeiba_race_id, num_of_horse, driver):
    trio_odds_list = []

    for jiku_no in range(1, num_of_horse + 1):
        jiku1_umano = str(jiku_no).zfill(2)
        url = f'https://race.netkeiba.com/odds/index.html?type=b7&race_id={netkeiba_race_id}&housiki=c0&rf=shutuba_submenu&jiku={jiku_no}'
        driver.get(url)
        time.sleep(3)

        html = driver.page_source.encode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')

        jiku2_blocks = soup.find_all('table', class_='Odds_Table')

        for jiku2_block in jiku2_blocks:
            jiku2_umano = jiku2_block.find('tr', class_='col_label').find('th').string.zfill(2)
            jiku3_umanos = jiku2_block.find_all('td', class_='Waku_Normal')
            trio_odds = jiku2_block.find_all('span', class_='transition-color')
            for i in range(len(jiku3_umanos)):
                jiku3_umano = jiku3_umanos[i].string.zfill(2)
                odds = float(trio_odds[i].string)
                trio_odds_list.append(Odds(f'{jiku1_umano}-{jiku2_umano}-{jiku3_umano}', odds))

    return trio_odds_list


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
