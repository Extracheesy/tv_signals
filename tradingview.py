import pandas as pd
from tradingview_ta import TA_Handler, Interval
from time import sleep

import config


def build_tv_df_recommendation(lst_symbol):
    df = pd.DataFrame(columns=['symbol', '1h',  '2h', '4h', '1d', 'signal'])
    res = [sub.replace('/', '') for sub in lst_symbol]
    df['symbol'] = res
    df.fillna(-1, inplace=True)
    return df


def get_tradingview_recommendation(lst_symbol):
    df_recommendation = build_tv_df_recommendation(lst_symbol)
    while True:
        for symbol in lst_symbol:
            symbol = symbol.replace('/', '')

            handler = TA_Handler()
            handler.set_symbol_as(symbol)
            handler.set_exchange_as_crypto_or_stock("FTX")
            handler.set_screener_as_crypto()

            for interval in config.LST_INTERVAL:
                try:
                    handler.set_interval_as(interval)
                    df_recommendation.loc[df_recommendation['symbol'] == symbol, interval] = handler.get_analysis().summary["RECOMMENDATION"]
                except:
                    sleep(1)
                    try:
                        handler.set_interval_as(interval)
                        df_recommendation.loc[df_recommendation['symbol'] == symbol, interval] = handler.get_analysis().summary["RECOMMENDATION"]
                    except:
                        print('################## no recommention: ', symbol, ' interval: ', interval)

        df = df_recommendation.copy()
        df.set_index('symbol', inplace=True)
        for symbol in df.index.tolist():
            lst_recom = df.loc[df.index == symbol].values.tolist()[0]
            lst_recom.pop()
            strong_buy_count = lst_recom.count('STRONG_BUY')

            if('SELL' in lst_recom or 'STRONG_SELL' in lst_recom or 'NEUTRAL' in lst_recom):
                df_recommendation.loc[df_recommendation['symbol'] == symbol, 'signal'] = 'SELL'
            else:
                if(strong_buy_count >= 2):
                    df_recommendation.loc[df_recommendation['symbol'] == symbol, 'signal'] = 'BUY'
                else:
                    df_recommendation.loc[df_recommendation['symbol'] == symbol, 'signal'] = 'HOLD'

        symbol_for_sell = "sell signal: "
        symbol_for_hold = "hold signal: "
        symbol_for_buy = "buy signal: "
        for symbol in df_recommendation['symbol'].tolist():
            if df_recommendation.loc[df_recommendation['symbol'] == symbol, 'signal'].iloc[0] == 'SELL':
                symbol_for_sell = symbol_for_sell + symbol + " "
            else:
                if df_recommendation.loc[df_recommendation['symbol'] == symbol, 'signal'].iloc[0] == 'HOLD':
                    symbol_for_hold = symbol_for_hold + symbol + " "
                else:
                    if df_recommendation.loc[df_recommendation['symbol'] == symbol, 'signal'].iloc[0] == 'BUY':
                        symbol_for_buy = symbol_for_buy + symbol + " "

        print(symbol_for_sell)
        print(symbol_for_hold)
        print(symbol_for_buy)


