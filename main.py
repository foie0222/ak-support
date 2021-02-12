import time

import openpyxl

from odds import get_odds_manager
from yumachan import get_yumachan


def main():
    start = time.time()

    print('ゆまちゃんデータ取得中...')
    yumachan = get_yumachan()

    # 出走頭数を取得
    horse_num = len(yumachan.horse_list)

    print('オッズ取得中...')
    odds_manager = get_odds_manager(yumachan.opdt, yumachan.race_course, yumachan.rno, horse_num)

    print('エクセルに転記中...')
    wb = openpyxl.load_workbook('xls/calc.xlsm', keep_vba=True)
    ws = wb['sheet']

    # 馬の勝率を転記
    for horse in sorted(yumachan.horse_list):
        ws.cell(row=1 + int(horse.umano), column=9, value=float(horse.probability))

    # 単勝オッズを転記
    for i, odds in enumerate(odds_manager.tan_odds_list):
        ws.cell(row=2 + i, column=4, value=float(odds.odds))

    # 複勝オッズを転記
    for i, odds in enumerate(odds_manager.fuku_min_odds_list):
        ws.cell(row=2 + i, column=16, value=float(odds.odds))

    # 馬連オッズを転記
    count = 0
    for i in range(horse_num - 1):
        for k in range(horse_num - i - 1):
            ws.cell(row=65 + k + i, column=2 + i, value=float(odds_manager.umaren_odds_list[count].odds))
            count += 1

    # ワイドオッズを転記
    count = 0
    for i in range(horse_num - 1):
        for k in range(horse_num - i - 1):
            ws.cell(row=145 + k + i, column=2 + i, value=float(odds_manager.wide_min_odds_list[count].odds))
            count += 1

    # 馬単オッズを転記
    count = 0
    for i in range(horse_num):
        for k in range(horse_num):
            if i == k:
                continue  # 軸紐が一致する箇所はスキップ
            ws.cell(row=225 + k, column=2 + i, value=float(odds_manager.umatan_odds_list[count].odds))
            count += 1

    # 3連複オッズを転記
    count = 0
    for i in range(horse_num):
        for k in range(horse_num - 1):
            for l in range(horse_num - k - 2):
                ws.cell(row=307 + 80 * i + k + l, column=2 + k,
                        value=float(odds_manager.trio_odds_list[count].odds))
                count += 1

    wb.save('xls/calc_after.xlsm')
    wb.close()

    elapsed_time = time.time() - start
    print(f'完了！処理時間 : {round(elapsed_time, 2)}[秒]')


if __name__ == '__main__':
    main()
