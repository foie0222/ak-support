import os

from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
NETKEIBA_LOGIN_ID = os.getenv('NETKEIBA_LOGIN_ID')
NETKEIBA_LOGIN_PASSWORD = os.getenv('NETKEIBA_LOGIN_PASSWORD')
IPATS = [{"INET_ID": os.getenv('INET_ID1'), "SUBSCRIBER_NUMBER": os.getenv('SUBSCRIBER_NUMBER1'),
          "PIN_NUMBER": os.getenv('PIN_NUMBER1'), "P_ARS_NUMBER": os.getenv('P_ARS_NUMBER1')},
         {"INET_ID": os.getenv('INET_ID2'), "SUBSCRIBER_NUMBER": os.getenv('SUBSCRIBER_NUMBER2'),
          "PIN_NUMBER": os.getenv('PIN_NUMBER2'), "P_ARS_NUMBER": os.getenv('P_ARS_NUMBER2')}
         ]
