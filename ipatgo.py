import os
import config


def vote(csv_list, number):
    for csv in csv_list:
        print(f'投票中...{csv}')
        try:
            print(rf'.\ipatgo\ipatgo.exe file {config.IPATS[number]["INET_ID"]} {config.IPATS[number]["SUBSCRIBER_NUMBER"]} {config.IPATS[number]["PIN_NUMBER"]} {config.IPATS[number]["P_ARS_NUMBER"]} ' + csv)
            os.system(rf'.\ipatgo\ipatgo.exe file {config.IPATS[number]["INET_ID"]} {config.IPATS[number]["SUBSCRIBER_NUMBER"]} {config.IPATS[number]["PIN_NUMBER"]} {config.IPATS[number]["P_ARS_NUMBER"]} ' + csv)
        except Exception as e:
            print(e.args)
            return 1