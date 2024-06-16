from telethon import TelegramClient, events
import requests
import os

# Укажите ваш API ID и API Hash, которые вы получили от Telegram
api_id = '22705099'
api_hash = '7caba79297a8910f8f19e22cbc259b44'
bot_token = '7322531202:AAG9Oe2qgWhcEn0j5CXzINoWsZw7xtjlNrU'

client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.reply('Привет! Отправь мне изображение, и я удалю его фон.')

@client.on(events.NewMessage)
async def handle_message(event):
    if event.photo:
        photo = await event.download_media()
        await event.reply('Изображение получено, удаляю фон...')
        new_photo = remove_background(photo)
        if new_photo:
            await client.send_file(event.chat_id, new_photo, caption='Вот ваше изображение без фона.')
            os.remove(new_photo)  # Удаляем временный файл
        else:
            await event.reply('Произошла ошибка при обработке изображения.')

def remove_background(file_path):
    # Используем API remove.bg для удаления фона
    api_key = 'ZKSNQrMpSCpot5bQsHqzEnAs'
    response = requests.post(
        'https://api.remove.bg/v1.0/removebg',
        files={'image_file': open(file_path, 'rb')},
        data={'size': 'auto'},
        headers={'X-Api-Key': api_key}
    )

    if response.status_code == requests.codes.ok:
        output_path = 'no_bg_' + os.path.basename(file_path)
        with open(output_path, 'wb') as out_file:
            out_file.write(response.content)
        return output_path
    else:
        print('Error:', response.status_code, response.text)
        return None

client.start()
client.run_until_disconnected()
