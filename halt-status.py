
import requests, pymongo, datetime, certifi
from variables import backend_url_dev, backend_url_prod, mongo_string

server = backend_url_prod

myclient = pymongo.MongoClient(mongo_string, tlsCAFile=certifi.where())
mydb = myclient["stockanalyst"]

data_setting = mydb.settings.find_one()

if data_setting['dataInsertionEnable'] == 0:
    print('exiting script')
    exit()

response  = requests.get(server + "/api/prices/marketDepthAllInst")
# response  = requests.get(server + "/api/prices/latestPrice")

if response.status_code == 200:
    # data = response.json()  # Parse the JSON response
    # print(data)
    print('Success')
else:
    print("Fail")

