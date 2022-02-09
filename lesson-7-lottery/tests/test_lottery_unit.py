from brownie import Lottery, accounts, config, network, exceptions
from web3 import Web3
from scripts.deploy_lottery import deploy_lottery
import pytest
from scripts.utils import LOCAL_BLOCKCHAIN_ENVIRONMENT, get_account, fund_with_link, get_contract

STATIC_RNG = 8888


def test_get_entrance_fee():
    if (network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENT):
        pytest.skip()

    lottery = deploy_lottery()
    entrance_fee = lottery.getEntranceFee()

    # 1 eth = $3000
    # $50 = 50 / 4000 = 1 / 60 = 0.016666666666666666

    assert entrance_fee > Web3.toWei(0.01, "ether")
    assert entrance_fee < Web3.toWei(0.02, "ether")


def test_cant_enter_unless_started():
    if (network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENT):
        pytest.skip()

    lottery = deploy_lottery()
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.enter(
            {"from": get_account(), "value": lottery.getEntranceFee()})


def test_can_start_and_enter_lottery():
    if (network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENT):
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    assert lottery.players(0) == account


def test_can_end_lottery():
    if (network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENT):
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    fund_with_link(lottery)
    lottery.endLottery({"from": account})
    assert lottery.lotteryState() == 2


def test_can_pick_winner_correctly():
    if (network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENT):
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()

    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    lottery.enter({"from": get_account(index=1),
                  "value": lottery.getEntranceFee()})
    lottery.enter({"from": get_account(index=2),
                  "value": lottery.getEntranceFee()})

    total_pot = lottery.balance()
    starting_account_balance = get_account(index=2).balance()

    fund_with_link(lottery)
    transaction = lottery.endLottery({"from": account})
    request_id = transaction.events["RequestedRandomness"]["requestId"]

    get_contract("vrf_coordinator").callBackWithRandomness(
        request_id, STATIC_RNG, lottery.address, {"from": account})

    # 8888 % 3 = 2
    assert lottery.recentWinner() == get_account(index=2)
    assert lottery.balance() == 0
    assert get_account(index=2).balance() == total_pot + \
        starting_account_balance
