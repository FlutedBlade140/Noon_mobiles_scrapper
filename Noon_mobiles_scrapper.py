import requests
import time
import pandas as pd

def scraper_code():
    url = f"https://www.noon.com/_vs/nc/mp-customer-catalog-api/api/v3/u/electronics-and-mobiles/mobiles-and-accessories/mobiles-20905/"
    items = []
    session = requests.Session()
    session.headers.update({
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "no-cache, max-age=0, must-revalidate, no-store",
        "priority": "u=1, i",
        "sec-ch-ua": "\"Chromium\";v=\"153\", \"Not_A Brand\";v=\"8\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Linux\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36",
        "x-ab-test": "1891,4632,4801,5001,4816,4832,4910,5081,1931,2001,4860,5271,5300,1531,1771,2531,4371,4511,3031,4730,4151,5372,5151,2881,3451,5501,4291,4401,5190,3731,5172,5342,3771,4481,4821,5050,4621,5071,4032,3920,4012,4990,2941,4203,5121,4692,5230,5261,1841,2741,5310,4342,5360,3442,2271,4871,4970,4672,5201,2161,4642,5061,1471,2451,2561,3900,4431,4442,4470,4931,2351,4551,5251,4361,4592,2341,3561,4560,4782,1881,3351,4191,4250,4532,4751,4772,4891,4581,4681,4881,4961,5111,5460,2841,4081,4230,4701,4921,4940",
        "x-cms": "v2",
        "x-content": "desktop",
        "x-ecom-zonecode": "EG-CAI-S10",
        "x-locale": "en-eg",
        "x-mp-country": "eg",
        "x-platform": "web",
    })
        
    for x in range(1 , 11):
        print(f"fetching page {x}...")
        time.sleep(1)
        session.headers.update({
            "referer": f"https://www.noon.com/egypt-en/electronics-and-mobiles/mobiles-and-accessories/mobiles-20905/?limit=50&page={str(x)}",
        })
        querystring = {"ps":"true","limit":"50","page": str(x)}
        payload = ""
        try:
            r = session.get(url, data=payload, params=querystring)
            r.raise_for_status()
            print (f"{r.status_code} OK" )
            data = r.json()
        except requests.exceptions.HTTPError as http_err:
            print(f"[!] HTTP error on page {x}: {http_err}")
            break  # Stop the loop if the URL/Build ID is dead
                
        except requests.exceptions.JSONDecodeError:
            print(f"[!] Page {x} did not return JSON. Returned raw HTML/Protection page instead.")
            continue  # Skip to the next page
                
        except requests.exceptions.RequestException as req_err:
            print(f"[!] Network error on page {x}: {req_err}")
            continue
        phones = data.get("hits" , {})
        for p in phones:
            raw_price = p.get("price")
            sale_price = p.get("sale_price")
            items.append({
                "Brand": p.get("brand"),
                "Model": p.get("name"),
                "Screen Size" : p.get("plp_specifications" , {}).get("Screen Size"),
                "Battery Capacity" : p.get("plp_specifications" , {}).get("Battery Size"),
                "Price (EGP)" : raw_price,
                "Sale Price (EGP)" : sale_price
            })
        
    return items

def save_to_csv(items):
    df = pd.DataFrame(items)
    df.to_csv("Noon_phones.csv", index=False , encoding='utf-8-sig')
    print(f"Scraping completed. Total items scraped: {len(items)}")

def main():
    items = scraper_code()
    save_to_csv(items)


if __name__ == "__main__":
    main()