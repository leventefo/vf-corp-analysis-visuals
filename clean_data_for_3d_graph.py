import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta, date

def get_next_weekday(ser):

    return ser.map(lambda x: x + timedelta(days=2)
            if x.dayofweek == 5 
            else x + timedelta(days=1) if x.dayofweek == 6
            else x)

def read_data_setup():
    df_VFC_close_price = pd.DataFrame()
    df_NI = pd.read_csv("NetIncomeData.csv")
    df_NI.drop(columns = ["Unnamed: 0"], inplace=True)
    df_NI["end"] = pd.to_datetime(df_NI["end"])
    df_NI["end"] = get_next_weekday(df_NI["end"])
    data = yf.download("VFC", start = df_NI.iloc[2]["end"] - timedelta(days = 10), end = df_NI.iloc[-1]["end"] + timedelta(days=10), auto_adjust=True)
    df_VFC_close_price["Close"] = data["Close"]
    df_VFC_close_price = df_VFC_close_price.reset_index()
    df_NI.rename(columns = {"end":"Date"}, inplace=True)
    df_VFC_NetIncome_Loss_Stock_Price = df_NI.merge(right = df_VFC_close_price, how = "left", on = "Date")
    df_VFC_NetIncome_Loss_Stock_Price.to_csv("VF_net_income_stock_price_new.csv")

read_data_setup()