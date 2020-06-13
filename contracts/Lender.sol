pragma solidity ^0.5.0;

import "./PayCoin.sol";
import "../interfaces/IT_PayCoin.sol"; 
import "./AdminRole.sol"; 

contract Lender is AdminRole {
    using SafeMath for uint256; 

    IT_PayCoin payCoin;

    mapping (address=>uint256) _loan;
    mapping (address=>uint256) _debt;

    uint256[] _id_loan; 
    uint256 private _maxLoan = 250000; 
    //uint256 private _exp = 10**(uint256(payCoin.decimals()));
     

    event OpenLoan(address indexed who, uint256 indexed amount); 
    event CloseLoan(address indexed who); 

    constructor (address payCoinAddress) public {
        payCoin = IT_PayCoin(payCoinAddress); 
    }

    function openLoan(uint256 amount) external returns(uint256) {
        require(_loan[msg.sender].add(amount) <= _maxLoan.mul(10**(uint256(payCoin.decimals()))), "Can't loan more than 250k totally."); 

        payCoin.mint(msg.sender, amount); 

        _loan[msg.sender] = _loan[msg.sender].add(amount); 
        _debt[msg.sender] = _debt[msg.sender].add(amount); 

        emit OpenLoan(msg.sender, amount);  

        return _id_loan.push(amount).sub(1); 
    }

    function closeLoan(uint256 id_loan) external {
        uint256 amount = _id_loan[id_loan]; 

        payCoin.burnFrom(msg.sender, amount.add(getFee(amount))); 
        _debt[msg.sender] = _debt[msg.sender].sub(amount); 

        emit CloseLoan(msg.sender); 
    }

    function loanStatus(uint256 id_loan) external returns(uint256, uint256){
        return(_id_loan[id_loan], getFee(_id_loan[id_loan])); 
    }

    function penalty(address teamAddress) onlyAdmin external returns(uint256) {
        //require(now >= "18 dell'ultimo giorno");
        payCoin.burnFrom(teamAddress, _debt[teamAddress].mul(15).div(10)); 
        return _debt[teamAddress].mul(15).div(10); 
    }

    function getFee(uint256 amount) internal returns(uint256) {
        return amount.div(10).mul(block.number).div(500); 
    }
    
}