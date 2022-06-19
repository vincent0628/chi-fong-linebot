from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import os
import datetime
import random
import pandas

app = Flask(__name__)
# LINE BOT info
# line_bot_api = LineBotApi('Channel Access token')
# handler = WebhookHandler('Channel Secret')
# https://developers.line.biz/console/channel/1657173822/basics
line_bot_api = LineBotApi('uf06g9Y6nQPtl50MIzo0XlNc1bJdBwNsF2EUGYkuDcz3xB5obY/NWmjKymmgS0i8JMHoQ2FXQJwOlsPIcRrFWJoGe5M4upjt0XYc0p6t5D2vcenI9NgRtwqqH8p0TAAjVjz5fmwyW57AR+9UFaGZtQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('b5987f3c74c321166ded1ba352df80f6')


@app.route("/callback", methods=['POST'])
def callback():
    # signature是LINE官方提供用來檢查該訊息是否透過LINE官方APP傳送
    signature = request.headers['X-Line-Signature']
    # body就是用戶傳送的訊息，並且是以JSON的格式傳送
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    print(body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


# Message event
@handler.add(MessageEvent)
def handle_message(event):
    message_type = event.message.type
    user_id = event.source.user_id
    reply_token = event.reply_token
    text = message = event.message.text
    emoji = None
    interval = datetime.datetime.now() - datetime.datetime(2020, 7, 22)
    nums = message.count('抽')
    if event.message.type == "sticker":
        nums = 1
    for i in range(nums):
        print(nums)
        home = "1UZpmCCiUixC8BuWS4qHYAGgG9m3izMg0l0fjJesd7S0"
        good_luck = "1zspKEeTAQPsrHFpM0sjYotupwrX0JZFR6yi_3NGTTfc"
        if random.uniform(0, 1):
            googleSheetId = worksheetName = home
        else:
            googleSheetId = worksheetName = good_luck
        URL = 'https://docs.google.com/spreadsheets/d/{0}/gviz/tq?tqx=out:csv&sheet={1}'.format(googleSheetId, worksheetName)
        df = pandas.read_csv(URL)
        image_url_array = df[df.columns[4]].to_numpy()
        image_url = random.choice(image_url_array)
        image_message = ImageSendMessage(original_content_url=image_url, preview_image_url=image_url)    
        line_bot_api.reply_message(reply_token, image_message)
    return

    # line_bot_api.reply_message(reply_token, TextSendMessage(text=text, emojis=emoji))


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0', port=port)