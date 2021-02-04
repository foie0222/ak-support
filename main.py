import openpyxl

from yumachan import get_yumachan


def main():
    # ゆまちゃんのデータを取ってくる
    yumachan = get_yumachan()

    for horse in sorted(yumachan.horse_list):
        print(horse.to_string())

    # エクセルに転記
    wb = openpyxl.load_workbook('./calc.xlsm')
    ws = wb['sheet']

    # 馬の勝率を転記
    for horse in sorted(yumachan.horse_list):
        ws[f"I{1 + int(horse.umano)}"].value = float(horse.probability)

    wb.save('./calc_after.xlsm')
    wb.close()


if __name__ == '__main__':
    main()
