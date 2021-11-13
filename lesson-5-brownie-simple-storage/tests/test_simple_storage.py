from brownie import SimpleStorage, accounts


def test_initial_value():
    account = accounts[0]
    simple_storage = SimpleStorage.deploy({"from": account})
    starting_value = simple_storage.retrieve()
    expected_starting_value = 0
    assert starting_value == expected_starting_value


def test_store():
    account = accounts[0]
    simple_storage = SimpleStorage.deploy({"from": account})
    fav_number = 15
    store_txn = simple_storage.store(fav_number)
    store_txn.wait(1)
    updated_number = simple_storage.retrieve()
    assert updated_number == fav_number
