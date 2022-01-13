import yfinance as yf
import pandas as pd
import pandas_ta as ta
from discord_webhook import DiscordWebhook
import time

# “1m”, “2m”, “5m”, “15m”, “30m”, “60m”, “90m”, “1h”, “1d”, “5d”, “1wk”, “1mo”, “3mo”

discordURL = "https://discord.com/api/webhooks/931087642039287867/8XRycawHFYaUgFO687-A3DBB-mbBCA4JgQMj2CSo3dhAVBJDnR53AYPD9q1qVSstViDg"

# User input
chartPeriod = "600d"
interval = "1h"
emaLength1 = 400
buys = []
sells = []
inPosition = False
buyPrice = None
sellPrice = None
balance = 10000
percentage = None
leverage = 2

# Market data

prices = []
ema1 = []
df = pd.DataFrame()
df = df.ta.ticker("^VIX", period=chartPeriod, interval=interval)

def talk():
    price(prices, df)
    text = "Starting Vix trading bot with balance: " + str(balance)
    print(text)
    time.sleep(1)
    DiscordWebhook(url=discordURL, content=text).execute()
    text = "Current Vix price " + str(prices[-1])
    print(text)
    time.sleep(1)
    DiscordWebhook(url=discordURL, content=text).execute()
    text = "Current stategy buy vix under ema 400, sell when over ema 400 + 2"
    print(text)
    time.sleep(1)
    DiscordWebhook(url=discordURL, content=text).execute()
    text = "Status: Running..."
    print(text)
    time.sleep(1)
    DiscordWebhook(url=discordURL, content=text).execute()

def price(prices, df):
    df = df.values.tolist()
    for i in range(len(df)):
        prices += [df[i][3]]

def EMA1(ema1, df):
    df = df.ta.ema(length=emaLength1)
    df = df.values.tolist()

    for i in range(len(df)):
        ema1 += [df[i]]


def trade(prices,ema1, buyPrice, sellPrice, balance, percentage, leverage):
    global inPosition
    if not inPosition:
        if prices[-1] < ema1[-1]:
            #buy
            inPosition = True
            buyPrice = prices[-1]
            text = "Bought Vix at: " + str(buyPrice)
            print(text)
            DiscordWebhook(url=discordURL,content=text).execute()
    else:
        if prices[-1] > (ema1[-1] + 2):
            #sell
            inPosition = False
            sellPrice = prices[-1]
            print("Sold ^VIX at: " + str(sellPrice))
            percentage = (sellPrice/buyPrice*100-100)*leverage
            balance += balance*percentage/100
            text = "Gain/loss: " + str(percentage) + " With" + str(leverage) + "x leverage, current balance: " + str(
                balance)
            print(text)
            DiscordWebhook(url=discordURL,content=text).execute()
            text = "-------------------------------------"
            print(text)
            DiscordWebhook(url=discordURL, content=text).execute()

talk()
while True:
    price(prices, df)
    EMA1(ema1, df)
    trade(prices,ema1,buyPrice,sellPrice, balance, percentage, leverage)
