from re import L
from brownie import AdvancedNFT, web3
from scripts.helpful_scripts import get_account, fund_with_link
from web3 import Web3


def createNFT():
    account = get_account()
    advanced_nft = AdvancedNFT[-1]
    fund_with_link(advanced_nft, amount=Web3.toWei(0.1, "ether"))
    create_tx = advanced_nft.createNFT({"from": account})
    create_tx.wait(1)
    print("\n---------------New token has been created--------------\n")


def main():
    createNFT()
