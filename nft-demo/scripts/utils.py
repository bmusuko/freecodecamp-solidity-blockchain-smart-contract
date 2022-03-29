from brownie import (
    network,
    accounts,
    config,
    Contract,
    LinkToken,
    VRFCoordinatorMock,
    interface,
)
from web3 import Web3

NON_FORKED_LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["hardhat", "development", "ganache"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = NON_FORKED_LOCAL_BLOCKCHAIN_ENVIRONMENTS + [
    "mainnet-fork",
    "binance-fork",
    "matic-fork",
]
OPENSEA_URL = "https://testnets.opensea.io/assets/{}/{}"

DECIMAL = 8
STARTING_PRICE = 3000_00000000
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork-dev"]


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    if id:
        return accounts.load(id)
    return accounts.add(config["wallets"]["from_key"])


contract_to_mock = {
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token": LinkToken,
}

BREED_MAPPING = {
    0: "PUG",
    1: "SHIBA_INU",
    2: "ST_BERNARD"
}

def get_breed(breed_number):
    return BREED_MAPPING[breed_number]

def deploy_mocks():
    account = get_account()
    link_token = LinkToken.deploy({"from": account})
    VRFCoordinatorMock.deploy(link_token.address, {"from": account})
    print("Mock Contract Deployed!")


def get_contract(contract_name):
    """
    This function will rab the contract address from the brownie config is definded, otherwise,
    it will deploy a mock version of that contract, and return it

    Args:
        contract_name

    Returns:
        brownie.network.contract.ProjectContract: The most recent deployed version of this contract
    """
    contract_type = contract_to_mock[contract_name]

    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]

        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
    return contract


def fund_with_link(
    contract_address, account=None, link_token=None, amount=Web3.toWei(0.3, "ether")
):
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    transfer_tx = link_token.transfer(contract_address, amount, {"from": account})
    # link_token_contract = interface.LinkTokenInterface(link_token.address)
    # link_token_contract.transfer(contract_address, amount, {"from": account})
    transfer_tx.wait(1)
    print("Fund contract with link token!")
    return transfer_tx
