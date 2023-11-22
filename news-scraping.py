import pymongo, certifi, datetime, re
from data import stocks_list_details
from variables import mongo_string

myclient = pymongo.MongoClient(mongo_string, tlsCAFile=certifi.where())

mydb = myclient["stockanalyst"]

today_date = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

news_list = mydb.news.find({
    # 'date': today_date,
    'title': { '$regex': 'Financials' } ,
    'description': { '$regex': 'Un-audited\\): Consolidated EPS was' } 
})

for  news in news_list:
  q = re.split(" ", news['title'])[1].lower()
  code = re.split(" ", news['title'])[0].replace(":", "")
  description = re.split(" ", news['description'])

  # print (news['title'], news['description'])

  filtered_list = [e for e in stocks_list_details if e['tradingCode'] == code]
  yearEnd = filtered_list[0]['yearEnd']

  # EPS #
  for i in range (len(description)):
    if "EPS" == description [i] and "was" == description [i+1] :
      for j in range (i+2, len(description)):
        if description [j] == 'Tk.':
          n=j+1
          break
      break  
  eps_string = description [n]

  if ("(" in eps_string):
    eps = - float(eps_string.strip('()'))
  else:
    eps = float(eps_string) 

  # YEAR #  
  if (yearEnd == '30-Jun'):
    if (q == 'q1' or q == 'q2'):
      year = int(description [n+3]) + 1
    else:
      year = description [n+3]
  else:
    year = description [n+3]

  # NOCFPS # 
  for i in range (len(description)):
    if "NOCFPS" == description [i] and "was" == description [i+1] :
      for j in range (i+2, len(description)):
        if description [j] == 'Tk.':
          n=j+1
          break
      break  

  nocfps_string = description [n]

  if ("(" in nocfps_string):
    nocfps = - float(nocfps_string.strip('()'))
  else:
    nocfps = float(nocfps_string)  

  # NOCFPS # 
  for i in range (len(description)):
    if "NAV" == description [i] :
      for j in range (i+2, len(description)):
        if description [j] == 'Tk.':
          n=j+1
          break
      break  
    
  nav_string = description [n]

  if ("(" in nav_string):
    nav = - float(nav_string.strip('()'))
  else:
    nav = float(nav_string)  

  print(q, year, yearEnd, code, eps, nocfps, nav, news['date'])