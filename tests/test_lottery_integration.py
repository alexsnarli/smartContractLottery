from brownie import network
import pytest
import time

from scripts.deploy import deploy_lottery
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
    fund_with_link,
)


def test_can_pick_winner():
    # Skip this test if we are not testing on local blockchain
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

    # Arrange
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee() + 100000})
    lottery.enter({"from": account, "value": lottery.getEntranceFee() + 100000})
    fund_with_link(lottery)

    lottery.endLottery({"from": account})
    time.sleep(180)

    # Assert
    assert lottery.recentWinner() == account
    assert lottery.balance() == 0
