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
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
print(channel_secret, channel_access_token)
# https://developers.line.biz/console/channel/1657173822/basics
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)


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
    nums = 1 if event.message.type == "sticker" else text.count('抽')
    print(nums, event.message.type, text)
    image_array = []
    if nums > 5:
        nums = 5
    for i in range(nums):
        home = "1eYqQdaiqKc0A2qriRdX8rtXNbAHWHqD-Th6x5CNM3i0"
        good_luck = "1zspKEeTAQPsrHFpM0sjYotupwrX0JZFR6yi_3NGTTfc"
        googleSheetId = worksheetName = home
        # if random.uniform(0, 1):
        #     googleSheetId = worksheetName = home
        # else:
        #     googleSheetId = worksheetName = good_luck
        URL = 'https://docs.google.com/spreadsheets/d/{0}/gviz/tq?tqx=out:csv&sheet={1}'.format(googleSheetId, worksheetName)
        df = pandas.read_csv(URL)
        image_url_array = df[df.columns[4]].to_numpy()
        image_url = random.choice(image_url_array)
        image_message = ImageSendMessage(original_content_url=image_url, preview_image_url=image_url)    
        image_array.append(image_message)
    line_bot_api.reply_message(reply_token, image_array)


    # line_bot_api.reply_message(reply_token, TextSendMessage(text=text, emojis=emoji))


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0', port=port)