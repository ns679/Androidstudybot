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
         Mysession.read_context(user_id) == "4" or
         Mysession.read_context(user_id) == "5" or
         Mysession.read_context(user_id) == "6" or
         Mysession.read_context(user_id) == "7" or
         Mysession.read_context(user_id) == "9" or
         Mysession.read_context(user_id) == "10"or
         Mysession.read_context(user_id) == "11"or
         Mysession.read_context(user_id) == "12"or
         Mysession.read_context(user_id) == "17") and
            text == "中止"):
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage("最初からやり直します。"),
            )
        # 現在のstatusを消して新規statusで初期化。
            Mysession.reset(user_id)
    if Mysession.read_context(user_id) == "0": #「勉強」、「検索」の選択
        if "勉強" in text or "開発" in text or "作成" in text:
            line_bot_api.reply_message(
                event.reply_token,
                [TextSendMessage("どういったアプリを作成したいですか？"),TextSendMessage("簡単なアプリを作成したいのであれば「基本」\n難しいアプリを作成したいのであれば「応用」 \nと入力してください。"),
                 TextSendMessage("各コースの質問についても答えます。\n例：製作時間どのくらいかかるか、どういったアプリを作成するのか等")]
            )
            Mysession.update_context(user_id, "1")
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage("勉強を行う場合は「勉強」と入力してください。")
            )
    elif Mysession.read_context(user_id) == "1": #勉強で行うアプリの選択

        if "基本" in text or "簡単" in text or "難しくない" in text:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage("※ここからは「はい」か\n「いいえ」で答えてください。\nでは基本コースにしますか？")
            )
            Mysession.update_context(user_id,"2")

        elif "応用" in text or "難しい" in text:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage("※ここからは「はい」か\n「いいえ」で答えてください。\nでは応用コースにしますか?")
            )
            Mysession.update_context(user_id,"9")

        elif "詳細" in text or "説明" in text or "作れ" in text or "作成" in text or "どんな" in text or "どういった" in text:
            line_bot_api.reply_message(
                event.reply_token,
                [TextSendMessage("基本コースは画面遷移を用いたアプリ開発\n応用コースは画面遷移に加えて\nローカルデータベース、非同期処理\nを用いたアプリ開発を行います。"),
                 TextSendMessage("使用言語はKotlinです。\nJavaに似た言語です。")]
            )

        elif ("基本" in text and "どういった" in text) or ("基本" in text and "どんな" in text) or ("基本" in text and "詳細" in text):
            line_bot_api.reply_message(
                event.reply_token,
                [TextSendMessage("基本コースは画面遷移を用いた\nアプリ開発を行います。"),
                 TextSendMessage("使用言語はKotlinです。\nJavaに似た言語です。")]
            )

        elif ("応用" in text and "どういった" in text) or ("応用" in text and "どんな" in text) or ("応用" in text and "詳細" in text):
            line_bot_api.reply_message(
                event.reply_token,
                [TextSendMessage("応用コースは画面遷移に加えて\nローカルデータベース、非同期処理\nを用いたアプリ開発を行います。"),
                 TextSendMessage("使用言語はKotlinです。\nJavaに似た言語です。")]
            )

        elif "時間" in text or "勉強時間" in text or "どのくらい" in text:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage("基本コースは5～10時間程度\n応用コースは10～15時間程度で\n作成できます。")
            )

        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage("簡単なアプリを作成したいのであれば「基本」\n難しいアプリを作成したいのであれば「応用」\nと入力してください。")
            )

    elif Mysession.read_context(user_id) == "2": #学内案内アプリについての質問
        if text == "はい":
            line_bot_api.reply_message(
                event.reply_token,
                [TextSendMessage("基本コースでは\n学内案内アプリを作成してもらいます。"),TextSendMessage("あなたはKotlinについて学習した経験はありますか？")]
            )
            Mysession.update_context(user_id, "3")
        else:
            line_bot_api.reply_message(
                event.reply_token,
                [TextSendMessage("もう一度入力してください。"),TextSendMessage("どういったアプリを作成したいですか？")]
            )
            Mysession.update_context(user_id, "1")

    elif Mysession.read_context(user_id) == "3": #質問結果による分岐
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

    elif Mysession.read_context(user_id) == "4": #Kotlin基礎のサイト出力(学内案内アプリ)
        line_bot_api.reply_message(
            event.reply_token,
            [TextSendMessage("https://sukkiri.jp/technologies/ides/intellij-idea/intellij-idea-win.html"),TextSendMessage("https://developer.android.com/studio/install?hl=ja"),
             TextSendMessage("https://qiita.com/SYABU555/items/25b1e81a2437d6a2559f"),TextSendMessage("https://www.programming-fun.net/article/article_133.html\n1~5,11~14の単元を勉強"),
             TextSendMessage("https://qiita.com/k-ysd/items/4efdecdfd60afe333a3a\n前編～中編まで勉強")]
        )
        Mysession.update_context(user_id, "5")

    elif Mysession.read_context(user_id) == "5": #画面遷移のサイト出力(学内案内アプリ)
        line_bot_api.reply_message(
            event.reply_token,
            [TextSendMessage("https://qiita.com/naoi/items/8384561d30111c8704b3"),TextSendMessage("https://developer.android.com/codelabs/android-navigation?hl=ja#0"),
             TextSendMessage("理解できたと感じたら、アプリの実装を行うので\n「実装」と入力してください。")]
        )
        Mysession.update_context(user_id, "6")

    elif Mysession.read_context(user_id) == "6":
        line_bot_api.reply_message(
            event.reply_token,
            [TextSendMessage("アプリの実装を行います。\n以下のリンクをクリックして実装を行ってください。"),TextSendMessage("https://docs.google.com/presentation/d/1iCHvT8svrE-omj0UlgG-HuNqCCNgSEStdGh5VIGblEI/edit?usp=sharing"),
             TextSendMessage("終了したらテストを行うので\n「テスト」と入力してください。")]
        )
        Mysession.update_context(user_id,"7")

    elif Mysession.read_context(user_id) == "7": #テストのURL出力
        line_bot_api.reply_message(
            event.reply_token,
            [TextSendMessage("理解度テストを行います。\n下記のテストとアンケートを行ってください。"),TextSendMessage("テスト\nhttps://forms.gle/fqVhgFJaAhHimqtQ9"),
             TextSendMessage("アンケート\nhttps://forms.gle/UoTNxxCP2bpa1a6ZA")]
        )
        Mysession.update_context(user_id,"8")

    elif Mysession.read_context(user_id) == "8": #学内案内アプリの終了表示
        if text == "Xtrfi8j":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage("学内案内アプリの勉強を終了します。\nお疲れ様でした。")
            )
            Mysession.reset(user_id)

    elif Mysession.read_context(user_id) == "9": #メモアプリについての質問
        if text == "はい":
            line_bot_api.reply_message(
                event.reply_token,
                [TextSendMessage("応用コースでは\nメモアプリを作成してもらいます。"),TextSendMessage("あなたはKotlinについて学習した経験はありますか？")]
            )
            Mysession.update_context(user_id, "10")
        else:
            line_bot_api.reply_message(
                event.reply_token,
                [TextSendMessage("もう一度入力してください。"),TextSendMessage("どういったアプリを作成したいですか？")]
            )
            Mysession.update_context(user_id, "1")

    elif Mysession.read_context(user_id) == "10": #質問結果による分岐(メモ１）
        if text == "はい":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage("あなたは画面遷移について学習した経験はありますか？")
            )

            Mysession.update_context(user_id, "11")
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage("Kotlinの基礎の勉強から始めてもらいます。\nKotlin基礎と入力してください。\nKotlin基礎が終わったら画面遷移と入力してください。")
            )
            Mysession.update_context(user_id, "13")

    elif Mysession.read_context(user_id) == "11":#質問結果による分岐（メモ２）
        if text == "はい":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage("あなたはローカルデータベースを構築した経験はありますか？")
            )
            Mysession.update_context(user_id,"12")
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage("画面遷移の勉強から始めてもらいます。\n画面遷移と入力してください。")
            )
            Mysession.update_context(user_id,"14")

    elif Mysession.read_context(user_id)=="12":#質問結果による分岐（メモ３）
        if text == "はい":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage("非同期処理から勉強してもらいます。\n非同期処理と入力してください。")
            )
            Mysession.update_context(user_id,"16")
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage("ローカルデータベース構築から勉強してもらいます。\nローカルデータベースと入力してください。")
            )
            Mysession.update_context(user_id,"15")

    elif Mysession.read_context(user_id)=="13":#メモアプリ版Kotlin基礎
        line_bot_api.reply_message(
            event.reply_token,
            [TextSendMessage("https://sukkiri.jp/technologies/ides/intellij-idea/intellij-idea-win.html"),
             TextSendMessage("https://developer.android.com/studio/install?hl=ja"),
             TextSendMessage("https://qiita.com/SYABU555/items/25b1e81a2437d6a2559f"),
             TextSendMessage("https://www.programming-fun.net/article/article_133.html\n1~5,11~14の単元を勉強"),
             TextSendMessage("https://qiita.com/k-ysd/items/4efdecdfd60afe333a3a\n前編～中編まで勉強")]
        )
        Mysession.update_context(user_id,"14")

    elif Mysession.read_context(user_id) == "14":#メモアプリ版画面遷移
        line_bot_api.reply_message(
            event.reply_token,
            [TextSendMessage("https://qiita.com/naoi/items/8384561d30111c8704b3"),
             TextSendMessage("https://developer.android.com/codelabs/android-navigation?hl=ja#0"),
             TextSendMessage("画面遷移が終わったら\nローカルデータベースと入力してください。")]
        )
        Mysession.update_context(user_id, "15")

    elif Mysession.read_context(user_id) == "15":#ローカルデータベース勉強サイト提供
        line_bot_api.reply_message(
            event.reply_token,
            [TextSendMessage("https://qiita.com/yukiyamadajp/items/73bffb6a3697cb62f9e1"),
             TextSendMessage("https://qiita.com/iTakahiro/items/7e0d63140ae4dac10d18"),
             TextSendMessage("https://developer.android.com/training/data-storage/room?hl=ja"),
             TextSendMessage("ローカルデータベースが終わったら\n非同期処理と入力してください。")]
        )
        Mysession.update_context(user_id,"16")

    elif Mysession.read_context(user_id) == "16":#非同期処理
        line_bot_api.reply_message(
            event.reply_token,
            [TextSendMessage("https://qiita.com/takahirom/items/3e0b7009d2e050e0e56c"),
             TextSendMessage("https://developer.android.com/kotlin/coroutines?hl=ja"),
             TextSendMessage("以上のサイトを用いて\nある程度知識が身に付いたら\n実装を行うので「実装」と入力してください。")]
        )
        Mysession.update_context(user_id,"17")

    elif Mysession.read_context(user_id) == "17":#メモアプリ実装
        line_bot_api.reply_message(
            event.reply_token,
            [TextSendMessage("アプリの実装を行います。\n以下のリンクをクリックして実装を行ってください。"),
             TextSendMessage("https://docs.google.com/presentation/d/1sC864a8PE51P_Vj7tfBwYITCXCORfHxXHR8yI5YdUY0/edit?usp=sharing"),
             TextSendMessage("https://docs.google.com/presentation/d/1MJz5t8Ti6bjsm_H0Ukud0DzXGOW8xws8smGYdWhve7w/edit?usp=sharing"),
             TextSendMessage("終了したらテストを行うので\n「テスト」と入力してください。")]
        )
        Mysession.update_context(user_id,"18")

    elif Mysession.read_context(user_id) == "18":
        line_bot_api.reply_message(
            event.reply_token,
            [TextSendMessage("理解度テストを行います。\n下記のテストとアンケートを行ってください。"),
             TextSendMessage("https://forms.gle/VPC96fYoeLBYETKx7"),
             TextSendMessage("https://forms.gle/23zfj2dGVHJiStJ4A")]
        )
        Mysession.update_context(user_id,"19")

    elif Mysession.read_context(user_id) == "19":
        if text == "Rkgijf03jt":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage("学内案内アプリの勉強を終了します。\nお疲れ様でした。")
            )
        Mysession.reset(user_id)





    # line_bot_api.reply_message(
    #     event.reply_token,
    #     TextSendMessage(text=event.message.text))

if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)