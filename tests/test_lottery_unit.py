from aiohttp import request
from brownie import Lottery, accounts, network, config, exceptions
from web3 import Web3
import pytest

from scripts.deploy import deploy_lottery
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
    fund_with_link,
    get_contract,
)


def test_get_entrance_fee():
    # Skip this test if we are not testing on local blockchain
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Arrange
    lottery = deploy_lottery()
    # Act
    # Expected value is starting value (2000usd / eth) / entrance fee in USD (50) = 0.025 eth
    expected_entrance_fee = Web3.toWei(0.025, "ether")
    entrance_fee = lottery.getEntranceFee()
    # Assert
    assert entrance_fee == expected_entrance_fee


def test_cant_enter_if_not_started():
    # Skip this test if we are not testing on local blockchain
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Arrange
    lottery = deploy_lottery()
    # Act + Assert
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.enter({"from": get_account(), "value": lottery.getEntranceFee() + 100})


def test_can_start_and_enter():
    # Skip this test if we are not testing on local blockchain
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Arrange
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})

    # Act
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})

    # Assert
    assert lottery.players(0) == account


def test_can_end_lottery():
    # Skip this test if we are not testing on local blockchain
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Arrange
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})

    # Act
    fund_with_link(lottery)
    lottery.endLottery({"from": account})

    assert lottery.lottery_state() == 2


def test_can_pick_winner_correctly():
    # Skip this test if we are not testing on local blockchain
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Arrange
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    lottery.enter({"from": get_account(index=1), "value": lottery.getEntranceFee()})
    lottery.enter({"from": get_account(index=2), "value": lottery.getEntranceFee()})
    fund_with_link(lottery)

    starting_balance_of_account = account.balance()
    starting_balance_of_lottery = lottery.balance()

    # Assert
    tx = lottery.endLottery({"from": account})
    request_id = tx.events["RequestedRandomness"]["requestId"]
    STATIC_RNG = 777
    get_contract("vrf_coordinator").callBackWithRandomness(
        request_id, STATIC_RNG, lottery.address, {"from": account}
    )

    # WinnerId will be 777 % 3 = 0, winner should be account
    assert lottery.recentWinner() == account
    assert lottery.balance() == 0
    assert account.balance() == (
        starting_balance_of_account + starting_balance_of_lottery
    )
