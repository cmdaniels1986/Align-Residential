C:\Users\cmdan\Anaconda3\Scripts\activate.bat
CD /d %~dp0
scrapy crawl doloress_spider -o "file:///C:\Users\cmdan\Desktop\Spiders\Align-Residential\results\results.csv" -t csv
popd