from brownie import accounts, config, SimpleStorage, network


def get_account():
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def deploy_simple_storage():
    account = get_account()
    simple_storage = SimpleStorage.deploy({"from": account})
    stored_value = simple_storage.retrieve()
    print(stored_value)
    txn = simple_storage.store(15, {"from": account})
    txn.wait(1)
    stored_value = simple_storage.retrieve()
    print(stored_value)


def main():
    deploy_simple_storage()