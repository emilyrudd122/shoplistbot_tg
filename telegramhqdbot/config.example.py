from enum import Enum

TOKEN = 'telegramtoken'
qiwi_token = 'qiwitoken'
phone_number = 'phonenumber'
db_file = 'database.vdb'


class States(Enum):
    S_START = "0"
    S_NEED_AUTH = "1"
    S_DEFAULT = "2"
    S_TOVARI = "3"
    S_KUPIT = "4"
    S_BALANCE = "5"
    S_ABOUT = "6"