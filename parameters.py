# how much candles can breakout from a trendline for the trendline to be considered valid
# 0 tolerance is ideal
breakout_tolerance_factor = 0

# size of rolling mean needed to calculate standard deviation from which dy is calculated
ma_duration = 20

# what fraction of standard deviation is dy
touch_tolerance_factor = 0.08

# how many touches to valid trendline
touch_requirement = 4

# number of candles to left and right of of any extrema, hence, window size = 2 * 9 + 1 = 19
extrema_window = 9

# fraction of limit (no. of data points) taken as previously available
fraction_old_data = 0.8