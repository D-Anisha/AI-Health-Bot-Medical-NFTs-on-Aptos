import requests
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
import ssl

# from utils.pinata_uploader import upload_to_pinata  # Uncomment when needed

url = "https://your-backend.com/api/mint"


headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer your_token",  # Replace with real token
}
payload = {
    "ipfs_hash": "your_ipfs_hash",          # Replace with actual IPFS hash
    "wallet_address": "wallet_address_here" # Replace with actual wallet address
}

class SSLAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = ssl.create_default_context()
        context.set_ciphers('ALL')
        kwargs['ssl_context'] = context
        return super().init_poolmanager(*args, **kwargs)

session = requests.Session()
adapter = SSLAdapter()
session.mount("https://", adapter)

response = session.post(url, headers=headers, json=payload)

print(response.status_code)
print(response.text)
