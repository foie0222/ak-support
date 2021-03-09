import os
import config


def vote(timestamp, number):
    print('投票中...')
    try:
        return os.system(rf'.\ipatgo\ipatgo.exe file {config.IPATS[number].INET_ID} {config.IPATS[number].SUBSCRIBER_NUMBER} {config.IPATS[number].PIN_NUMBER} {config.IPATS[number].P_ARS_NUMBER} .\tickets\ticket_' + timestamp + f'_{number}.csv')
    except Exception as e:
        print(e.args)
        return 1