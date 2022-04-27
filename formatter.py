def format(api_response):
	timestamp = []
	volume = []
	close = []
	high = []
	low = []
	open = []
	for i in range(0, len(api_response)):
		timestamp.append(api_response[i][0])
		volume.append(api_response[i][1])
		close.append(api_response[i][2])
		high.append(api_response[i][3])
		low.append(api_response[i][4])
		open.append(api_response[i][5])

	return timestamp, volume, close, high, low, open