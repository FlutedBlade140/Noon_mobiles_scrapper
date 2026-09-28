# Noon Egypt Mobile Catalog Scraper

A Python script to extract mobile phone specifications and pricing from Noon Egypt.

### How it works
It targets Noon's internal catalog API (`mp-customer-catalog-api`). To prevent `403 Forbidden` responses, the script uses a persistent `requests.Session` with required headers including `x-cms`, `x-mp-country`, `x-ecom-zonecode`, and dynamically updates the `referer` header per page iteration.

### Data Collected
- Brand & Model Name
- Original Price & Sale Price (EGP)
- Screen Size & Battery Capacity

### Requirements
```bash
pip install requests pandas
```
### Running the script
```bash
python Noon_mobiles_scrapper.py
```
### Output
Outputs the scraped mobile catalog to Noon_phones.csv encoded in utf-8-sig.
