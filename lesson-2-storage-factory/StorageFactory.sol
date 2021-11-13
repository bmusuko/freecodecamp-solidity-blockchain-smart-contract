// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;

import "./SimpleStorage.sol";

contract StorageFactory {
    SimpleStorage[] public simpleStorages;
    
    function createSimpleStorageContract() public {
        SimpleStorage simpleStorage = new SimpleStorage();
        simpleStorages.push(simpleStorage);
    }
    
    function sfStore(uint256 _simpleStorageIndex, uint256 _simpleStorageNumber) public {
        SimpleStorage simpleStorage = SimpleStorage(address(simpleStorages[_simpleStorageIndex]));
        simpleStorage.store(_simpleStorageNumber);
    }
    
    function sfGet(uint256 _simpleStorageIndex) public view returns(uint256){
        SimpleStorage simpleStorage = SimpleStorage(address(simpleStorages[_simpleStorageIndex]));
        return simpleStorage.retrieve();
    }
}
