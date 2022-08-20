// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

import "openzeppelin-contracts/contracts/token/ERC20/ERC20.sol";
import "openzeppelin-contracts/contracts/access/Ownable.sol";
import "openzeppelin-contracts/contracts/utils/math/SafeMath.sol";

contract Token is ERC20, Ownable {
    using SafeMath for uint256;
    uint256 public _maxTokens;
    uint256 public totalTokens;
    uint256 public _price;
    uint8 private _decimals;
    string private _symbol;
    string private _name;

    constructor() ERC20(_name, _symbol) {
        _name = "Token";
        _symbol = "Test";
        _maxTokens = 100000000000000000000;
        totalTokens = 0;
        _price = 100000000000000000;
    }

    function mint(uint256 amount) public {
        _mint(msg.sender, amount);
        totalTokens += amount;
    }

    function burn(address account, uint256 amount) public onlyOwner {
        _burn(account, amount);
        totalTokens -= amount;
    }

    function buy(uint256 amount, address account) public payable {
        uint256 weiAmount = msg.value;
        require(account != address(0), "Receiver is the zero address");
        require(
            totalSupply() + weiAmount < _maxTokens,
            "Exceeded amount of tokens"
        );
        require(weiAmount >= amount * _price, "Exceed BNB balance");
        _mint(account, amount);
        totalTokens += amount;
    }
}
