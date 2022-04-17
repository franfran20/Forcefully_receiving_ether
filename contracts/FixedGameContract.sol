//SPDX-License-Identifier: MIT

pragma solidity ^0.8.7;

contract FixedGameContract {
    uint256 public targetAmount = 5 ether;
    uint256 public balance;
    address public winner;
    
    
    function play() public payable{
        require(msg.value == 1 ether);
        balance += msg.value;

        require(balance <= targetAmount, "Game is over cant participate again");

        if(balance == targetAmount){
            winner = msg.sender;
        }
    }

    function claimReward() public {
        require(msg.sender == winner);
        (bool sent, ) = msg.sender.call{value: balance}("");
        require(sent, "Tx failed to send ether");
    }

    function getBalance() public view returns (uint256){
        return address(this).balance;
    }
}

