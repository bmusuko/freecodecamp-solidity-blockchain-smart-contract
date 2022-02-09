from brownie import network
from scripts.utils import LOCAL_BLOCKCHAIN_ENVIRONMENT, get_account, fund_with_link
import pytest
from scripts.deploy_lottery import deploy_lottery
import time


def test_can_pick_winner():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENT:
        pytest.skip()

    lottery = deploy_lottery()
    account = get_account()

    tx = lottery.startLottery({"from": account})
    tx.wait(1)
    tx = lottery.enter(
        {"from": account, "value": lottery.getEntranceFee()})
    tx.wait(1)
    tx = lottery.enter(
        {"from": account, "value": lottery.getEntranceFee()})
    tx.wait(1)

    fund_with_link(lottery)
    tx = lottery.endLottery({"from": account})
    tx.wait(1)

    # wait vrf callback (longer depends on network)
    time.sleep(300)

    assert lottery.recentWinner() == account
    assert lottery.balance() == 0
