pragma solidity ^0.5.0;

import "./PayCoin.sol";
import "../interfaces/IT_PayCoin.sol"; 
import "./AdminRole.sol"; 

contract Lender is AdminRole {
    using SafeMath for uint256; 

    PayCoin payCoin;

    mapping (address=>uint256) _loan;
    mapping (address=>uint256) _debt;
    mapping (uint256=>uint256) _blockNumber; 
    mapping (uint256=>bool) _closed; 

    uint256[] _id_loan; 
    uint256 private _maxLoan = 250000; 

    event OpenLoan(address indexed who, uint256 indexed amount, uint256 indexed id_loan); 
    event CloseLoan(address indexed who, uint256 indexed id_loan); 

    constructor (address payCoinAddress) public {
        payCoin = PayCoin(payCoinAddress); 
    }

    function openLoan(uint256 amount) external returns(uint256) {
        uint256 _id ; 
        require(_loan[_msgSender()].add(amount) <= _maxLoan.mul(10**(uint256(payCoin.decimals()))), "Can't loan more than 250k totally."); 

        payCoin.mint(_msgSender(), amount); 

        _loan[_msgSender()] = _loan[_msgSender()].add(amount); 
        _debt[_msgSender()] = _debt[_msgSender()].add(amount); 
        
        _id = _id_loan.push(amount).sub(1); 
        _blockNumber[_id] = block.number; 
        _closed[_id] = false; 

        emit OpenLoan(_msgSender(), amount, _id);  

        return _id; 
    }

    function closeLoan(uint256 id_loan) external {
        require(_closed[id_loan] == false, "Loan already closed.");
        uint256 amount = _id_loan[id_loan]; 

        payCoin.burnFrom(_msgSender(), amount.add(getFee(amount, id_loan))); 
        _debt[_msgSender()] = _debt[_msgSender()].sub(amount); 

        _closed[id_loan] = true; 
        emit CloseLoan(_msgSender(), id_loan); 
    }

    function loanStatus(uint256 id_loan) external view returns(uint256, uint256){
        require(_closed[id_loan] == false, "Loan already closed.");
        return(_id_loan[id_loan], getFee(_id_loan[id_loan], id_loan)); 
    }
    /*
    function penalty(address teamAddress) onlyAdmin external returns(uint256) {
        //require(now >= "18 dell'ultimo giorno");
        payCoin.burnFrom(teamAddress, _debt[teamAddress].mul(15).div(10)); 
        return _debt[teamAddress].mul(15).div(10); 
    }
    */
    function getFee(uint256 amount, uint256 id_loan) internal view returns(uint256) {
        return amount.div(1000).mul(block.number.sub(_blockNumber[id_loan])).div(500); 
    }
    
}