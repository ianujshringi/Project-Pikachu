from brownie import network, AdvancedNFT
import pytest
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENV, get_account, get_contract
from scripts.advanced_nft.deploy_and_create_nft import deploy_and_create_nft


def test_can_create_advanced_nft():
    """
    1. deploy the contract
    2. create a NFT
    3. get a random pokemon back
    """

    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENV:
        pytest.skip("Only for local testing")

    # Act
    advanced_nft, creation_tx = deploy_and_create_nft()
    requestId = creation_tx.events["requestNFT"]["requestId"]
    random_number = 777
    get_contract("vrf_coordinator").callBackWithRandomness(
        requestId, random_number, advanced_nft.address, {"from": get_account()}
    ).wait(1)

    # Assert
    assert advanced_nft.tokenCounter() == 1
    assert advanced_nft.tokenIdToType(0) == random_number % 4
