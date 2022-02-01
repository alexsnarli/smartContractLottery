from brownie import Lottery, accounts, network, config
from web3 import Web3


def test_get_entrance_fee():
    account = accounts[0]
    lottery = Lottery.deploy(
        config["networks"][network.show_active()]["eth-usd-price-feed"],
        {"from": account},
    )
    entranceFee = lottery.getEntranceFee()

    # assert entranceFee > Web3.toWei(0.016, "ether")
    # assert entranceFee < Web3.toWei(0.020, "ether")
