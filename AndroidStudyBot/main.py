from flask import Flask,request,abort
import os

from linebot import (LineBotApi,WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage,)

class Status:
    def __init__(self):
        self.context = "0"

    def get_context(self):
        return self.context

    def set_context(self, context):
        self.context = context


class Mysession:
    _status_map = dict()

    def register(user_id):
        if Mysession._get_status(user_id) is None:
            Mysession._put_status(user_id, Status())

    def reset(user_id):
        Mysession._put_status(user_id, Status())

    def _get_status(user_id):
        return Mysession._status_map.get(user_id)

    def _put_status(user_id,status: Status):
        Mysession._status_map[user_id] = status

    def read_context(user_id):
        return Mysession._status_map.get(user_id).get_context()

    def update_context(user_id, context):
        new_status = Mysession._status_map.get(user_id)
        new_status.set_context(context)
        Mysession._status_map[user_id] = new_status


app = Flask(__name__)

YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api: LineBotApi = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

@app.route("/")
def hello_world():
    return "hello world!"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event: MessageEvent):
    text = event.message.text
    user_id = event.source.user_id

    Mysession.register(user_id)
    if ((Mysession.read_context(user_id) == "1" or
         Mysession.read_context(user_id) == "2" or
         Mysession.read_context(user_id) == "3" or
         Mysession.read_context(user_id) == "4") and
            text == "中止"):
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage("最初からやり直します。"),
            )
        # 現在のstatusを消して新規statusで初期化。
            Mysession.reset(user_id)
    if Mysession.read_context(user_id) == "0":
        if text == "勉強":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage("どういったアプリを作成したいですか？")
            )
            Mysession.update_context(user_id, "1")
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage("勉強を行う場合は「勉強」と入力してください。")
            )
    elif Mysession.read_context(user_id) == "1":
        if text == "基本":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage("※ここからは「はい」か\n「いいえ」で答えてください。\nでは学内案内アプリを作成しますか？")
            )
            Mysession.update_context(user_id,"2")
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage("簡単なアプリを作成したいのであれば「基本」と入力してください。")
            )

    elif Mysession.read_context(user_id) == "2":
        if text == "はい":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage("あなたはKotlinについて学習した経験はありますか？")
            )
            Mysession.update_context(user_id, "3")
        else:
            line_bot_api.reply_message(
                event.reply_token,
                [TextSendMessage("もう一度入力してください。"),TextSendMessage("どういったアプリを作成したいですか？")]
            )
            Mysession.update_context(user_id, "1")

    elif Mysession.read_context(user_id) == "3":
        if text == "はい":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage("画面遷移の勉強から始めてもらいます。\n画面遷移と入力してください。")
            )

            Mysession.update_context(user_id, "5")
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage("Kotlinの基礎の勉強から始めてもらいます。\nKotlin基礎と入力してください。\nKotlin基礎が終わったら画面遷移と入力してください。")
            )
            Mysession.update_context(user_id, "4")

    elif Mysession.read_context(user_id) == "4":
        line_bot_api.reply_message(
            event.reply_token,
            [TextSendMessage("https://sukkiri.jp/technologies/ides/intellij-idea/intellij-idea-win.html"),TextSendMessage("https://developer.android.com/studio/install?hl=ja"),
             TextSendMessage("https://qiita.com/SYABU555/items/25b1e81a2437d6a2559f"),TextSendMessage("https://www.programming-fun.net/article/article_133.html\n1~5,11~14の単元を勉強"),
             TextSendMessage("https://qiita.com/k-ysd/items/4efdecdfd60afe333a3a\n前編～中編まで勉強")]
        )
        Mysession.update_context(user_id, "5")

    elif Mysession.read_context(user_id) == "5":
        line_bot_api.reply_message(
            event.reply_token,
            [TextSendMessage("https://qiita.com/naoi/items/8384561d30111c8704b3"),TextSendMessage("https://developer.android.com/codelabs/android-navigation?hl=ja#0")]
        )
        Mysession.update_context(user_id, "0")
    # line_bot_api.reply_message(
    #     event.reply_token,
    #     TextSendMessage(text=event.message.text))

if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)