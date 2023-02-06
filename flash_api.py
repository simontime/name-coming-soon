import requests

# API constants
FLASH_API_KEY             = "AIzaSyD-bwHpMvFCN3PfRN4Txsw_ECg_iptNfMQ"
FLASH_API_URL_BASE        = "https://content-flashstation-pa.googleapis.com/v1"
FLASH_API_ENDPOINT_BUILDS = "/builds"
FLASH_API_REFERRER        = "https://flash.android.com"

# Retrieves the list of available builds given a product ID 
def retrieve_builds_for_product(product):
    # Generate URL
    url = FLASH_API_URL_BASE + FLASH_API_ENDPOINT_BUILDS

    # URL params
    params = {
        "product": product,
        "key":     FLASH_API_KEY
    }

    # Make request
    response = requests.get(url, params=params, headers={"Referer": FLASH_API_REFERRER})

    # Decode JSON object and return
    return response.json()
