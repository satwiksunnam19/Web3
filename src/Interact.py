import json
import os
from dotenv import load_dotenv
from web3 import Web3

load_dotenv()

# Environment variables
ANVIL_ACCOUNT = os.getenv("ANVIL_ACCOUNT")
ANVIL_PRIVATE_KEY = os.getenv("ANVIL_PRIVATE_KEY")
LOCAL_PROVIDER = os.getenv("LOCAL_PROVIDER")

# Web3 connection
w3 = Web3(Web3.HTTPProvider(LOCAL_PROVIDER))

# Load ABI
with open('newContract.abi', 'r') as abi_file:
    contract_abi = json.load(abi_file)

# Address of deployed contract (use Deploy.py to deploy and update the address here)
contract_address = "0xDc64a140Aa3E981100a9becA4E685f962f0cF6C9"

# Connect to the deployed contract
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

def interact_with_contract():
    # Update the StudentId value to 5341
    update_txn = contract.functions.updateID(5341).build_transaction({
        "chainId": 31337,
        "from": ANVIL_ACCOUNT,
        "nonce": w3.eth.get_transaction_count(ANVIL_ACCOUNT),
        "gas": 200000,
        "gasPrice": w3.to_wei('50', 'gwei')
    })
    
    signed_update_txn = w3.eth.account.sign_transaction(update_txn, ANVIL_PRIVATE_KEY)
    update_tx_hash = w3.eth.send_raw_transaction(signed_update_txn.raw_transaction)
    w3.eth.wait_for_transaction_receipt(update_tx_hash)
    
    # Fetch the updated StudentId
    updated_value = contract.functions.viewMyId().call()
    print(f"Updated value is {updated_value}")

if __name__ == "__main__":
    interact_with_contract()
