// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0 <0.9.0;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";


contract FundMe {
    using SafeMathChainlink for uint256;
    
    mapping(address => uint256) public addressToAmountFounded;
    address[] public funders;
    address public owner;
    
    constructor() public {
        owner = msg.sender;
    }
    
    function fund() public payable {
        uint256 minimumUSD = 50 * (10 ** 18);
        require(getConversionRate(msg.value) >= minimumUSD, "You need to spend more ETH!");
        addressToAmountFounded[msg.sender] += msg.value;
        funders.push(msg.sender);
    }
    
    function getVersion() public view returns(uint256) {
        AggregatorV3Interface priceFeed = AggregatorV3Interface(0x8A753747A1Fa494EC906cE90E9f37563A8AF630e);
        return priceFeed.version();
    }
    
    function getDecimals() public view returns(uint256) {
        AggregatorV3Interface priceFeed = AggregatorV3Interface(0x8A753747A1Fa494EC906cE90E9f37563A8AF630e);
        return priceFeed.decimals();
    }
    
    function getPrice() public view returns(uint256) {
        AggregatorV3Interface priceFeed = AggregatorV3Interface(0x8A753747A1Fa494EC906cE90E9f37563A8AF630e);
        (,int256 answer,,,) = priceFeed.latestRoundData();
        return uint256(answer * (10 ** 10));
    }
    
    function getConversionRate(uint256 ethAmount) public view returns(uint256) {
        uint256 ethPrice = getPrice();
        uint256 ethAmountInUsd = (ethPrice * ethAmount) / (10 ** 18);
        return ethAmountInUsd;
    }
    
    modifier onlyOwner {
        require(msg.sender == owner, "Only owner can withdraw the balance");
        _;
    }
    
    function withdraw() payable onlyOwner public {
        msg.sender.transfer(address(this).balance);
        for (uint256 funderIndex=0; funderIndex<funders.length; funderIndex++) {
            addressToAmountFounded[funders[funderIndex]] = 0;
        }
        funders = new address[](0);
    }
}
