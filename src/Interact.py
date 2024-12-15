import json
import os
from dotenv import load_dotenv
from web3 import Web3
from web3.exceptions import BadFunctionCallOutput, ContractLogicError

load_dotenv()

# Retrieve environment variables
ANVIL_ACCOUNT = "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"
ANVIL_PRIVATE_KEY = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
LOCAL_PROVIDER = "http://127.0.0.1:8545"

# Web3 connection
w3 = Web3(Web3.HTTPProvider(LOCAL_PROVIDER))

# Check if the Web3 connection is successful
if not w3.is_connected():
    print("Error: Unable to connect to Web3 provider!")
    exit(1)

# Load ABI
try:
    with open('newContract.abi', 'r') as abi_file:
        contract_abi = json.load(abi_file)
except FileNotFoundError:
    print("Error: ABI file not found!")
    exit(1)
except json.JSONDecodeError:
    print("Error: Failed to decode ABI JSON!")
    exit(1)

# Address of deployed contract (use Deploy.py to deploy and update the address here)
contract_address = "0x159252fDD59B0c883D35Cc5708bB5b23faEa87aA"

# Verify the contract address format
if not Web3.is_address(contract_address):
    print("Error: Invalid contract address format!")
    exit(1)

# Contract instance
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Function to check if the contract method works correctly
def check_contract_method():
    try:
        updated_value = contract.functions.viewMyId().call()
        print(f"Raw output from contract: {updated_value}")
    except BadFunctionCallOutput:
        print("Error: Bad output from the contract function.")
    except Exception as e:
        print(f"Error: {str(e)}")


# Function to interact with contract
def interact_with_contract():
    # Check the current StudentId
    check_contract_method()

    # Update the StudentId value to 5341
    try:
        update_txn = contract.functions.updateID(5341).build_transaction({
            "chainId": 31337,
            "from": ANVIL_ACCOUNT,
            "nonce": w3.eth.get_transaction_count(ANVIL_ACCOUNT),
            "gas": 200000,
            "gasPrice": w3.to_wei('50', 'gwei')
        })

        signed_update_txn = w3.eth.account.sign_transaction(update_txn, ANVIL_PRIVATE_KEY)
        update_tx_hash = w3.eth.send_raw_transaction(signed_update_txn.raw_transaction)
        print(f"Transaction hash: {update_tx_hash.hex()}")

        # Wait for the transaction receipt to confirm the update
        receipt = w3.eth.wait_for_transaction_receipt(update_tx_hash)
        print(f"Transaction receipt: {receipt}")

        # Try fetching the updated StudentId
        try:
            updated_value = contract.functions.viewMyId().call()
            print(f"Updated Student ID: {updated_value}")
        except Exception as e:
            print("Error:", str(e))
            if 'revert' in str(e):
                print(f"Revert reason: {str(e)}")

    except Exception as e:
        print(f"Error in contract interaction: {str(e)}")
        exit(1)


if __name__ == "__main__":
    interact_with_contract()
