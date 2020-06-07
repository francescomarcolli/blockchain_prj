pragma solidity ^0.5.0;

import "./token_exchange.sol" ; 

contract token_challenge {

    address _exchangeAddress; 

    constructor (address exchangeAddress) public {
        _exchangeAddress = exchangeAddress; 
    }

    function overnightStart(int256 new_delta_price) public {
        uint256 last_id_price; 
        uint256 startChallenge; 
        token_exchange fss_exchange = token_exchange(_exchangeAddress); 
        
        require(!(fss_exchange.isOpen()), "The market is still open, come back later"); 

        startChallenge = now; 
        last_id_price = fss_exchange.setNewPrice(new_delta_price); 

    }


}