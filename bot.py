import datetime
from parsing_rival import get_info
import telegram
import logging
import os
import sys
import time
import random
from dotenv import load_dotenv
load_dotenv()

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

bot = telegram.Bot(token=os.environ['TELEGRAM_TOKEN'])


def format_message(info):
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    message = (f'<b>{today}</b> \n Описание:\n {info["description"]} \n\n'
               f'<b>{yesterday}</b> \nОписание:\n {info["yesterday_description"]} \n\n'
               f'Разница:\n {info["difference"]} \n\n')
               
    if len(info) > 3:
        message += 'Характеристики:\n'
        for key in info:
            if key == 'description' or key == 'yesterday_description' or key == 'difference':
                continue
            message += f'{key}: {info[key]}\n'
    else: 
        message += 'Характеристики не изменились'
    return message.replace('**', '')


def send_long_message(chat_id, message):
    for i in range(0, len(message), 4096):
        bot.sendMessage(chat_id=chat_id, text=message[i:i+4096], parse_mode=telegram.ParseMode.HTML)
        time.sleep(1)

def send_long_message_to_all(message):
    for chat_id in os.environ['CHAT_IDS'].split(','):
        try:
            send_long_message(chat_id, message)
        except Exception as e:
            logging.error(f'Error while sending message to chat {chat_id} ' + str(e))
            continue

if __name__ == '__main__':
    info = get_info(os.environ['PRODUCT_ID'])
    print(info)
    if info:
        send_long_message_to_all(format_message(info))
