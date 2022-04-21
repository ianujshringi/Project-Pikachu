import json
import os
from brownie import AdvancedNFT, network
import requests
from scripts.helpful_scripts import get_pokemonType, get_pokemonDescription
from scripts.advanced_nft.upload_to_pinata import upload_to_pinata
from metadata.sample_metadata import metadata_template
from pathlib import Path


def main():
    advanced_nft = AdvancedNFT[-1]
    number_of_advance_nfts = advanced_nft.tokenCounter()
    print(f"you have created {number_of_advance_nfts} nfts!")
    for token_id in range(number_of_advance_nfts):
        pokemonType = get_pokemonType(advanced_nft.tokenIdToType(token_id))
        metadata_file_name = (
            f"./metadata/{network.show_active()}/{token_id}-{pokemonType}.json"
        )
        tokenURI_file = (
            f"./metadata/{network.show_active()}/{token_id}-{pokemonType}-uri.json"
        )
        nft_metadata = metadata_template
        if Path(metadata_file_name).exists():
            print(f"{metadata_file_name} already exists! Delete it to overwrite")
        else:
            print(f"Creating Metadata file: {metadata_file_name}")
            nft_metadata["name"] = pokemonType
            nft_metadata["description"] = get_pokemonDescription(pokemonType)
            image_path = "./img/" + pokemonType.lower() + ".png"

            image_uri = None
            if os.getenv("UPLOAD_PINATA") == "true":
                image_uri = upload_to_pinata(image_path)
            elif os.getenv("UPLOAD_IPFS") == "true":
                image_uri = upload_to_ipfs(image_path)
            image_uri = (
                image_uri if image_uri else type_to_image_uri(metadata_file_name)
            )

            nft_metadata["image"] = image_uri
            with open(metadata_file_name, "w") as file:
                json.dump(nft_metadata, file)

            tokenURI = None
            if os.getenv("UPLOAD_PINATA") == "true":
                tokenURI = upload_to_pinata(metadata_file_name)
            elif os.getenv("UPLOAD_IPFS") == "true":
                tokenURI = upload_to_ipfs(metadata_file_name)

            if tokenURI:
                create_tokenURI_file(tokenURI_file, token_id, tokenURI)


def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = "http://127.0.0.1:5001"
        endpoint = "/api/v0/add"
        response = requests.post(ipfs_url + endpoint, files={"file": image_binary})
        ipfs_hash = response.json()["Hash"]
        filename = filepath.split("/")[-1:][0]
        image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        return image_uri


def type_to_image_uri(metadata_file_name):
    with open(metadata_file_name, "r") as file:
        return json.load(metadata_file_name)["image"]


def create_tokenURI_file(filepath, tokenId, tokenURI):
    pokemonURI = {tokenId: tokenURI}
    with open(filepath, "w") as file:
        json.dump(pokemonURI, file)
