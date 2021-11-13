from solcx import compile_standard, install_solc
import json
import os
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()
install_solc("0.6.0")

with open("./SimpleStorage.sol", "r") as f:
    simple_storage_file = f.read()

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)

# with open("compiled_code.json", "w") as f:
#     json.dump(compiled_sol, f)


bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# connecting to ganache
w3 = Web3(
    Web3.HTTPProvider(f"https://rinkeby.infura.io/v3/{os.getenv('INFURA_API_KEY')}")
)
chain_id = 4
account_address = os.getenv("PRIVATE_KEY")
private_key = os.getenv("ACCOUNT_ADDRESS")

# create the contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# get the latest transaction
nonce = w3.eth.getTransactionCount(account_address)

# build a transaction
# sign a transaction
# send a transaction
transaction = SimpleStorage.constructor().buildTransaction(
    {"chainId": chain_id, "from": account_address, "nonce": nonce}
)

signed_txn = w3.eth.account.sign_transaction(transaction, private_key)
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

# working with the contract
simple_storage_contract = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

# call to execute non modifying state function
print(simple_storage_contract.functions.retrieve().call())
store_transaction = simple_storage_contract.functions.store(15).buildTransaction(
    {
        "chainId": chain_id,
        "from": account_address,
        "nonce": w3.eth.getTransactionCount(account_address),
    }
)
signex_store_txn = w3.eth.account.sign_transaction(store_transaction, private_key)
store_tx_hash = w3.eth.send_raw_transaction(signex_store_txn.rawTransaction)
store_tx_receipt = w3.eth.wait_for_transaction_receipt(store_tx_hash)

# print(simple_storage_contract.functions.store(15).transact())
print(simple_storage_contract.functions.retrieve().call())
