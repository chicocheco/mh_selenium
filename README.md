## mh_selenium

Web scraper written in Selenium (Python) inspired by my work in a call center, collecting contact data of rental 
agencies and individuals offering their estates online.

Dependencies :
- Linux
- pyenv global 3.7.0; python -m venv venv370; pyenv global system; source venv370/bin/activate
- (venv370) pip install selenium
- (venv370) pip install openpyxl
- (venv370) pip install pymysql
- Firefox v.65 with add-ons uBlock Origin and NoScript installed
- MariaDB v. 10.3.12
- execute `install_db.py` to create a new database user and import a database scheme
- unzip `helpers/mrgxem71.scraping.zip` folder into `/home/your_username/.mozilla/firefox` (linux) and set `linux_user`
variable to match in `contact_scraper.py`

How it works:
1. When neither from_page nor to_page arguments were input (int), start scraping from the first page to the last page 
that was confirmed on the first page.
2. When only from_page argument was input (must be by its keyword), start scraping from there to the last page that was
 confirmed on the first page.
3. When only to_page argument was input, start scraping from the first page to to_page but to_page cannot exceed the 
last confirmed page. If so, it is lowered to the last confirmed page (scraping that single page only).
4. When from_page and to_page arguments were input, start scraping from from_page to to_page but:
- to_page cannot exceed the last confirmed page. If so, it is lowered to the last confirmed page.
- to_page must be a bigger number than from_page. If so a warning appears and the program terminates.
- If from_page and to_page are the same numbers, only 1 page is scraped and the program terminates.
     
Usage:
The input URL must be always the first URL of the search results (listing page number 1) and so far only of the 
following websites:
- www.milanuncios.com (ES)
- vacances.seloger.com (FR)
- https://www.vivaweek.com (FR)
- www.traum-ferienwohnungen.de (DE)

Edit the following line in contact_scraper.py and execute it:
p = mp.Process(target=start_crawl(first_url, to_page, from_page, output_xlsx=file.xlsx))

where arguments: 
- `first_listing` (URL (str) - required)
- `to_page` (number (int) - optional)
- `from_page` (number (int) - optional)
- `output_xlsx=file.xlsx` (file name ending with '.xlsx' (str) - required until an auto-creation feature of a database 
scheme implemented)

example:

`first_listing_url = 'https://vacances.seloger.com/location-vacances-france/savoie-10000007425'`

`p = mp.Process(target=start_crawl(first_listing_url, 30, 15, output_xlsx='file.xlsx'))`
