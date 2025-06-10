
import pandas as pd
import numpy as np
from kiteconnect import KiteConnect
from zerodha_login import zerodha_login
from datetime import datetime ,timedelta
import gspread
from google.oauth2.service_account import Credentials

scopes = ["https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
client = gspread.authorize(creds)
workbook = client.open("Stock SIP")

kite=zerodha_login()

holdings = kite.holdings()

holdings_map={
    h["tradingsymbol"]:h["quantity"]*h["average_price"]
    for h in holdings
}

ABCAPITAL={"symbol":"ABCAPITAL","qty":1,"dqty":2,"max_investment":14760}
MOTILALOFS={"symbol":"MOTILALOFS","qty":1,"dqty":1,"max_investment":24000}
JSWENERGY={"symbol":"JSWENERGY","qty":1,"dqty":2,"max_investment":12000}
TATAPOWER={"symbol":"TATAPOWER","qty":1,"dqty":2,"max_investment":12000}
stocks_list=[ABCAPITAL,MOTILALOFS,JSWENERGY,TATAPOWER]

curr_date=datetime.today()
for stock in stocks_list:
    symbol=stock["symbol"]
    stock["holdings"]=holdings_map.get(symbol,0)
    print(symbol)
    
    sheet = workbook.worksheet(symbol)
    stock_sheet_data=sheet.get_all_values()
    
    df=pd.DataFrame(stock_sheet_data[1:],columns=stock_sheet_data[0])
    df["Date"]=pd.to_datetime(df["Date"],format="%m/%d/%Y",errors="coerce")
    df["Close Price"]=pd.to_numeric(df["Close Price"],errors="coerce")
    df = df.dropna(subset=["Close Price"]).sort_values("Date").reset_index(drop=True)
    
    df = df[df["Date"] < curr_date]
    if len(df) < 2:
        print("Not enough data for", symbol)
        continue
    
    previous_price=df.iloc[-1]["Close Price"]
    last_week_price=df.iloc[-2]["Close Price"]
    print(previous_price,last_week_price)
    price_change=(previous_price-last_week_price)/last_week_price*100
    
    if stock["holdings"]<stock["max_investment"]:
        
        if price_change<-2:
            
            qty= stock["dqty"]
        else:
            qty=stock["qty"]
        
        margin=stock["max_investment"]-stock["holdings"]
        qty= min(int(np.floor(margin/previous_price)),qty)
        
        if qty == 0:
            print(f"Not enough margin left to buy {symbol}")
            continue
            
        try:
            
            order_id = kite.place_order(
                variety=kite.VARIETY_REGULAR,
                exchange=kite.EXCHANGE_NSE,
                tradingsymbol=symbol,
                transaction_type=kite.TRANSACTION_TYPE_BUY,
                quantity=qty,
                product=kite.PRODUCT_CNC,
                order_type=kite.ORDER_TYPE_MARKET,
                validity=kite.VALIDITY_DAY )
                
            print(f"Price Change of {price_change} | Order placed for {symbol} | Qty: {qty} | Order ID: {order_id}")
            history = kite.order_history(order_id)
            executed_order = next((entry for entry in reversed(history) if entry["status"] == "COMPLETE"), None)
        
            if executed_order:
                buy_date = executed_order["order_timestamp"]
                executed_price = executed_order["average_price"]
                quantity = executed_order["filled_quantity"]
                total_amount = executed_price * quantity
            
                dt = df.iloc[-1]["Date"]
                previous_date = f"{dt.month}/{dt.day}/{dt.year}"
            
                for row_idx, row in enumerate(stock_sheet_data[1:], start=2):
                
                    if row[0] == previous_date:
            
                        try:
                                                   
                            sheet.update(f"D{row_idx}:G{row_idx}", [[
                                buy_date.strftime("%m/%d/%Y %H:%M:%S"),
                                round(executed_price, 2),
                                quantity,
                                round(total_amount, 2)
                            ]])
                        except Exception as e:
                            print(f"Failed to log data for {symbol}: {e}")
                            
                        
                        break
            

            else:
                print("Market Order not executed yet.")
        
        except Exception as e:
            print(f"Failed to place order for {symbol}: {e}")
        
    else:
        print(f"Max Investment Done for Stock {symbol} of Rs{stock.get('max_investment')}")

