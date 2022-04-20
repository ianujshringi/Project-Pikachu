from brownie import accounts, network, config, Contract, VRFCoordinatorMock, LinkToken
from web3 import Web3

LOCAL_BLOCKCHAIN_ENV = ["development", "ganache-local"]
FORKED_LOCAL_ENV = ["mainnet-fork"]
OPENSEA_URL = "https://testnets.opensea.io/assets/{}/{}"


def get_account(index=None, id=None):
    """
    This function will return the account based on the given args or network status.
    """
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENV
        or network.show_active() in FORKED_LOCAL_ENV
    ):
        return accounts[0]

    return accounts.add(config["wallets"]["from_key"])


contract_to_mock = {
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token": LinkToken,
}


def get_contract(contract_name):
    """
    Summery :
        - return the latest deployed contract.
        - Or deploy a Mock to use for a network that does'nt have the contract.

    Args:
        contract_name (string) : Name of the contract that got from the config or deploy

    Returns :
        brownie.network.contract.ProjectContract (The most recently deployed contract of the type
        specified by a dictionary. this could be either a mock or a 'real'
        contract on a live chain.)
    """

    contract_type = contract_to_mock[contract_name]

    if network.show_active() in LOCAL_BLOCKCHAIN_ENV:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]

    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(
            contract_type.name, contract_address, contract_type.abi
        )
    return contract


def deploy_mocks():
    """
    Module to deploy mocks to a testnet
    """
    print(f"The active network is {network.show_active()}")
    print("\n---------------------Deploying Mocks-------------------\n")
    account = get_account()
    print("\n----------------Deploying Mock Link Token--------------\n")
    link_token = LinkToken.deploy({"from": account})
    print(f"Link Token Deployed to {link_token.address}")
    print("\n-------------Deploying Mock VRF Coordinator------------\n")
    vrf_coordinator = VRFCoordinatorMock.deploy(link_token.address, {"from": account})
    print(f"VRF Coordinator Deployed to {vrf_coordinator.address}\n")


def fund_with_link(
    contract_address, account=None, link_token=None, amount=Web3.toWei(1, "ether")
):
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")

    tx = link_token.transfer(contract_address, amount, {"from": account})
    tx.wait(1)
    print("Contract Funded!")
