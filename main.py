import openpyxl

from odds import get_realtime_odds
from yumachan import get_yumachan


def main():
    # ゆまちゃんのデータを取ってくる
    yumachan = get_yumachan()

    for horse in sorted(yumachan.horse_list):
        print(horse.to_string())

    # # リアルタイムオッズを取得
    # realtime_odds = get_realtime_odds(yumachan.opdt, yumachan.rcoursecd, yumachan.rno)

    # エクセルに転記
    wb = openpyxl.load_workbook('xls/calc.xlsm', keep_vba=True)
    ws = wb['sheet']

    # 出走頭数を取得
    horse_num = len(yumachan.horse_list)

    # 馬の勝率を転記
    for horse in sorted(yumachan.horse_list):
        ws.cell(row=1 + int(horse.umano), column=9, value=float(horse.probability))
    #
    # # 単勝オッズを転記
    # for i, tanodds in enumerate(realtime_odds.tan_odds_list):
    #     ws.cell(row=2 + i, column=4, value=float(tanodds.tanodds))
    #
    # # 複勝オッズを転記
    # for i, fuku_min_odds in enumerate(realtime_odds.fuku_min_odds_list):
    #     ws.cell(row=2 + i, column=16, value=float(fuku_min_odds.fuku_min_odds))
    #
    # # 馬連オッズを転記
    # count = 0
    # for i in range(horse_num - 1):
    #     for k in range(horse_num - i - 1):
    #         ws.cell(row=65 + k + i, column=2 + i, value=float(realtime_odds.umaren_odds_list[count].umaren_odds))
    #         count += 1
    #
    # # ワイドオッズを転記
    # count = 0
    # for i in range(horse_num - 1):
    #     for k in range(horse_num - i - 1):
    #         ws.cell(row=145 + k + i, column=2 + i, value=float(realtime_odds.wide_odds_list[count].wideodds))
    #         count += 1
    #
    # # 3連複オッズを転記
    # count = 0
    # for i in range(horse_num - 1):
    #     for k in range(horse_num - i - 1):
    #         for l in range(horse_num - i - k - 2):
    #             ws.cell(row=307 + 81 * i + k + l, column=2 + i + k,
    #                     value=float(realtime_odds.trio_odds_list[count].trio_odds))
    #             count += 1

    wb.save('xls/calc_after.xlsm')
    wb.close()


if __name__ == '__main__':
    main()
