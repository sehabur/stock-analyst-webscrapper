
import requests
from variables import backend_url_dev, backend_url_prod

server = backend_url_prod

response  = requests.get(server + "/api/users/schedulePriceAlertNotification")

if response.status_code == 200:
    # data = response.json()  # Parse the JSON response
    # print(data)
    print('Success')
else:
    print("Fail")

