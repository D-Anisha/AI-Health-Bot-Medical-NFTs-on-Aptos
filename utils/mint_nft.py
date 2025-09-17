import requests
def mint_nft_to_patron(ipfs_hash, wallet_address):
    url = "https://your-backend.com/api/mint"  # Replace with your actual endpoint
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "wallet_address": wallet_address,
        "ipfs_hash": ipfs_hash
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise if 4xx or 5xx
        try:
            return response.json()  # Try parsing JSON
        except requests.exceptions.JSONDecodeError:
            print("Non-JSON response received:")
            print(response.text)
            return {"error": "Invalid JSON returned from server"}
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return {"error": str(e)}
