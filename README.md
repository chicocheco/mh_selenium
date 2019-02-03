## mh_selenium

Web scraper written in Selenium (Python) based on needs of MH Marketing.

Dependencies:
- pyenv global 3.7.0; python -m venv venv370; pyenv global system; source venv370/bin/activate
- (venv370) pip install selenium
- (venv370) pip install openpyxl
- (venv370) pip install pymysql

How it works:
1. when neither from_page nor to_page is input (integers), execute from the first page to the last page that was found
2. when only from_page was input (!with keyword argument!), execute from from_page to the last page that was found
3. when only to_page was input, execute from the first page to the to_page but:
- to_page cannot exceed last existing page, it is lowered to the last page that was found if so
- if to_page=1 was input, only 1 page is scraped and the program terminates if so
4. when from_page and to_page were input, execute from from_page to to_page but:
- to_page cannot exceed last existing page, it is lowered to the last page that was found if so
- to_page must be a bigger number than from_page, a warning appears and the program terminates if so
- if from_page and to_page are the same numbers, only 1 page is scraped and the program terminates if so
     
Usage:
The input URL must be always the first URL of the search results (listing page number 1) and so far only of the following websites:
- www.milanuncios.com (ES)
- vacances.seloger.com (FR)
- https://www.vivaweek.com (FR)
- www.traum-ferienwohnungen.de (DE)

Edit the following line in contact_scraper.py and execute:
p = mp.Process(target=start_crawl(first_url, to_page, from_page, output_xlsx=file.xlsx))

where arguments: 
- first_listing (URL (str) - required)
- to_page (number (int) - optional)
- from_page (number (int) - optional)
- output_xlsx=file.xlsx (file name ending with '.xlsx' (str) - optional), if not input, store in database
  
example:
p = mp.Process(target=start_crawl('https://vacances.seloger.com/location-vacances-france/savoie-10000007425', 30, 15, output_xlsx=file.xlsx))
