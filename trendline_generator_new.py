import parameters as pmts

import numpy as np
from sortedcontainers import SortedList

def get_support_trendlines(close, high, low, open, limit):
	close = np.array([float(i) for i in close])
	high = np.array([float(i) for i in high])
	low = np.array([float(i) for i in low])
	open = np.array([float(i) for i in open])

	avg = sum(close[0 : pmts.ma_duration]) / pmts.ma_duration
	sm = 0
	for i in range(pmts.ma_duration, len(close)):
		sm = sm + (close[i] - avg) ** 2
		avg = (avg * pmts.ma_duration - close[i - pmts.ma_duration] + close[i]) / pmts.ma_duration;
	std_deviation = (sm / (limit - pmts.ma_duration)) ** 0.5
	dy = pmts.touch_tolerance_factor * std_deviation

	trendlines = list()
	extrema = list()
	end_for_candle = dict()
	end_for_candle_b4_live = dict()

	for j in range(len(close)):
		lb = max(0, j - pmts.extrema_window)
		ub = min(len(close), j + pmts.extrema_window + 1)
		if min(low[lb : ub]) != low[j]:
			continue
		extrema.append(j)
		covered_extrema = dict()
		for ii in range(len(extrema)):
			i = extrema[ii]
			if i == j:
				break
			if covered_extrema.get(i,False):
				continue
			y0 = low[i] - dy
			y1 = low[i] + dy
			slope = (low[j] - low[i]) / (j - i)
			current_extrema = list()
			breakouts = 0
			for kk in range(ii, len(extrema)):
				k = extrema[kk]
				if y0 + (k - i) * slope <= low[k] and low[k] <= y1 + (k - i) * slope:
					current_extrema.append(k)
				if y0 + (k - i) * slope > low[k]:
					breakouts = breakouts + 1
			if breakouts <= (j - i + 1) * pmts.breakout_tolerance_factor and len(current_extrema) >= pmts.touch_requirement:
				if j < limit * pmts.fraction_old_data:
					end_for_candle_b4_live[i] = j
				if j >= limit * pmts.fraction_old_data:
					if end_for_candle_b4_live.get(i, -1) != -1 and end_for_candle_b4_live[i] not in current_extrema:
						del end_for_candle_b4_live[i]

				end_for_candle[i] = j
				for k in current_extrema:
					covered_extrema[k] = True

	for i, j in end_for_candle.items():
		# trendlines.append((i, j, low[i] - dy, low[j] - dy));
		# trendlines.append((i, j, low[i] + dy, low[j] + dy));
		if (j < limit * pmts.fraction_old_data):
			trendlines.append((i, j, low[i], low[j]));
		else:
			if end_for_candle_b4_live.get(i, -1) != -1:
				x0 = i
				y0 = low[i]

				x2 = j
				y2 = low[j]

				slope = (y2 - y0) / (x2 - x0)

				x1 = end_for_candle_b4_live[i]
				y1 = y0 + slope * (x1 - x0)
				trendlines.append((x0, x1, y0, y1))
				trendlines.append((x1, x2, y1, y2))
			else:
				trendlines.append((i, j, low[i], low[j]));


	return trendlines, extrema


def get_resistance_trendlines(close, high, low, open, limit):
	close = np.array([float(i) for i in close])
	high = np.array([float(i) for i in high])
	low = np.array([float(i) for i in low])
	open = np.array([float(i) for i in open])

	avg = sum(close[0 : pmts.ma_duration]) / pmts.ma_duration
	sm = 0
	for i in range(pmts.ma_duration, len(close)):
		sm = sm + (close[i] - avg) ** 2
		avg = (avg * pmts.ma_duration - close[i - pmts.ma_duration] + close[i]) / pmts.ma_duration;
	std_deviation = (sm / (limit - pmts.ma_duration)) ** 0.5
	dy = pmts.touch_tolerance_factor * std_deviation

	trendlines = list()
	extrema = list()
	end_for_candle = dict()
	end_for_candle_b4_live = dict()

	for j in range(len(close)):
		lb = max(0, j - pmts.extrema_window)
		ub = min(len(close), j + pmts.extrema_window + 1)
		if max(high[lb : ub]) != high[j]:
			continue
		extrema.append(j)
		covered_extrema = dict()
		for ii in range(len(extrema)):
			i = extrema[ii]
			if i == j:
				break
			if covered_extrema.get(i, False):
				continue
			y0 = high[i] - dy
			y1 = high[i] + dy
			slope = (high[j] - high[i]) / (j - i)
			current_extrema = list()
			breakouts = 0
			for kk in range(ii, len(extrema)):
				k = extrema[kk]
				if y0 + (k - i) * slope <= high[k] and high[k] <= y1 + (k - i) * slope:
					current_extrema.append(k)
				if y1 + (k - i) * slope < high[k]:
					breakouts = breakouts + 1
			if breakouts <= (j - i + 1) * pmts.breakout_tolerance_factor and len(current_extrema) >= pmts.touch_requirement:
				if j < limit * pmts.fraction_old_data:
					end_for_candle_b4_live[i] = j
				if j >= limit * pmts.fraction_old_data:
					if end_for_candle_b4_live.get(i, -1) != -1 and end_for_candle_b4_live[i] not in current_extrema:
						del end_for_candle_b4_live[i]

				end_for_candle[i] = j
				for k in current_extrema:
					covered_extrema[k] = True

	for i, j in end_for_candle.items():
		# trendlines.append((i, j, low[i] - dy, low[j] - dy));
		# trendlines.append((i, j, low[i] + dy, low[j] + dy));
		if (j < limit * pmts.fraction_old_data):
			trendlines.append((i, j, high[i], high[j]));
		else:
			if end_for_candle_b4_live.get(i, -1) != -1:
				x0 = i
				y0 = high[i]

				x2 = j
				y2 = high[j]

				slope = (y2 - y0) / (x2 - x0)

				x1 = end_for_candle_b4_live[i]
				y1 = y0 + slope * (x1 - x0)
				trendlines.append((x0, x1, y0, y1))
				trendlines.append((x1, x2, y1, y2))
			else:
				trendlines.append((i, j, high[i], high[j]));


	return trendlines, extrema