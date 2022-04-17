//SPDX-License-Identifier: MIT

pragma solidity ^0.8.7;

contract GameContract {
    uint targetAmount = 5 ether;
    address public winner;
    
    function play() public payable{
        require(msg.value == 1 ether);
        uint256 balance = address(this).balance;

        require(balance <= targetAmount, "Game is over cant participate again");

        if(balance == targetAmount){
            winner = msg.sender;
        }
    }

    function claimReward() public {
        require(msg.sender == winner);
        (bool sent, ) = msg.sender.call{value: address(this).balance}("");
        require(sent, "Tx failed to send ether");
    }

    function getBalance() public view returns (uint256){
        return address(this).balance;
    }
}