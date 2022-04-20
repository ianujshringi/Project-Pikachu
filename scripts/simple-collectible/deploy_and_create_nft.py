from scripts.helpful_scripts import get_account
from brownie import SimpleCollectible

def main():
    account = get_account()
    simple_collectible = SimpleCollectible.deploy({"from" : account})