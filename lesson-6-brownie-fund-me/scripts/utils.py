from brownie import network, accounts, config, MockV3Aggregator
from web3 import Web3


DECIMAL = 8
STARTING_PRICE = 500000000000
LOCAL_BLOCKCHAIN_ENVIRONMENT = ["development", "ganache-local"]
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork-dev"]


def get_account():
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENT
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def get_mocks_aggregator():
    if len(MockV3Aggregator) <= 0:
        print("Deploying mock V3 Aggregator")
        mock_aggregator = MockV3Aggregator.deploy(
            DECIMAL, STARTING_PRICE, {"from": get_account()}
        )
        print("Mock V3 Aggregator Deployed")
    price_feed_address = MockV3Aggregator[-1].address
    return price_feed_address