from brownie import accounts, network, exceptions
from scripts.deploy_contracts import deploy_contracts
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENV,
    get_account,
    one_ether,
    five_ether,
)
import pytest


def test_game_expected_functionality():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENV:
        pytest.skip("Only for local testing")
    # fetchin already deployed_contracts
    game_contract, break_game, fixed_game_contract = deploy_contracts()

    # we allow 5 users to play the game, the 5th account is the winner
    game_contract.play({"from": accounts[0], "value": one_ether})
    game_contract.play({"from": accounts[1], "value": one_ether})
    game_contract.play({"from": accounts[2], "value": one_ether})
    game_contract.play({"from": accounts[3], "value": one_ether})
    # winnin account
    game_contract.play({"from": accounts[4], "value": one_ether})
    # winner prev balance
    winner_prev_balance = accounts[4].balance()
    # claim reward
    game_contract.claimReward({"from": accounts[4]})

    # check winner balance
    assert accounts[4].balance() == winner_prev_balance + five_ether


def test_game_break():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENV:
        pytest.skip("Only for local testing")
    # fetchin already deployed_contracts
    game_contract, break_game, fixed_game_contract = deploy_contracts()

    # we allow 5 users to play the game, the 5th account is the winner
    game_contract.play({"from": accounts[0], "value": one_ether})
    game_contract.play({"from": accounts[1], "value": one_ether})
    game_contract.play({"from": accounts[2], "value": one_ether})
    # attacking the contract by forcefully sending ether
    break_game.breakGame(
        game_contract.address, {"from": accounts[8], "value": five_ether}
    )
    # this user is supposed to be allowed to play but he can't why?
    # we forcefully sent ether to the game contract when it didnt have a fallback function
    # now the logic of the game has been destroyed
    # no winner no player no reward!
    with pytest.raises(exceptions.VirtualMachineError):
        game_contract.play({"from": accounts[3], "value": one_ether})

    assert game_contract.getBalance() > five_ether


def test_fixed_game_functionality():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENV:
        pytest.skip("Only for local testing")
    # fetchin already deployed_contracts
    game_contract, break_game, fixed_game_contract = deploy_contracts()

    # we allow 5 users to play the game, the 5th account is the winner
    fixed_game_contract.play({"from": accounts[0], "value": one_ether})
    fixed_game_contract.play({"from": accounts[1], "value": one_ether})
    fixed_game_contract.play({"from": accounts[2], "value": one_ether})
    fixed_game_contract.play({"from": accounts[3], "value": one_ether})
    break_game.breakGame(
        fixed_game_contract.address, {"from": accounts[8], "value": five_ether}
    )
    # winning account
    fixed_game_contract.play({"from": accounts[4], "value": one_ether})
    # winner prev balance
    winner_prev_balance = accounts[4].balance()
    # claim reward
    fixed_game_contract.claimReward({"from": accounts[4]})

    # check winner balance
    assert accounts[4].balance() == winner_prev_balance + five_ether
