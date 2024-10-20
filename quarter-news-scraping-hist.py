import pymongo, certifi, datetime, re
from data import stocks_list_details
from variables import mongo_string

myclient = pymongo.MongoClient(mongo_string, tlsCAFile=certifi.where())
mydb = myclient["stockanalyst"]

def is_valid_date(year, month, day):
    try:
        datetime.datetime(year, month, day)
        return True
    except ValueError:
        return False

count = 0
year_insert = 2024
for month_insert in range(7, 8):
  for date_insert in range(24, 25):

    print(f'date -> {date_insert}, month -> {month_insert}')

    if not is_valid_date(year_insert, month_insert, date_insert):
        print('invalid date')
        continue

    news_list = mydb.news.find({
        'date': datetime.datetime(year_insert, month_insert, date_insert, 0, 0),
        'title': { '$regex': 'Financials', '$options': 'i' } ,
        # 'tradingCode': 'BERGERPBL',
        # 'description': { '$regex': '^\\(Q[0-9] (Un-audited|Audited)\\): (EPU) was', '$options': 'i' } 
        'description': { '$regex': '^\\(Q[0-9] (Un-audited|Audited)\\): (Diluted EPS|Consolidated EPS|Basic EPS|EPS|EPU) was', '$options': 'i' } 
    })
  
    for news in news_list:

      try:
        q = news['title'].split()[1].lower()
        code = news['title'].split()[0].replace(":", "")
        description = news['description'].split()

        filtered_list = [e for e in stocks_list_details if e['tradingCode'] == code]

        if len(filtered_list) < 1:
          print('trading code not found')
          continue

        yearEnd = filtered_list[0]['yearEnd']

        # EPS #
        n=-1
        for i in range (len(description)):
          if "EPS" == description[i] or "EPU" == description[i]:
            for j in range (i+2, len(description)):
              if description [j] == 'Tk.':
                n=j+1
                break
            break 

        eps_string = description [n] if n != -1 else None 

        if eps_string:
          if ("(" in eps_string):
            eps = - float(eps_string.strip('()'))
          else:
            eps = float(eps_string) 
        else:
          eps = 0

        # YEAR #
        for i in range (n+3, len(description)):
          if description[i][:3] == '202': 
            year_string = (description[i]).replace(".", '').replace(";", '').replace(",", '')[:4]
            if (yearEnd == '30-Jun'):
              if (q == 'q1' or q == 'q2'):
                year = str(int(year_string) + 1)
              else:
                year = year_string
            else:
              year = year_string
            break      

        # NOCFPS # 
        n=-1
        for i in range (len(description)):
          if "NOCFPS" == description[i] or "NOCFPU" == description[i]:
            for j in range (i+2, len(description)):
              if description [j] == 'Tk.':
                n=j+1
                break
            break  

        nocfps_string = description [n] if n != -1 else None

        if nocfps_string: 
          if ("(" in nocfps_string):
            nocfps = - float(nocfps_string.strip('()'))
          else:
            nocfps = float(nocfps_string)  
        else: 
          nocfps = 0    

        # NAV # 
        n=-1
        for i in range (len(description)):
          if "NAV" == description [i] :
            for j in range (i+2, len(description)):
              if description [j] == 'Tk.':
                n=j+1
                break
            break  
          
        nav_string = (description [n]).replace(",", '') if n != -1 else None 

        if nav_string:
          if ("(" in nav_string):
            nav = - float(nav_string.strip('()'))
          else:
            nav = float(nav_string)
        else:
          nav = 0      

        print(code, q, year, yearEnd, eps, nav, nocfps, news['date'])

        data = mydb.fundamentals.find_one({ 'tradingCode': code })

        eps_data = data['epsQuaterly'] if 'epsQuaterly' in data else []
        nav_data = data['navQuaterly'] if 'navQuaterly' in data else []
        nocfps_data = data['nocfpsQuaterly'] if 'nocfpsQuaterly' in data else []
        
        index = -1
        for i in range (len(eps_data)):
          if str(eps_data[i]['year']) == year:
            index = i
            break  
        
        if index != -1:
          eps_data[index][q] = eps
        else:
          eps_data.append({
            'year': year,
            q: eps
          })  

        index = -1
        for i in range (len(nav_data)):
          if nav_data[i]['year'] == year or nav_data[i]['year'] == int(year):
            index = i
            break  
        
        if index != -1:
          nav_data[index][q] = nav
        else:
          nav_data.append({
            'year': year,
            q: nav
          })  

        index = -1
        for i in range (len(nocfps_data)):
          if nocfps_data[i]['year'] == year or nocfps_data[i]['year'] == int(year):
            index = i
            break  
        
        if index != -1:
          nocfps_data[index][q] = nocfps
        else:
          nocfps_data.append({
            'year': year,
            q: nocfps
          })  

        newvalues = {
          'epsQuaterly': eps_data,
          'navQuaterly': nav_data,
          'nocfpsQuaterly': nocfps_data,
        }

        mydb.fundamentals.update_one({ 'tradingCode': code }, { '$set': newvalues })
        print('# insert success', newvalues)

        count += 1
        print("Count: ", count)

      except Exception as excp:
        print(code, ' -> Error: ', str(excp))
        continue    