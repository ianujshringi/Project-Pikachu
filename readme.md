# **Project-Pikachu :**

_A Simple ERC721 demonstration contract wich shows some concepts like :_

1. Creating an ERC721 token.
2. Pinning files to ipfs and also uploading same to PINATA.
3. Creating metadata for tokens.
4. URI generation for the file and also metadata.
5. Assigning URI to token.

## **Info about the advance-nft contract:**

This contract generates a random and unique pokemon nft when called.
For deploying the contract run the following script:
[deploy_and_create_nft.py](./scripts/advanced_nft/deploy_and_create_nft.py)

### **Languages and tools used :**
- Languages:
     1. `Solidity`  
     2. `Python`  
 - Tools and Services:
     1. [Brownie](https://eth-brownie.readthedocs.io/en/stable/)  
     2. [Alchemy](https://www.alchemy.com/)  
     3. [PINATA](https://app.pinata.cloud/)

### **Script execution order for minting pokemon nft:**

1. [create_nft.py](./scripts/advanced_nft/create_nft.py)
2. [create_metadata.py](./scripts/advanced_nft/create_metadata.py)
3. [set_token_uri.py](./scripts/advanced_nft/set_token_uri.py)

**Note : Add a `.env` file containing following**:
 - `PRIVATE_KEY`="Your account's private key here"
 - `PINATA_API_KEY`="Your api key here"
 - `PINATA_API_SECRET`="Your secret key here"
 - `UPLOAD_IPFS`= "`true` if you want to only upload to ipfs"
 - `UPLOAD_PINATA`="`true` if you want to upload to pinata and pin it to ipfs"

#### **Demo nft link : https://testnets.opensea.io/assets/0xeda3e7518e0a4d50fb15fc5872ec8283f2bdaa57/0/**
