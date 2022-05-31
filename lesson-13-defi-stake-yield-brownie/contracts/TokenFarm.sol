// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract TokenFarm is Ownable {
    IERC20 public dappToken;

    mapping(address => bool) public allowedTokens;
    address[] public allowedTokensArr;

    mapping(address => mapping(address => uint256)) public stakingBalance;
    address[] public stakers;

    mapping(address => uint256) public uniqueTokensStaked;

    mapping(address => address) public tokenPriceFeedMapping;

    constructor(address _dappTokenAddress) {
        dappToken = IERC20(_dappTokenAddress);
    }

    function setPriceFeedContract(address _token, address _priceFeed)
        external
        onlyOwner
    {
        tokenPriceFeedMapping[_token] = _priceFeed;
    }

    function stakeTokens(uint256 _amount, address _token) external {
        require(_amount > 0, "Amount must be more than 0");

        require(tokenIsAllowed(_token), "Token must be allowed");

        IERC20(_token).transferFrom(msg.sender, address(this), _amount);
        updateUniqueTokenssStaked(msg.sender, _token);
        stakingBalance[_token][msg.sender] += _amount;
        if (uniqueTokensStaked[msg.sender] == 1) {
            stakers.push(msg.sender);
        }
    }

    function unstakeTokens(address _token) external {
        uint256 balance = stakingBalance[_token][msg.sender];
        require(balance > 0, "Staking balance must be greater than 0");
        // prone to re entrancy attack
        IERC20(_token).transfer(msg.sender, balance);
        stakingBalance[_token][msg.sender] = 0;
        uniqueTokensStaked[msg.sender]--;
    }

    function issueTokens() external onlyOwner {
        for (
            uint256 stakersIndex = 0;
            stakersIndex < stakers.length;
            stakersIndex++
        ) {
            address recipient = stakers[stakersIndex];
            // send token reward
            uint256 userTotalValue = getUserTotalValue(recipient);
            dappToken.transfer(recipient, userTotalValue);
        }
    }

    function getUserTotalValue(address _user) public view returns (uint256) {
        require(uniqueTokensStaked[_user] > 0, "No Token Staked");
        uint256 totalValue;
        for (
            uint256 allowedTokenIdx = 0;
            allowedTokenIdx < allowedTokensArr.length;
            allowedTokenIdx++
        ) {
            totalValue += getUserSingleTokenValue(
                _user,
                allowedTokensArr[allowedTokenIdx]
            );
        }
        return totalValue;
    }

    function getUserSingleTokenValue(address _user, address _token)
        public
        view
        returns (uint256)
    {
        if (stakingBalance[_token][_user] <= 0) {
            return 0;
        }

        (uint256 price, uint256 decimals) = getTokenValue(_token);
        return (stakingBalance[_token][_user] * price) / (10**decimals);
    }

    function getTokenValue(address _token)
        public
        view
        returns (uint256, uint256)
    {
        address priceFeedAddress = tokenPriceFeedMapping[_token];
        AggregatorV3Interface priceFeed = AggregatorV3Interface(
            priceFeedAddress
        );
        (, int256 price, , , ) = priceFeed.latestRoundData();
        uint256 decimals = uint256(priceFeed.decimals());
        return (uint256(price), decimals);
    }

    function addAllowedTokens(address _token) external onlyOwner {
        allowedTokens[_token] = true;
        allowedTokensArr.push(_token);
    }

    function updateUniqueTokenssStaked(address _user, address _token) internal {
        if (stakingBalance[_token][_user] >= 0) {
            uniqueTokensStaked[_user]++;
        }
    }

    // function removeAllowedTokens(address _token) public onlyOwner {
    //     allowedTokens[_token] = false;
    // }

    function tokenIsAllowed(address _token) public view returns (bool) {
        return allowedTokens[_token];
    }
}
