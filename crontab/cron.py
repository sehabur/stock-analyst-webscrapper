"""
        #  Crontab schedule for  
        #  python scripts 
        #  Latest Version

* 3-5 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/market-start.py

* 3-7 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/price-minute.py
0-30 8 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/price-minute.py
31-35 8 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/price-minute-end.py

* 3-7 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/index-minute.py
0-30 8 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/index-minute.py
45 8 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/index-minute-end.py

*/5 3-7 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/halt-status.py
0,5,10,15 8 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/halt-status.py

15 1 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/calc-gain-lose-daily.py
30 1 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/calc-index-gain-lose-daily.py

5 9 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/index-daily.py  
25 9 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/price-daily.py
30 9 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/technical-screener-daily.py
35 9 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/sector-daily.py
40 9 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/block-transection-daily.py
45 9 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/calc-shareholding-daily.py
50 9 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/reserve-surplus-daily.py
55 9 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/calc-eps-daily.py
5 10 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/screener-daily.py

5 2-14 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/news-hourly.py
10 2-14 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/quarter-news-scraping-hourly.py
15 2-14 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/yearly-news-scraping-hourly.py
20 2-14 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/calc-eps-hourly.py
25 2-14 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/screener-hourly.py

35 2-14 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/news-hourly.py
40 2-14 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/quarter-news-scraping-hourly.py
45 2-14 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/yearly-news-scraping-hourly.py
50 2-14 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/calc-eps-hourly.py
55 2-14 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/screener-hourly.py

58 14 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/market-end.py

"""


"""
        #  Crontab schedule for  
        #  python scripts 
        #  Quota issue Version

* 3-5 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/market-start.py
* 3-7 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/price-minute.py
0 8 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/price-minute.py
1-5 8 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/price-minute-end.py
* 3-7 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/index-minute.py
0 8 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/index-minute.py
15 8 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/index-minute-end.py

5,15,25,35,45,55 3-7 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/halt-status.py

15 1 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/calc-gain-lose-daily.py
30 1 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/calc-index-gain-lose-daily.py
35 9 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/index-daily.py  
5 10 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/price-daily.py
10 10 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/technical-screener-daily.py
15 10 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/sector-daily.py
5 11 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/block-transection-daily.py
10 11 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/calc-shareholding-daily.py
15 11 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/reserve-surplus-daily.py
20 11 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/calc-eps-daily.py
25 11 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/screener-daily.py

5 2-14 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/news-hourly.py
10 2-14 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/quarter-news-scraping-hourly.py
15 2-14 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/yearly-news-scraping-hourly.py
20 2-14 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/calc-eps-hourly.py
25 2-14 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/screener-hourly.py

35 2-14 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/news-hourly.py
40 2-14 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/quarter-news-scraping-hourly.py
45 2-14 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/yearly-news-scraping-hourly.py
50 2-14 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/calc-eps-hourly.py
55 2-14 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/screener-hourly.py

58 14 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/market-end.py

"""





"""
        #  Crontab schedule for  
        #  python scripts 
        #  Old Version

0-5 4 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/market-start.py

* 4-7 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/price-minute.py
0-30 8 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/price-minute.py
31-35 8 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/price-minute-end.py

* 4-7 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/index-minute.py
0-30 8 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/index-minute.py
45 8 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/index-minute-end.py

15 1 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/calc-gain-lose-daily.py
35 9 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/index-daily.py
5 10 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/price-daily.py
10 10 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/sector-daily.py
5 11 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/block-transection-daily.py
10 11 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/calc-shareholding-daily.py
15 11 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/reserve-surplus-daily.py
20 11 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/screener-daily.py

5 2-14 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/news-hourly.py
10 2-14 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/quarter-news-scraping-daily.py
15 2-14 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/yearly-news-scraping-daily.py
20 2-14 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/calc-eps-daily.py

35 2-14 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/news-hourly.py
40 2-14 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/quarter-news-scraping-daily.py
45 2-14 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/yearly-news-scraping-daily.py
50 2-14 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/calc-eps-daily.py

55 14 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/market-end.py

"""



"""
        #  Crontab schedule for  
        #  python scripts 
        #  Ramadan version

30-35 3 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/market-start.py

30-59 3 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/price-minute.py
* 4-6 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/price-minute.py
0-30 7 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/price-minute.py

30-59 3 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/index-minute.py
* 4-6 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/index-minute.py
0-30 7 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/index-minute.py
45 7 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/index-minute-end.py
15 1 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/calc-gain-lose-daily.py
5 10 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/index-daily.py
15 10 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/price-daily.py
25 10 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/sector-daily.py
10 11 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/news-daily.py
15 11 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/block-transection-daily.py
20 11 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/yearly-news-scraping-daily.py
25 11 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/quarter-news-scraping-daily.py
30 11 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/calc-eps-daily.py
35 11 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/calc-shareholding-daily.py
40 11 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/reserve-surplus-daily.py

45 11 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/market-end.py

"""