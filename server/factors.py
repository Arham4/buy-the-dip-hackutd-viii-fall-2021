import json
import math
import urllib.request
import certifi

import finnhub

config = json.load(open('config.json', mode='r'))
finnhub_client = finnhub.Client(api_key=config['finnhub_api_key'])

dummy_value = 100
dummy_length = 100
epoch_today = 1636761600

reddit_sentiment = json.load(open('./sentiment/reddit_sentiment.json', mode='r'))
twitter_sentiment = json.load(open('./sentiment/twitter_sentiment.json', mode='r'))


def get_price_values(ticker, from_epoch, to_epoch):
    return finnhub_client.stock_candles(ticker, 'D', from_epoch, to_epoch)['c']


def get_volume_values(ticker, from_epoch, to_epoch):
    return finnhub_client.stock_candles(ticker, 'D', from_epoch, to_epoch)['v']


def get_stock_fear_indices(from_epoch, to_epoch):
    return [dummy_value] * dummy_length


def get_crypto_fear_indices(from_epoch, to_epoch):
    days_between = math.ceil((to_epoch - from_epoch) / 86400)
    fear_index_json = json.loads(
        urllib.request.urlopen('https://api.alternative.me/fng/?limit=' + str(days_between),
                               cafile=certifi.where()).read())
    return list(map(lambda day: int(day['value']), fear_index_json['data']))[::-1]


def get_rsi_indices(ticker, from_epoch, to_epoch):
    rsi_data = finnhub_client.technical_indicator(symbol=ticker, resolution='D', _from=from_epoch, to=to_epoch,
                                                  indicator='rsi', indicator_fields={"timeperiod": 14, })
    rsi_datum = rsi_data['rsi']
    while len(rsi_datum) < dummy_length:
        rsi_datum.insert(0, dummy_value)
    return rsi_datum


def get_macd_indices(ticker, from_epoch, to_epoch):
    macd_data = finnhub_client.technical_indicator(symbol=ticker, resolution='D', _from=from_epoch, to=to_epoch,
                                                   indicator='macd',
                                                   indicator_fields={})
    macd_datum = macd_data['macdSignal']
    while len(macd_datum) < dummy_length:
        macd_datum.insert(0, dummy_value)
    return macd_datum


def get_stochastic_indices(ticker, from_epoch, to_epoch):
    stochastic_data = finnhub_client.technical_indicator(symbol=ticker, resolution='D', _from=from_epoch, to=to_epoch,
                                                         indicator='stoch',
                                                         indicator_fields={"fastkperiod": 14, })
    stochastic_datum = stochastic_data['slowd']
    while len(stochastic_datum) < dummy_length:
        stochastic_datum.insert(0, dummy_value)
    return stochastic_datum


def get_google_trends_values(ticker, from_epoch, to_epoch):
    return [dummy_value] * dummy_length


def get_twitter_values(ticker, from_epoch, to_epoch):
    return twitter_sentiment[ticker]


def get_reddit_values(ticker, from_epoch, to_epoch):
    if ticker not in reddit_sentiment:
        return [dummy_value] * dummy_length
    else:
        return reddit_sentiment[ticker]


def get_volatility_values(ticker, from_epoch, to_epoch):
    return [dummy_value] * dummy_length


def get_market_cap_and_logo(ticker):
    market_cap = finnhub_client.company_profile2(symbol=ticker)
    if 'marketCapitalization' not in market_cap:
        return None, None, None
    return market_cap['marketCapitalization'], market_cap['logo'], market_cap['name']
