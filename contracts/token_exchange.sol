pragma solidity ^0.5.0;


import "./PayCoin.sol";
import "../interfaces/IT_ERC20.sol";
import "./token_erc20.sol";
import "./BrokerRole.sol";
import "./AdminRole.sol";

contract token_exchange is BrokerRole, AdminRole {
    using SafeMath for uint256;

    IT_ERC20 public token;
    IT_PayCoin public payCoin;
    uint256 private tk_price;
    uint256 private _openingtime;
    uint256 private _closingtime;

    uint256[] priceHistory;

    //address _addressPC ;
    //= 0xc429620C4451d820B96FD3E5209FADa0F5a89852

    address _frama = 0x96E7Cf89FF09659854277531FA315AFc27102E37 ;
    address _libra = 0x2FbfB1e766E6F6244669E4794ff022a653F34eFf ;
    address _pirot = 0x743491ab1511287491af8De4Ca25b2fbc707eB88 ;

    event Buy(address indexed buyer, uint256 indexed amount, uint256 indexed price);
    event Sell(address indexed buyer, uint256 indexed amount, uint256 indexed price);

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
        // TODO Implement allowances for transferFrom
        // TODO set real address of the team
        payCoin.transferFrom(recipient, address(this), getFee(amount, true));

        token.mint(recipient, amount);

        emit Buy(recipient, amount, tk_price);
    }

    function _sell(address seller, uint256 amount) internal {
        // TODO: Implement allowances for transferFrom
        // token_exchange != team, so it can mint paycoin (these doesn't count vs initial 50k)

        token.burnFrom(seller, amount);

        payCoin.mint(seller,getFee(amount, false));

        emit Sell(address(this), amount, tk_price);
    }

    function getFee(uint256 amount, bool from_buy) public returns (uint256){
        // TODO: Implement different fees for buying and selling
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
    /*
        TODO What is id_prezzo?
            ** If integer (1, 2, 3, etc) maybe priceHistory should be an array ( priceHistory[] )
            If hash/something else, then mapping. So, we need two more global variables (last_price id and last_price)
    */

    function lastPrice() external view returns (uint256, uint256){
        return (priceHistory.length.sub(1), priceHistory[priceHistory.length.sub(1)]);
    }




}
