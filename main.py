import openpyxl
from odds import get_odds_manager
from yumachan import get_yumachan


def main():

    print('ゆまちゃんデータ取得中...')
    yumachan = get_yumachan()

    print('オッズ取得中...')
    odds_manager = get_odds_manager(yumachan.opdt, yumachan.race_course, yumachan.rno)

    print('エクセルに転記中...')
    wb = openpyxl.load_workbook('xls/calc.xlsm', keep_vba=True)
    ws = wb['sheet']

    # 出走頭数を取得
    horse_num = len(yumachan.horse_list)

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

    print('全部完了！')


if __name__ == '__main__':
    main()
