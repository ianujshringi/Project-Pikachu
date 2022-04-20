from scripts.helpful_scripts import get_account, OPENSEA_URL, get_contract, fund_with_link
from brownie import AdvancedNFT, network, config

def deploy_and_create_nft():
    account = get_account()
    print("\n------------------Deploying AdvancedNFT----------------\n")
    advanced_nft = AdvancedNFT.deploy(
        get_contract("vrf_coordinator"),
        get_contract("link_token"),
        config["networks"][network.show_active()]["key_hash"],
        config["networks"][network.show_active()]["fee"],
        {"from" : account}
    )
    print("\n------------------AdvancedNFT Deployed-----------------\n")

    # funding the contract with links
    fund_with_link(advanced_nft.address) 

    tx = advanced_nft.createNFT({"from" : account})
    tx.wait(1)
    print("\n---------------New token has been created--------------\n")


def main():
    deploy_and_create_nft()