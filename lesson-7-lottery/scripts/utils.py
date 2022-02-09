from brownie import network, accounts, config, MockV3Aggregator, Contract, LinkToken, VRFCoordinatorMock, interface
from web3 import Web3
import time

DECIMAL = 8
STARTING_PRICE = 3000_00000000
LOCAL_BLOCKCHAIN_ENVIRONMENT = ["development", "ganache-local"]
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork-dev"]


def get_account(index=None, id=None):
    if index:
        return accounts[index]

    if id:
        return accounts.load(id)

    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENT
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]

    return accounts.add(config["wallets"]["from_key"])


contract_to_mock = {
    "eth_usd_price_feed": MockV3Aggregator,
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token": LinkToken
}


def deploy_mocks():
    account = get_account()
    MockV3Aggregator.deploy(
        DECIMAL, STARTING_PRICE, {"from": account}
    )
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

    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENT:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active(
        )][contract_name]

        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi)
    return contract


def fund_with_link(contract_address, account=None, link_token=None, amount=(10**17)):
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    transfer_tx = link_token.transfer(
        contract_address, amount, {"from": account})
    # link_token_contract = interface.LinkTokenInterface(link_token.address)
    # link_token_contract.transfer(contract_address, amount, {"from": account})
    transfer_tx.wait(1)
    print("Fund contract with link token!")
    return transfer_tx
