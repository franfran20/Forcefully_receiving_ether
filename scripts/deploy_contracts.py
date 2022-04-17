from brownie import BreakGame, FixedGameContract, GameContract, network, accounts
from scripts.helpful_scripts import get_account, one_ether

# we'll use this function to make writing tests easier!
def deploy_contracts():
    account = get_account()
    game_contract = GameContract.deploy({"from": account})
    break_game = BreakGame.deploy({"from": account})
    fixed_game_contract = FixedGameContract.deploy({"from": account})
    return game_contract, break_game, fixed_game_contract


def main():
    deploy_contracts()
