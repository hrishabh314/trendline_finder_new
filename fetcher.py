from __future__ import print_function

import gate_api
from gate_api.exceptions import ApiException, GateApiException

configuration = gate_api.Configuration(
    host = "https://api.gateio.ws/api/v4"
)

api_client = gate_api.ApiClient(configuration)
api_instance = gate_api.SpotApi(api_client)

def fetch(currency_pair, limit, interval):
    try:
        api_response = api_instance.list_candlesticks(currency_pair, limit = limit, interval = interval)
    except GateApiException as ex:
        print("Gate api exception, label: %s, message: %s\n" % (ex.label, ex.message))
    except ApiException as e:
        print("Exception when calling SpotApi->list_candlesticks: %s\n" % e)

    return api_response

if __name__ == "__main__":
    api_response = fetch("BTC_USD", 10)
    print(api_response)