import requests 

def get_token_info(network, address):
    params = {
        "network": network,
        "address": address
    }
    url = f"https://api.geckoterminal.com/api/v2/networks/{params["network"]}/tokens/{params["address"]}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "application/json;version=20230302"
    }

    response = requests.get(url=url, params=params, headers=headers, verify=False)
    if response:
        return response.json()
    return False