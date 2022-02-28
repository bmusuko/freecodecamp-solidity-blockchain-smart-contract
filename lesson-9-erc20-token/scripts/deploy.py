from .utils import get_account
from brownie import NDC, config, network
from web3 import Web3

initial_supply = Web3.toWei(1_000_000_000, "ether")


def deploy():
    account = get_account()
    NDC.deploy(
        initial_supply,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )


def main():
    deploy()
