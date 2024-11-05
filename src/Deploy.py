import json
import os
from dotenv import load_dotenv
from web3 import Web3

# Load environment variables from .env file
load_dotenv()

# Retrieve environment variables
ANVIL_ACCOUNT = os.getenv("ANVIL_ACCOUNT")
ANVIL_PRIVATE_KEY = os.getenv("ANVIL_PRIVATE_KEY")
LOCAL_PROVIDER = os.getenv("LOCAL_PROVIDER")

# Debug: Verify environment variables
print("Environment variables loaded.")
print(f"ANVIL_ACCOUNT: {ANVIL_ACCOUNT}")  # Should print a valid address
print(f"ANVIL_PRIVATE_KEY: {ANVIL_PRIVATE_KEY}")  # Should print the private key
print(f"LOCAL_PROVIDER: {LOCAL_PROVIDER}")  # Should print the provider URL

# Check if variables are None
if not ANVIL_ACCOUNT or not ANVIL_PRIVATE_KEY or not LOCAL_PROVIDER:
    raise ValueError("One or more environment variables are not set correctly.")

# Initialize Web3 connection
w3 = Web3(Web3.HTTPProvider(LOCAL_PROVIDER))
chain_id = 31337  # Anvil's chain ID

# Load ABI and Bytecode
with open('newContract.abi', 'r') as abi_file:
    contract_abi = json.load(abi_file)

with open('newContract.bin', 'r') as bin_file:
    contract_bytecode = bin_file.read()

def deploy_contract():
    # Verify address format
    if not Web3.is_address(ANVIL_ACCOUNT):
        raise ValueError(f"Invalid address format: {ANVIL_ACCOUNT}")

    # Define the contract
    new_contract = w3.eth.contract(abi=contract_abi, bytecode=contract_bytecode)
    
    # Build transaction for deployment
    transaction = new_contract.constructor().build_transaction({
        "chainId": chain_id,
        "from": ANVIL_ACCOUNT,
        "nonce": w3.eth.get_transaction_count(ANVIL_ACCOUNT),
        "gas": 2000000,
        "gasPrice": w3.to_wei('50', 'gwei')  # Corrected here
    })
    
    # Sign and send transaction
    signed_txn = w3.eth.account.sign_transaction(transaction, ANVIL_PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    contract_address = tx_receipt.contractAddress
    print(f"Contract deployed at {contract_address}")
    return contract_address

if __name__ == "__main__":
    deploy_contract()
