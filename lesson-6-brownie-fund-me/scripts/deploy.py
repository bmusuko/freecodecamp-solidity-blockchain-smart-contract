from brownie import FundMe, accounts, network, config
from scripts.utils import (
    get_account,
    get_mocks_aggregator,
    LOCAL_BLOCKCHAIN_ENVIRONMENT,
)


def deploy_fund_me():
    account = get_account()

    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENT:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        price_feed_address = get_mocks_aggregator()

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print(f"Contract deployed to {fund_me.address}")
    return fund_me


def main():
    deploy_fund_me()