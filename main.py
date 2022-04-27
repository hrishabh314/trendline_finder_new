import fetcher
import formatter
import trendline_generator_new
import plotter
import os
import shutil
from datetime import datetime

path = 'Plots'
if os.path.exists(path):
	shutil.rmtree(path)
os.makedirs(path)

coin_names = ["BTC_USDT", "MANA_USDT", "DOGE_USDT", "AVAX_USDT", "MATIC_USDT", "XRP_USDT", "LTC_USDT", "ADA_USDT", "SOL_USDT", "DOT_USDT"]
# coin_names = ["BTC_USDT"]

limit = 1000

time_start = datetime.now()

for coin_name in coin_names:
	api_response = fetcher.fetch(coin_name, limit = limit, interval = "4h")

	timestamp, volume, close, high, low, open = formatter.format(api_response)

	support_trendlines, support_extrema = trendline_generator_new.get_support_trendlines(close, high, low, open, limit)
	resistance_trendlines, resistance_extrema = trendline_generator_new.get_resistance_trendlines(close, high, low, open, limit)
	trendlines = support_trendlines + resistance_trendlines

	print(sorted(support_trendlines))
	print(sorted(resistance_trendlines))
	print(coin_name)
	print()

	plotter.plot(api_response = api_response, coin_name = coin_name, trendlines = trendlines, support_extrema = support_extrema, resistance_extrema = resistance_extrema)

time_delta = datetime.now() - time_start
print(time_delta)