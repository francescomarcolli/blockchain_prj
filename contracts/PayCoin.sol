pragma solidity ^0.5.0;

import "OpenZeppelin/openzeppelin-contracts@2.5.0/contracts/GSN/Context.sol";
//import "./contracts/token/ERC20/IERC20.sol";
import "OpenZeppelin/openzeppelin-contracts@2.5.0/contracts/math/SafeMath.sol";
import "./BurnerRole.sol";
import "OpenZeppelin/openzeppelin-contracts@2.5.0/contracts/token/ERC20/ERC20Detailed.sol";
import "OpenZeppelin/openzeppelin-contracts@2.5.0/contracts/token/ERC20/ERC20Burnable.sol";
import "OpenZeppelin/openzeppelin-contracts@2.5.0/contracts/token/ERC20/ERC20Mintable.sol";

contract PayCoin is ERC20Detailed, ERC20Mintable, ERC20Burnable, BurnerRole {
    using SafeMath for uint256;

    constructor() public ERC20Detailed("Paycoin", "PaC", 18){
    }
}