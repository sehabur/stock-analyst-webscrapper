
import requests

server = "http://localhost:5000"

response  = requests.get(server + "/api/prices/marketDepthAllInst")

if response.status_code == 200:
    # data = response.json()  # Parse the JSON response
    print('Success')
else:
    print("Fail")

