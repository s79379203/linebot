# -*- coding: utf-8 -*-
"""
FWT LineBot小幫手
2022.06.21
"""
#載入LineBot所需要的套件
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import re

app = Flask(__name__)

# 必須放上自己的Channel Access Token
# 20220714 line_bot_api = LineBotApi('7BzW5LqyzXzq+Vp9mP3EWjHGTgmto7ogCBc1QftEcMGkwauHpQ5crcBQbER/BbzeLa4BdmIsd4a/jeqEkxU/K4dTSprIDTMzadRo8JOIa+jdoyeWFxpZRlifWR4SsKhEyCx2JLRGdHHTSULjBFPN8gdB04t89/1O/w1cDnyilFU=')
line_bot_api = LineBotApi('tFQSmjyJiF0D1FBBWedSPZow+6pAQgDbaW7oTyX2VpA9TxR6dUKiJ+6+o/9cfeio+JIxiFMBCMEOFsC/9FTJmd3EMNTUFwx/Ayu7XLXFa8n0DjlVaeENnrj6bhh/OoGiXwjZPEzK+IH7clQJiVSxUAdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
# 20220714 handler = WebhookHandler('e07acd6e4cf0a0c84272962d4aa9ce0f')
handler = WebhookHandler('4e658180396dad03bd7323fcf7815232')
# 主動推播提示資訊: push message (Your user ID, TextSendMessage())
# 20220714 line_bot_api.push_message('U9903430172b3160867439bbc74135845', TextSendMessage(text='FWT小幫手資料已更新. 請輸入小寫fwt開始!'))
line_bot_api.push_message('U53be936e1a490c452cb4e85ac52ae60b', TextSendMessage(text='FWT小幫手已啟動. 請輸入小寫fwt開始!'))

# 監聽所有來自 /callback 的 Post Request
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
# '拆解步驟詳細介紹安裝並使用Anaconda、Python、Spyder、VScode…'
#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = text=event.message.text
    if re.match('fwt',message):
        carousel_template  = CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/oINarLO.png',
                        title='FWT績效',
                        text='接單狀況',
                        actions=[
                            PostbackAction(
                                label='累計接單金額',
                                display_text=data,
                                data='action=接單明細'
                            ),
                            PostbackAction(
                                label='本月接單金額',
                                display_text=datac,
                                data='action=本月接單明細'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/Lr88MTG.png',
                        title='FWT績效',
                        text='OutPut金額',
                        actions=[
                            PostbackAction(
                                label='累計出貨金額',
                                display_text=data2,
                                data='action=累計出貨金額'
                            ),
                            PostbackAction(
                                label='本月出貨金額',
                                display_text=data2c,
                                data='action=本月出貨金額'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://i.imgur.com/oTj2UaK.png',
                        title='FWT績效',
                        text='HRS Input金額',
                        actions=[
                            PostbackAction(
                                label='累計HRS採購金額',
                                display_text=data3,
                                data='action=採購金額'
                            ),
                            PostbackAction(
                                label='本月HRS採購金額',
                                display_text=data3c,
                                data='action=本月採購金額'
                            )
                        ]
                    )
                ]
            )

        # line_bot_api.reply_message(event.reply_token, carousel_template_message)
        template_message = TemplateSendMessage(
        alt_text = 'Carousel alt text', template = carousel_template)

        line_bot_api.reply_message(event.reply_token, template_message)
    else:
        # 20220714 將TextSendMessage(message)改為: 請輸入小寫fwt叫出選單!
        line_bot_api.reply_message(event.reply_token, TextSendMessage('請輸入小寫fwt叫出選單!'))
#主程式

import sqlite3

import os.path

from datetime import date
today = date.today()
# currentdate = today.strftime("%Y/%m/%d") # 取得今天日期
currentyear = str(today.year)
currentmonth = str(today.month)
currentday = str(today.day)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "CustOrders.db")

try:
    # 查詢order
    con = sqlite3.connect(db_path)
    cursor = con.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print(cursor.fetchall()[2])
    # 累計接單金額
    data = '2022年累計接單' + '\n'
    totalamt = 0
    avgamt = 0
    for item in cursor.execute("SELECT * FROM OrdersBySales;"):
        data += item[0]+'˙累計接單:'+ str(round(item[1], ndigits=1)) +'萬 \n'+'月平均:'+str(item[2])+'萬 ' +'\n'
        print(data)
        totalamt += item[1]
        avgamt += item[2]
    data += '總金額:'+ str(round(totalamt, ndigits=1)) +'萬 \n'+'月平均:'+str(round(avgamt,ndigits=1))+'萬 '
    # 本月接單金額
    datac = '2022年本月接單金額:' + '\n'
    totalamtc = 0
    for item in cursor.execute("SELECT * FROM ordercurrentmonth;"):
        datac += item[0] + '˙本月接單:' + str(round(item[1], ndigits=1)) + '萬 \n' + '\n'
        print(datac)
        totalamtc += item[1]
    datac += '總金額:' + str(round(totalamtc, ndigits=1)) + '萬 \n'
    print(datac)
    # 查詢累計output table
    if int(currentday) < 25:
        # 如果日期小於25日, 代表當月成本未結算. 故資料統計至前月底止
        data2 = '2022年1-' + str(int(currentmonth) - 1) + '月出貨' + '\n'+'(本月成本尚未結算)' + '\n'
    else:
        data2 = '2022年1-' + currentmonth + '月出貨' + '\n'
    totalamt2 = 0
    totagpamt = 0
    avgamt2 = 0
    for item in cursor.execute("SELECT * FROM outputbysales"):
        data2 += item[0] + '˙出貨金額:' + str(item[1]) + '萬 \n' + '月平均:' + str(item[2]) + '萬 \n' + '毛利率:' + str(item[5]) + '\n'
        print(data2)
        totalamt2 += item[1]
        totagpamt += item[3]
        avgamt2 += item[2]
    data2 += '總金額:' + str(round(totalamt2, ndigits=1)) + '萬 \n' + '月平均:' + str(round(avgamt2, ndigits=1)) + '萬 \n' + '毛利率:' + str(round(totagpamt / totalamt2, ndigits=2))
    print(data2)
    # 查詢本月output
    data2c = '本月出貨金額:'+'\n'
    totalamt2c = 0
    totagpamtc = 0
    for item in cursor.execute("SELECT * FROM outputcurrentmonth"):
        data2c += item[0] + '˙出貨金額:' + str(item[1]) + '萬 \n' + '毛利額:' + str(item[2]) + '萬 \n' + '毛利率:' + str(
            item[3]) + '\n'
        print(data2c)
        totalamt2c += item[1]
        totagpamtc += item[2]
    data2c += '總金額:' + str(round(totalamt2c, ndigits=1)) + '萬 \n' + '總毛利額:' + str(
        round(totagpamtc, ndigits=1)) + '萬 \n' + '毛利率:' + str(round(totagpamtc / totalamt2c, ndigits=2))
    print(data2c)
    # 查詢input table
    data3 = currentyear+'年'+'累計HRS input/USD:' + '\n'
    totalamt3 = 0
    avgamt3 = 0
    for item in cursor.execute("SELECT * FROM inputbysales"):
        data3 += item[0] + '˙採購金額:' + str(item[1]) + '萬 \n' + '月平均:' + str(item[2]) + '萬 \n'
        print(data3)
        totalamt3 += item[1]
        avgamt3 += item[2]
    data3 += '採購總金額USD:' + str(totalamt3) + '萬 \n' + '月平均USD:' + str(round(avgamt3, ndigits=1)) + '萬 '
    # 查詢本月input
    data3c = currentyear + '年' + '本月HRS input/USD:' + '\n'
    totalamt3c = 0
    for item in cursor.execute("SELECT * FROM inputcurrentmonth"):
        data3c += item[0] + '˙採購金額:' + str(item[1]) + '萬 \n'
        print(data3c)
        totalamt3c += item[1]
    data3c += '採購總金額USD:' + str(round(totalamt3c, ndigits=2)) + '萬 \n'
    print(data3c)
    con.close()
except sqlite3.Error as e:

    print(f"Error {e.args[0]}")

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
