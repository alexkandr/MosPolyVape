import os
import asyncio
import logging
from aiogram import Bot

logging.basicConfig(format=u'%(filename)s [ LINE:%(lineno)+3s ]#%(levelname)+8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG)

bot = Bot(token=open('tokens.txt', 'r').readline().strip())

BASE_MEDIA_PATH = './source'


async def uploadMediaFiles(folder, method, file_attr):
    folder_path = os.path.join(BASE_MEDIA_PATH, folder)
    for filename in os.listdir(folder_path):
        if filename.startswith('.'):
            continue

        logging.info(f'Started processing {filename}')
        with open(os.path.join(folder_path, filename), 'rb') as file:
            msg = await method(MY_ID, file, disable_notification=True)
            if file_attr == 'photo':
                file_id = msg.photo[-1].file_id
            else:
                file_id = getattr(msg, file_attr).file_id

            print(filename, file_id, sep='  fileid  ')

loop = asyncio.get_event_loop()

tasks = [
    loop.create_task(uploadMediaFiles('img', bot.send_photo, 'photo')),
]

wait_tasks = asyncio.wait(tasks)

loop.run_until_complete(wait_tasks)
loop.close()
Session.remove()