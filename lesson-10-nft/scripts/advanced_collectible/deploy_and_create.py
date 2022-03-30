from scripts.utils import get_account, OPENSEA_URL, get_contract, fund_with_link
from brownie import AdvancedCollectible, config, network

from web3 import Web3
from web3.middleware import geth_poa_middleware


def deploy_and_create():
    w3 = Web3("http://localhost:8545")
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    account = get_account()
    advanced_collectible = AdvancedCollectible.deploy(
        get_contract("vrf_coordinator"),
        get_contract("link_token"),
        config["networks"][network.show_active()]["keyhash"],
        config["networks"][network.show_active()]["fee"],
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    fund_with_link(advanced_collectible.address, amount=Web3.toWei(0.1, "ether"))
    creating_tx = advanced_collectible.createCollectible({"from": account})
    creating_tx.wait(1)
    print("New Token (NFT) has been created")
    return advanced_collectible, creating_tx


def main():
    deploy_and_create()
