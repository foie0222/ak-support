from horse import get_horse_list_from_png_by_google
from scraper import Scraper


class YumaChan:
    def __init__(self, opdt, race_course, rno, rname, horse_list):
        self.opdt = opdt
        self.race_course = race_course
        self.rno = rno
        self.rname = rname
        self.horse_list = horse_list


def get_yumachan():
    print('ゆまちゃんデータ取得中...')
    scraper = Scraper()
    header_txt = scraper.get_header_txt()
    png_url = scraper.get_png_url()

    opdt = get_opdt(header_txt)
    race_course = get_race_course(header_txt[:15])
    rno = get_rno(header_txt)
    rname = get_rname(header_txt)
    horser_list = get_horse_list_from_png_by_google(png_url)

    return YumaChan(opdt, race_course, rno, rname, horser_list)


def get_opdt(row):
    return row[0:8]


class RaceCource:
    def __init__(self, name, roman, cd):
        self.name = name
        self.roman = roman
        self.cd = cd


def get_race_course(row):
    if '札幌' in row:
        return RaceCource('札幌', 'SAPPORO', '01')
    if '函館' in row:
        return RaceCource('函館', 'HAKODATE', '02')
    if '福島' in row:
        return RaceCource('福島', 'FUKUSHIMA', '03')
    if '新潟' in row:
        return RaceCource('新潟', 'NIIGATA', '04')
    if '東京' in row:
        return RaceCource('東京', 'TOKYO', '05')
    if '中山' in row:
        return RaceCource('中山', 'NAKAYAMA', '06')
    if '中京' in row:
        return RaceCource('中京', 'CHUKYO', '07')
    if '京都' in row:
        return RaceCource('京都', 'KYOTO', '08')
    if '阪神' in row:
        return RaceCource('阪神', 'HANSHIN', '09')
    if '小倉' in row:
        return RaceCource('小倉', 'KOKURA', '10')
    return None


def get_race_course_from_cd(cd):
    digit2_cd = cd.zfill(2)
    if '01' == digit2_cd:
        return RaceCource('札幌', 'SAPPORO', '01')
    if '02' == digit2_cd:
        return RaceCource('函館', 'HAKODATE', '02')
    if '03' == digit2_cd:
        return RaceCource('福島', 'FUKUSHIMA', '03')
    if '04' == digit2_cd:
        return RaceCource('新潟', 'NIIGATA', '04')
    if '05' == digit2_cd:
        return RaceCource('東京', 'TOKYO', '05')
    if '06' == digit2_cd:
        return RaceCource('中山', 'NAKAYAMA', '06')
    if '07' == digit2_cd:
        return RaceCource('中京', 'CHUKYO', '07')
    if '08' == digit2_cd:
        return RaceCource('京都', 'KYOTO', '08')
    if '09' == digit2_cd:
        return RaceCource('阪神', 'HANSHIN', '09')
    if '10' == digit2_cd:
        return RaceCource('小倉', 'KOKURA', '10')
    return None


def get_rno(row):
    return row[11:].split('R')[0].zfill(2)


def get_rname(row):
    return row.split('R ')[1]
