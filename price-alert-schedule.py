import requests, pymongo, certifi
from variables import backend_url_dev, backend_url_prod, mongo_string

server = backend_url_prod

myclient = pymongo.MongoClient(mongo_string, tlsCAFile=certifi.where())
mydb = myclient["stockanalyst"]

data_setting = mydb.settings.find_one()

if data_setting['dataInsertionEnable'] == 0:
    print('exiting script')
    exit()

response = requests.get(server + "/api/users/schedulePriceAlertNotification")

if response.status_code == 200:
    print('Success')
else:
    print("Fail")

