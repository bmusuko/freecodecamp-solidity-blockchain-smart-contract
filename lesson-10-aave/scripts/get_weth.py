from scripts.utils import get_account
from brownie import interface, config, network


def get_weth(amount):
    account = get_account()
    weth = interface.IWeth(config["networks"][network.show_active()]["weth_token"])
    tx = weth.deposit({"from": account, "value": amount * (10**18)})
    tx.wait(1)
    print(f"Swap {amount} ETH to wETH")
    return tx


def main():
    get_weth(0.01)
