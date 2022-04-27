import pandas as pd
import numpy as np
import mplfinance as mpf
import parameters as pmts
from datetime import datetime

def plot(api_response, coin_name, trendlines, support_extrema, resistance_extrema):
	df = pd.DataFrame(api_response)
	df.columns = ['Time', 'Volume', 'Close', 'High', 'Low', 'Open', 'dummy']
	df['Time'] = [datetime.fromtimestamp(int(df.iloc[i]['Time'])) for i in df.index]
	df = df.set_index('Time')
	df[['Volume', 'Close', 'High', 'Low', 'Open']] = df[['Volume', 'Close', 'High', 'Low', 'Open']].astype(float)

	points_for_trendlines = []
	linestyle = []
	for i, j, yi, yj in trendlines:
		points_for_trendlines.append([(str(df.index[i]), yi), (str(df.index[j]), yj)])
		if j >= pmts.fraction_old_data * len(api_response):
			linestyle.append("dotted")
		else:
			linestyle.append("solid")

	if len(support_extrema) == 0:
		support_extrema.append(0)
	if len(resistance_extrema) == 0:
		resistance_extrema.append(0)
	points_for_support_extrema = [np.nan] * len(api_response)
	for i in support_extrema:
		points_for_support_extrema[i] = float(df.iloc[i]['Low'])
	points_for_resistance_extrema = [np.nan] * len(api_response)
	for i in resistance_extrema:
		points_for_resistance_extrema[i] = float(df.iloc[i]['High'])

	apds = [
			mpf.make_addplot(points_for_support_extrema, type='scatter', markersize=100, marker='^', color = 'g'),
			mpf.make_addplot(points_for_resistance_extrema, type='scatter', markersize=100, marker='v', color = 'r')
			]
	mpf.plot(df,
		alines = dict(alines = points_for_trendlines, linestyle = linestyle),
		type = 'candle', style = 'yahoo', tight_layout = True, figsize = (16*3, 9*3), savefig = "plots/" + coin_name,
		addplot = apds, warn_too_much_data = 5000)




# import pandas as pd
# import mplfinance as mpf
# from datetime import datetime

# def plot(api_response, coin_name, trendlines = None):
# 	df = pd.DataFrame(api_response)
# 	df.columns = ['Time', 'Volume', 'Close', 'High', 'Low', 'Open', 'dummy']
# 	df['Time'] = [datetime.fromtimestamp(int(df.iloc[i]['Time'])) for i in df.index]
# 	df = df.set_index('Time')
# 	df[['Volume', 'Close', 'High', 'Low', 'Open']] = df[['Volume', 'Close', 'High', 'Low', 'Open']].astype(float)

# 	if trendlines:
# 		points_for_trendlines = []
# 		linestyle = []
# 		for i, j, yi, yj in trendlines:
# 			points_for_trendlines.append([(str(df.index[i]), yi), (str(df.index[j]), yj)])
# 			if j >= 700:
# 				linestyle.append("dotted")
# 			else:
# 				linestyle.append("solid")

# 		mpf.plot(df,
# 			alines = dict(alines = points_for_trendlines, linestyle = linestyle),
# 			type = 'candle', style = 'yahoo', tight_layout = True, figsize = (16*3, 9*3), savefig = "plots/" + coin_name)
# 	else:
# 		mpf.plot(df,
# 			type = 'candle', style = 'yahoo', figsize = (32, 18), savefig = coin_name)