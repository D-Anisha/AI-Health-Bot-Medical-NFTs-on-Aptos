import requests
from cryptography.fernet import Fernet
  # Replace with actual summary


PINATA_API_KEY = "9a17fbd24197fae05247"
PINATA_SECRET_API_KEY = "dbcf4aad6f2f69a99e66aefe0bf32f6f5f64aefe5e9716d728b2b9df130eb5a3"

def upload_to_pinata(file_path):
    url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
    headers = {
        "pinata_api_key": PINATA_API_KEY,
        "pinata_secret_api_key": PINATA_SECRET_API_KEY
    }
    with open(file_path, "rb") as file:
        response = requests.post(url, files={"file": file}, headers=headers)
    if response.status_code == 200:
        ipfs_hash = response.json()["IpfsHash"]
        print(f"✅ Uploaded to IPFS: https://gateway.pinata.cloud/ipfs/{ipfs_hash}")
        return ipfs_hash
    else:
        print("❌ Failed to upload:", response.text)
        return None