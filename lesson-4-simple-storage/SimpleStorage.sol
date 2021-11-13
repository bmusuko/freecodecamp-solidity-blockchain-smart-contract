// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;

contract SimpleStorage {
    uint256 myNumber;

    function store(uint256 _myNumber) public returns (uint256) {
        myNumber = _myNumber;
        return _myNumber;
    }

    function retrieve() public view returns (uint256) {
        return myNumber;
    }

    struct People {
        uint256 number;
        string name;
    }

    People[] public people;
    mapping(string => uint256) public nameToFavoriteNumber;

    function addPerson(uint256 _number, string memory _name) public {
        people.push(People({number: _number, name: _name}));
        nameToFavoriteNumber[_name] = _number;
    }
}
