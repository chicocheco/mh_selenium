## mh_selenium

Web scraper written in Selenium (Python) inspired by my work in a call center, collecting contact data of rental 
agencies and individuals offering their estates online.

Dependencies:
- linux
- python 3.7
- selenium
- openpyxl
- pymysql
- mariadb (execute `install_db.py` to create a new database user and import a database scheme)
- firefox 65 + uBlock Origin and NoScript (unzip `helpers/mrgxem71.scraping.zip` folder into 
`/home/your_username/.mozilla/firefox` (linux) and set `linux_user` variable to match in `contact_scraper.py`)

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

Sample URLs to test with:
- `https://www.milanuncios.com/alquiler-vacaciones-en-las_palmas/`
- `https://vacances.seloger.com/location-vacances-france/savoie-10000007425`
- `https://www.vivaweek.com/fr/locations-vacances/herault-languedoc-roussillon-france/hebergement-type:appartement,studio,autre-appartement,bateau,catamaran,peniche,voilier,yacht,autre-bateau,bungalow-mobilhome,chalet,chateau-manoir,gite,insolite,cabane-arbre,moulin,phare,roulotte,tipi,yourte,autre-insolite,maison-villa,mas,riad,villa,autre-maison`
- `https://www.traum-ferienwohnungen.de/europa/deutschland/schleswig-holstein/ergebnisse/?person=34&is_in_clicked_search=1`

Examples of how to run the program:
- `python contact_scraper.py -begin 50 -end 100 'https://www.milanuncios.com/alquiler-vacaciones-en-las_palmas/'`
- `python contact_scraper.py -b 33 'https://www.milanuncios.com/alquiler-vacaciones-en-las_palmas/'`
- `python contact_scraper.py -e 66 'https://www.milanuncios.com/alquiler-vacaciones-en-las_palmas/'`
- `python contact_scraper.py 'https://www.milanuncios.com/alquiler-vacaciones-en-las_palmas/'`

Run `contact_scraper.py with --help` to get a description of each parameter.
