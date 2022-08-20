#!/usr/bin/python3
import pytest
from brownie import NarfexToken, accounts


# clean chain for each function, ensures clean working environment
@pytest.fixture(autouse=True)
def isolate(fn_isolation):
    pass


@pytest.fixture(scope="module")
def token():
    # no arguments for NarfexToken
    return accounts[0].deploy(NarfexToken)
