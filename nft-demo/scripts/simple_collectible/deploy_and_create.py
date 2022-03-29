from scripts.utils import get_account, OPENSEA_URL
from brownie import SimpleCollectible

from web3 import Web3
from web3.middleware import geth_poa_middleware


sample_token_uri = (
    "ipfs://Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json"
)


def deploy_and_create():
    w3 = Web3("http://localhost:8545")
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    account = get_account()
    simple_collectible = SimpleCollectible.deploy({"from": account})
    tx = simple_collectible.createCollectible(sample_token_uri, {"from": account})
    tx.wait(1)
    print(
        f"you can view your NFT at {OPENSEA_URL.format(simple_collectible.address, simple_collectible.tokenCounter()-1)}"
    )
    return simple_collectible


def main():
    deploy_and_create()
