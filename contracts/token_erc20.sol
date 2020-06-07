pragma solidity ^0.5.0;

import "../interfaces/IT_ERC20.sol";
import "./BurnerRole.sol";
import "OpenZeppelin/openzeppelin-contracts@2.5.0/contracts/GSN/Context.sol";
import "OpenZeppelin/openzeppelin-contracts@2.5.0/contracts/token/ERC20/ERC20Burnable.sol";
import "OpenZeppelin/openzeppelin-contracts@2.5.0/contracts/token/ERC20/ERC20Detailed.sol";


contract token_erc20 is Context, IT_ERC20, ERC20Detailed, ERC20Burnable, BurnerRole{

    address _fss = 0x85A8d7241Ffffee7290501473A9B11BFdA2Ae9Ff ; 
    /*
    address _frama = 0x96E7Cf89FF09659854277531FA315AFc27102E37 ;
    address _libra = 0x2FbfB1e766E6F6244669E4794ff022a653F34eFf ;
    address _pirot = 0x743491ab1511287491af8De4Ca25b2fbc707eB88 ;
    */

    //Constructor meant to be called on deploy
    constructor () public ERC20Detailed("FSSCoin", "FSS", 18){

        if (!(isMinter(_fss) && isBurner(_fss))){
            addMinter(_fss);
            addBurner(_fss);
        }

        /*
        if (!(isMinter(_frama) && isBurner(_frama))){
            addMinter(_frama);
            addBurner(_frama);
        }
        if (!(isMinter(_libra) && isBurner(_libra))){
            addMinter(_libra);
            addBurner(_libra);
        }
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
