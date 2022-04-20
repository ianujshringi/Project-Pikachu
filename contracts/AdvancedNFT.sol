// An NFT contract 
// Where the tokenURI can be one of three different pikachus randomly selected.

// SPDX-License-Identifier: Unlicensed

pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@chainlink/contracts/src/v0.8/VRFConsumerBase.sol";

contract AdvancedNFT is ERC721, VRFConsumerBase {
    
    uint256 public tokenCounter;
    bytes32 public keyHash;
    uint256 public fee;

    enum PokemonType{Fire, Dark, Ice, Ghost}
    mapping(uint256 => PokemonType) public tokenIdToType;
    mapping(bytes32 => address) public requestIdToSender;
    mapping (uint256 => string) private _tokenURIs;

    event requestNFT(bytes32 indexed requestId, address requester);
    event typeAssigned(uint256 indexed tokenId, PokemonType pokemonType);

    constructor(address _vrfCoordinator, address _linkToken, bytes32 _keyHash, uint256 _fee) public
    VRFConsumerBase(_vrfCoordinator, _linkToken)
    ERC721("Pikachu", "POK")
    {
        tokenCounter = 0;
        keyHash = _keyHash;
        fee = _fee; 
    }

    function createNFT() public returns (bytes32) {
        // reuest randomNo
        bytes32 requestId = requestRandomness(keyHash, fee);
        
        // map requestId to owner(*User calling the createNFT function.)
        requestIdToSender[requestId] = msg.sender;
        //emit event
        emit requestNFT(requestId, msg.sender);
    }

    function fulfillRandomness(bytes32 requestId, uint256 randomNumber) internal override {
        
        // get random pokemon and assign the token id
        PokemonType pokemonType = PokemonType(randomNumber % 4);
        uint256 newTokenId  = tokenCounter; 
        tokenIdToType[newTokenId] = pokemonType;
        // emit event
        emit typeAssigned(newTokenId, pokemonType);

        //Mint the nft 
        address owner = requestIdToSender[requestId];
        _safeMint(owner, newTokenId);

        // increment the tokenCounter
        tokenCounter += 1;
    }

    function _setTokenURI(uint256 _tokenId, string memory _tokenURI) internal virtual {
        require(_exists(_tokenId), "ERC721Metadata: URI set of nonexistent token");
        _tokenURIs[_tokenId] = _tokenURI;
    }
}

