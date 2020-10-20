from SimpleQIWI import *
from time import sleep
import telegramhqdbot.config as config

token = config.qiwi_token         # https://qiwi.com/api
phone = config.phone_number

api = QApi(token=token, phone=phone)
# price = 1
# comment = api.bill(price)

# print("Pay %i rub for %s with comment '%s'" % (price, phone, comment))


@api.bind_echo()            # Создаем эхо-функцию.  Она будет вызываться при каждом новом полученном платеже. В качестве аргументов ей
                            # передаётся информация о платеже. 
def foo(bar):
    print("New payment!")
    print(bar)             
    api.stop()

api.start()