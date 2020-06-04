pragma solidity ^0.5.0;

import "OpenZeppelin/openzeppelin-contracts@2.5.0/contracts/token/ERC20/IERC20.sol";
import "OpenZeppelin/openzeppelin-contracts@2.5.0/contracts/token/ERC20/ERC20Mintable.sol";

contract IT_PayCoin is IERC20, ERC20Mintable {

    function name() public view returns (string memory);

    function symbol() public view returns (string memory);

    function decimals() public view returns (uint8);

    function burn(uint256 amount) public;

    function burnFrom(address account, uint256 amount) public;

}
