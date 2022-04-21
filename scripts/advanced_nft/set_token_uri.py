import json
from brownie import network, AdvancedNFT
from scripts.helpful_scripts import OPENSEA_URL, get_account, get_pokemonType


def main():
    print(f"Working on {network.show_active()}")
    advanced_nft = AdvancedNFT[-1]
    number_of_nfts = advanced_nft.tokenCounter()
    print(f"You have {number_of_nfts} tokenIds")
    for token_id in range(number_of_nfts):
        pokemonType = get_pokemonType(advanced_nft.tokenIdToType(token_id))
        if not advanced_nft.tokenURI(token_id).startswith("https://"):
            print(f"Setting tokenURI of {token_id}")
            uri_file_name = (
                f"./metadata/{network.show_active()}/{token_id}-{pokemonType}-uri.json"
            )
            set_tokenURI(
                token_id, advanced_nft, get_tokenURI(uri_file_name, str(token_id))
            )


def set_tokenURI(token_id, nft_contract, tokenURI):
    account = get_account()
    tx = nft_contract._setTokenURI(token_id, tokenURI, {"from": account})
    tx.wait(1)
    print(
        f"Awesome! You can view your NFT at {OPENSEA_URL.format(nft_contract, token_id)}"
    )
    print(
        "It could take some time to see the result please wait up to 20 min. and hit refresh metadata button."
    )


def get_tokenURI(nft_uri, token_id):
    with open(nft_uri, "r") as file:
        return json.load(file)[token_id]
