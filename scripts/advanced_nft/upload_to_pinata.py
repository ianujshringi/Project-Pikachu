import os
from pathlib import Path
import requests

PINATA_BASE_URL = "https://api.pinata.cloud/"
endpoint = "pinning/pinFileToIPFS"

headers = {
    "pinata_api_key": os.getenv("PINATA_API_KEY"),
    "pinata_secret_api_key": os.getenv("PINATA_API_SECRET"),
}


def upload_to_pinata(filepath):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        filename = filepath.split("/")[-1:][0]
        response = requests.post(
            PINATA_BASE_URL + endpoint,
            files={"file": (filename, image_binary)},
            headers=headers,
        )
        ipfs_hash = response.json()["IpfsHash"]
        image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        return image_uri
