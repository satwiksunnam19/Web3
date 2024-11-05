import json
from solcx import compile_source, install_solc, set_solc_version, get_installed_solc_versions

# Solidity source code for the contract
contract_source_code = '''
// SPDX-License-Identifier: MIT
pragma solidity 0.8.13;

contract newContract {
    uint public StudentId;
    address public owner;

    constructor() {
        StudentId = 10;
        owner = msg.sender;
    }

    function viewMyId() public view returns(uint) {
        return StudentId;
    }

    function updateID(uint _newId) public {
        require(msg.sender == owner);
        StudentId = _newId;
    }
}
'''

def compile_contract():
    # Specify the Solidity version to use
    solc_version = '0.8.13'

    # Check if the version is installed, and install if necessary
    if solc_version not in get_installed_solc_versions():
        print(f"Installing solc version {solc_version}...")
        install_solc(solc_version)
    set_solc_version(solc_version)

    # Compiling the contract
    compiled_sol = compile_source(contract_source_code)
    contract_interface = compiled_sol['<stdin>:newContract']
    
    # Save ABI and Bytecode
    with open('newContract.abi', 'w') as abi_file:
        json.dump(contract_interface['abi'], abi_file)
        
    with open('newContract.bin', 'w') as bin_file:
        bin_file.write(contract_interface['bin'])
        
    print("Contract compiled successfully, ABI and Bytecode saved.")
    return contract_interface['abi'], contract_interface['bin']

if __name__ == "__main__":
    compile_contract()
