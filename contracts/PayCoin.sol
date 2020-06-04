pragma solidity ^0.5.0;

import "../interfaces/IT_PayCoin.sol";
import "./BurnerRole.sol";
import "OpenZeppelin/openzeppelin-contracts@2.5.0/contracts/GSN/Context.sol";
import "OpenZeppelin/openzeppelin-contracts@2.5.0/contracts/token/ERC20/ERC20Burnable.sol";
import "OpenZeppelin/openzeppelin-contracts@2.5.0/contracts/token/ERC20/ERC20Detailed.sol";


contract PayCoin is Context, IT_PayCoin, ERC20Detailed, ERC20Burnable, BurnerRole{

    address _superUser = 0x743491ab1511287491af8De4Ca25b2fbc707eB88 ;
    address _exchange = 0x5831dE8826c01CC7fB165b30D59356D9BA27886F ;
    //address _pirot = 0x743491ab1511287491af8De4Ca25b2fbc707eB88 ;

    //Constructor meant to be called on deploy
    constructor () public ERC20Detailed("PayCoin", "PaC", 18){
        if (!(isMinter(_superUser) && isBurner(_superUser))){
            addMinter(_superUser);
            addBurner(_superUser);
        }
        if (!(isMinter(_exchange) && isBurner(_exchange))){
            addMinter(_exchange);
            addBurner(_exchange);
        }
        /*
        if (!(isMinter(_pirot) && isBurner(_pirot))){
            addMinter(_pirot);
            addBurner(_pirot);
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
