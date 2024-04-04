"""
        #  Crontab schedule for  
        #  python scripts 

0-5 4 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/market-start.py

* 4-7 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/price-minute.py
0-30 8 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/price-minute.py

* 4-7 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/index-minute.py
0-30 8 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/index-minute.py
45 8 * * 0-4 /usr/bin/python3 /home/ubuntu/dse_scrapper/index-minute-end.py

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




"""
        #  Crontab schedule for  
        #  python scripts 
        #  Ramadan schedule

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