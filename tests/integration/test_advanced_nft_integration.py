from brownie import network, AdvancedNFT
import pytest
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENV
from scripts.advanced_nft.deploy_and_create_nft import deploy_and_create_nft
from time import sleep


def test_can_create_advanced_nft_integration():
    """
    1. deploy the contract
    2. create a NFT
    3. get a random pokemon back
    """

    # Arrange
    if network.show_active() in LOCAL_BLOCKCHAIN_ENV:
        pytest.skip("Only for local testing")

    # Act
    advanced_nft, creation_tx = deploy_and_create_nft()
    sleep(60)
    # Assert
    assert advanced_nft.tokenCounter() == 1
