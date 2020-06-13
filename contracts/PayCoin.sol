pragma solidity ^0.5.0;

import "../interfaces/IT_PayCoin.sol";
import "./BurnerRole.sol";
import "OpenZeppelin/openzeppelin-contracts@2.5.0/contracts/GSN/Context.sol";
import "OpenZeppelin/openzeppelin-contracts@2.5.0/contracts/token/ERC20/ERC20Burnable.sol";
import "OpenZeppelin/openzeppelin-contracts@2.5.0/contracts/token/ERC20/ERC20Detailed.sol";


contract PayCoin is Context, IT_PayCoin, ERC20Detailed, ERC20Burnable, BurnerRole{

    address _superUser = 0x85A8d7241Ffffee7290501473A9B11BFdA2Ae9Ff ;
    //address _exchange = 0x5831dE8826c01CC7fB165b30D59356D9BA27886F ;

    //Constructor meant to be called on deploy
    constructor () public ERC20Detailed("PayCoin", "PaC", 18){
        
        if (!(isMinter(_superUser) && isBurner(_superUser))){
            addMinter(_superUser);
            addBurner(_superUser);
        }
        
        /*
        if (!(isMinter(_exchange) && isBurner(_exchange))){
            addMinter(_exchange);
            addBurner(_exchange);
        }
        */
    }

    function burn(uint256 amount) public onlyBurner {
        super.burn(amount);
    }

    function burnFrom(address account, uint256 amount) public onlyBurner{
        super.burnFrom(account, amount);
    }

}
