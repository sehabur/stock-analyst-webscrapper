import pymongo, certifi
from datetime import datetime, timedelta
from variables import mongo_string, db_name

myclient = pymongo.MongoClient(mongo_string, tlsCAFile=certifi.where())
mydb = myclient[db_name]

data_setting = mydb.settings.find_one()

if data_setting['dataInsertionEnable'] == 0:
    print('Exiting script')
    exit()

# adjust days in 2nd element of array #
collection_items = [
   ["minute_prices", 45],
   ["index_minute_values", 180],
   ["yesterday_prices", 5],
]

output_text = ""

for col_item in collection_items:
  coll = col_item[0]
  last_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days = col_item[1])

  result = mydb[coll].delete_many({ "date": { "$lt": last_date } })

  output_text += f"{coll}: {result.deleted_count}; "

  # print("col:", coll, "|", "last_date:", last_date, "|", "documents_deleted:", result.deleted_count,)

mydb.data_script_logs.insert_one({
  'script': 'db-parse-daily',
  'message': output_text.strip("; "),
  'time': datetime.now()
})  

myclient.close()