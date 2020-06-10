pragma solidity ^0.5.0;


import "./PayCoin.sol";
import "../interfaces/IT_ERC20.sol";
import "./token_erc20.sol";
import "./BrokerRole.sol";
import "./AdminRole.sol";

contract token_exchange is BrokerRole, AdminRole {
    using SafeMath for uint256;
    using SafeMath for int256; 

    IT_ERC20 public token;
    IT_PayCoin public payCoin;

    uint256 private tk_price;
    uint256 private _openingtime;
    uint256 private _closingtime;
    uint8 public _overnightCalls; 

    uint256[] priceHistory;

    //address _addressPC ;
    //= 0xc429620C4451d820B96FD3E5209FADa0F5a89852
    /*
    address _frama = 0x96E7Cf89FF09659854277531FA315AFc27102E37 ;
    address _libra = 0x2FbfB1e766E6F6244669E4794ff022a653F34eFf ;
    address _pirot = 0x743491ab1511287491af8De4Ca25b2fbc707eB88 ;
    */

    address _fss = 0x85A8d7241Ffffee7290501473A9B11BFdA2Ae9Ff ; 

    event Buy(address indexed buyer, uint256 indexed amount, uint256 indexed price);
    event Sell(address indexed buyer, uint256 indexed amount, uint256 indexed price);
    event PriceChange(address indexed changer, uint256 indexed id_price, uint256 indexed price); 
    event ChangeStart(address indexed who, uint256 indexed when); 
    event ChangeEnd(address indexed who, uint256 indexed when); 

    modifier onlyWhileOpen {
        require(isOpen(), "Market is closed");
        _;
    }

    constructor() public {

        token = new token_erc20();
        payCoin = new PayCoin();

        tk_price = 1e18 ; //accounts for PayCoin's decimals
        priceHistory.push(tk_price);

        _openingtime = now ;
        _closingtime = now + 1 hours ; //TODO Remember to modify it!
        _overnightCalls = 0; 

        if (!(isAdmin(_fss) && isBroker(_fss))){
            addAdmin(_fss);
            addBroker(_fss);
        }
        /*
        if (!(isAdmin(_frama) && isBroker(_frama))){
            addAdmin(_frama);
            addBroker(_frama);
        }
        if (!(isAdmin(_libra) && isBroker(_libra))){
            addAdmin(_libra);
            addBroker(_libra);
        }
        if (!(isAdmin(_pirot) && isBroker(_pirot))){
            addAdmin(_pirot);
            addBroker(_pirot);
        }
        */
        emit ChangeStart(_msgSender(), _openingtime); 
        emit ChangeEnd(_msgSender(), _closingtime + 7 days); 
    }

    function buy(uint256 tokenAmount) external onlyWhileOpen returns (bool){
        /*
        require(msg.value > 0, "You have to pay, my friend");
        require(msg.value == getFee(tokenAmount), "That's not enough money!");
        */
        //require(!(token.isMinter(_msgSender())), "You can't buy your own tokens, my friend");

        _buy(_msgSender(), tokenAmount.mul(10**uint256(token.decimals())));

        return true;
    }

    function sell(uint256 tokenAmount) external onlyWhileOpen returns (bool){
        /*
        require(msg.value > 0, "You have to pay, my friend");
        require(msg.value == getFee(tokenAmount), "That's not enough money!");
        */
        //require(!(token.isMinter(_msgSender())), "You can't buy your own tokens, my friend");

        _sell(_msgSender(), tokenAmount.mul(10**uint256(token.decimals())));

        return true;
    }

    function _buy(address recipient, uint256 amount) internal {
        // TODO set real address of the team
        payCoin.transferFrom(recipient, address(this), getFee(amount, true));

        token.mint(recipient, amount);

        emit Buy(recipient, amount, tk_price);
    }

    function _sell(address seller, uint256 amount) internal {
        // token_exchange != team, so it can mint paycoin (these doesn't count vs initial 50k)

        token.burnFrom(seller, amount);

        payCoin.mint(seller,getFee(amount, false));

        emit Sell(address(this), amount, tk_price);
    }

    function getFee(uint256 amount, bool from_buy) public returns (uint256){
        // amount * tk_price / 10^18 +- 2*amount/1000
        uint256 exp = uint256(token.decimals());

        if (from_buy){
            return amount.mul(tk_price).div(10**exp).add(amount.mul(2).div(1000));
        }
        else{
            return amount.mul(tk_price).div(10**exp).sub(amount.mul(2).div(1000));
        }

    }

    function isOpen() public view returns (bool) {
        return now >= _openingtime && now <= _closingtime;
    }

    function setOpenTime() external onlyAdmin {
        require(_openingtime < _closingtime, "Something's wrong, maybe you set the initial _openingtime wrong.");
        _openingtime = _closingtime.add(15 hours) ;
        _closingtime = _openingtime.add(9 hours) ;
    }

    function lastPrice() external view returns (uint256, uint256){
        return (priceHistory.length.sub(1), priceHistory[priceHistory.length.sub(1)]);
    }

    function getHistory(uint256 id_price) external view returns (uint256){
        return priceHistory[id_price] ;        
    }

    function setHistory(uint256 price) onlyBroker public {
        priceHistory.push(price); 
    }

    function setNewPrice(int256 delta_price) onlyBroker public returns (uint256) {
        uint256 last_price = priceHistory[priceHistory.length.sub(1)]; 
        int256 new_price = int256(last_price) + delta_price; 
        uint256 last_id_price; 

        require (new_price > 0, "Price must be positive!"); 
        
        if (isAdmin(_msgSender())) {
            require(isOpen(), "Market is closed"); 
            
            setHistory(uint256(new_price));
            last_id_price = priceHistory.length.sub(1);
            
            emit PriceChange(_msgSender(), last_id_price, uint256(new_price)); 
        }
        else{
            require(_overnightCalls < 4, "Already calls 4 times this night."); 
            require( uint256(new_price) > last_price.sub(last_price.mul(10).div(100)) && uint256(new_price) < last_price.add(last_price.mul(10).div(100)), "Can't change more than -+10%" ); 
            
            setHistory(uint256(new_price));
            last_id_price = priceHistory.length.sub(1);
            
            _overnightCalls += 1; 
        }

        return last_id_price; 
    }



}
