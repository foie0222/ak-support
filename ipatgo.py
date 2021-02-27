import os
import config


def vote(timestamp):
    print('投票中...')
    try:
        return os.system(rf'.\ipatgo\ipatgo.exe file {config.INET_ID} {config.SUBSCRIBER_NUMBER} {config.PIN_NUMBER} {config.P_ARS_NUMBER} .\tickets\ticket_' + timestamp + '.csv')
    except Exception as e:
        print(e.args)
        return 1