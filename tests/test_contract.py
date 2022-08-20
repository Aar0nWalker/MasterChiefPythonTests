from brownie import MasterChef, accounts
from brownie import Token
from brownie.exceptions import *
from conftest import *
import time


def test_account_balance():
    balance = accounts[0].balance()
    accounts[0].transfer(accounts[1], "10 ether", gas_price=0)
    assert balance - "10 ether" == accounts[0].balance()


def test_correct_initial_balance(accounts, token, isolate):
    chef = MasterChef.deploy(token.address, 0, 0, 0, 0, 0, 0, 0, {
                             'from': accounts[0]})
    assert chef.balance() == "0 ether"


def test_narfex_mint(accounts, token, isolate):
    number_of_tokens = 100 * 10**18
    tx = token.mint(accounts[1], number_of_tokens, {'from': accounts[0]})
    tx.wait(1)


def test_get_narfex_left(accounts, token, isolate):
    chef = MasterChef.deploy(token.address, 0, 0, 0, 0, 0, 0, 0, {
                             'from': accounts[0]})
    number_of_tokens = 100 * 10**18
    tx = token.mint(chef.address, number_of_tokens, {'from': accounts[0]})
    tx.wait(1)

    wei = chef.getNarfexLeft({'from': accounts[0]})
    assert wei == number_of_tokens


def test_owner_withdraw_narfex(accounts, token, isolate):
    chef = MasterChef.deploy(token.address, 0, 0, 0, 0, 0, 0, 0, {
                             'from': accounts[0]})

    initial_contract_balance = chef.getNarfexLeft({'from': accounts[0]})
    number_of_tokens = 100 * 10**18

    token.mint(chef.address, number_of_tokens, {'from': accounts[0]})
    middle_contract_balance = chef.getNarfexLeft({'from': accounts[0]})

    # 0 = all narfex
    chef.withdrawNarfex(0, {'from': accounts[0]})
    final_contract_balance = chef.getNarfexLeft({'from': accounts[0]})

    assert initial_contract_balance == 0
    assert middle_contract_balance == number_of_tokens
    assert final_contract_balance == 0


def test_owner_can_withdraw_all(accounts, token, isolate):
    chef = MasterChef.deploy(token.address, 0, 0, 0, 0, 0, 0, 0, {
                             'from': accounts[0]})
    number_of_tokens = 100 * 10**18

    tx = token.mint(chef.address, number_of_tokens, {'from': accounts[0]})
    tx.wait(1)

    wei_before_transfer = chef.getNarfexLeft({'from': accounts[0]})
    tx = chef.withdrawNarfex(0, {'from': accounts[0]})
    tx.wait(1)

    assert wei_before_transfer == number_of_tokens
    assert chef.getNarfexLeft({'from': accounts[0]}) == 0


def test_owner_can_create_pool(accounts, token, isolate):
    chef = MasterChef.deploy(token.address, 0, 0, 0, 0, 0, 0, 0, {
                             'from': accounts[0]})
    tx = chef.createPool(accounts[1], 0, {'from': accounts[0]})
    tx.wait(1)
    print(tx)


def test_not_owner_cant_create_pool(accounts, token, isolate):
    chef = MasterChef.deploy(token.address, 0, 0, 0, 0, 0, 0, 0, {
                             'from': accounts[0]})
    try:
        tx = chef.createPool(accounts[1], 0, {'from': accounts[1]})
        tx.wait(1)
        assert False
    except VirtualMachineError:
        assert True


def test_user_can_deposit(accounts, token, isolate):
    # деплою MasterChef на NarfexToken
    chef = MasterChef.deploy(token.address, 0, 0, 0, 0, 0, 0, 0, {
                             'from': accounts[0]})
    pair = Token.deploy({'from': accounts[0]})
    # создаю пул из NarfexToken
    tx = chef.createPool(pair.address, 0, {'from': accounts[0]})
    tx.wait(1)
    # mint NarfexToken на account1
    number_of_tokens = 1 * 10**18
    pair.mint(number_of_tokens, {'from': accounts[1]})  
    pair.increaseAllowance(chef.address, number_of_tokens, {'from': accounts[1]})
    # делаю депозит в пул (LP_address, amount, рефералка)
    tx = chef.deposit(pair.address,
                      number_of_tokens,
                      '0x0000000000000000000000000000000000000000',
                      {'from': accounts[1]})

    tx.wait(1)
