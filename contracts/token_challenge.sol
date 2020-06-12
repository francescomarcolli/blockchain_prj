pragma solidity ^0.5.0;

import "./token_exchange.sol" ; 
import "./TeamRole.sol" ; 

contract token_challenge is AdminRole, TeamRole {

    //address _exchangeAddress; 
    address _fss = 0x85A8d7241Ffffee7290501473A9B11BFdA2Ae9Ff ;

    //EXCHANGE & PAYCOIN
    token_exchange fss_exchange; 
    IT_PayCoin payCoin; 

    //SIGNING UP & CHECKING VARIABLES
    address[] _teamAddresses; 

    event Registered(address indexed teamAddress); 

    //PRICE OVERNIGHT VARIABLES
    uint256 _last_id_price; 
    uint256 _startOvernightChallenge;
    bool _overnightWon; 
    
    event Overnight(address indexed winner, uint256 indexed coin_won); 

    //DIRECT CHALLENGE VARIABLES
    uint256[] _directFlag; 
    //uint256 _startDirectChallenge; 
    address _directChallenger; 
    address _directChallenged; 
    //bool _directChallengeWon;
    mapping (uint256 => bool) _directChallengeWon;
    mapping (uint256 => uint256) _startDirectChallenge; 

    event DirectChallenge(address indexed directChallenger, address indexed directChallenged, uint256 directFlag); 
    event DirectChallengeWon(address indexed directWinner, uint256 indexed directFlag, uint256 indexed coin_amount); 

    //TEAM CHALLENGE VARIABLES
    uint256[] _teamFlag; 
    address _teamChallenger; 
    address[] _teamChallenged;
    
    mapping (uint256 => uint256) _startTeamChallenge; 
    mapping (uint256 => bool) _teamChallengeWon; 
    
    event TeamChallenge(address indexed teamChallenger, uint256 teamFlag);
    event TeamChallengeWon(address indexed teamWinner, uint256 indexed teamFlag, uint256 indexed coin_amount);  

    //CONSTRUCTOR
    constructor (address exchangeAddress) public {
        fss_exchange = token_exchange(exchangeAddress);
        payCoin = IT_PayCoin(fss_exchange.payCoin());
    }

    //SIGNING UP & CHECKING FUNCTIONS
    function register(address teamAddress) external {
        //token_exchange fss_exchange = token_exchange(_exchangeAddress);
        bool _alreadyRegistered = false; 

        //TODO: Remember to uncomment!
        //require(!(fss_exchange.isOpen()), "The market is still open, come back later");

        for(uint256 i = 0; i < _teamAddresses.length; i++){
            if(_teamAddresses[i] == teamAddress){
                _alreadyRegistered = true; 
            }
        }
        require(_alreadyRegistered == false, "You're already registered."); 

        _teamAddresses.push(teamAddress); 
        if(!(isTeam(teamAddress))){
            addTeam(teamAddress);
        }
         
        require(_teamAddresses.length <= 3, "Too many teams."); 
        
        emit Registered(teamAddress); 
    }

    function isRegistered(address teamAddress) external view returns(bool){
        for(uint256 i = 0; i < _teamAddresses.length; i++){
            if(_teamAddresses[i] == teamAddress){
                return true; 
            }
        }
    return false; 
    }

    //PRICE OVERNIGHT

    function overnightStart(int256 new_delta_price) onlyAdmin external {
        //token_exchange fss_exchange = token_exchange(_exchangeAddress); 
        //IT_PayCoin payCoin = IT_PayCoin(fss_exchange.payCoin());

        //TODO: Remember to uncomment!
        //require(!(fss_exchange.isOpen()), "The market is still open, come back later");
        
        _startOvernightChallenge = now; 
        _last_id_price = fss_exchange.setNewPrice(new_delta_price);
        _overnightWon = false;  
        payCoin.burnFrom(msg.sender, 200e18); 

    }

    function overnightCheck(uint256 id_price) external {
        //token_exchange fss_exchange = token_exchange(_exchangeAddress); 
        //IT_PayCoin payCoin = IT_PayCoin(fss_exchange.payCoin());

        require(id_price == _last_id_price, "Wrong id price."); 
        if( now > _startOvernightChallenge && now < _startOvernightChallenge + 1 minutes){
            require(_overnightWon == false, "The challenge has already been won."); 

            payCoin.mint(msg.sender, 1200e18); 
            _overnightWon = true;
            emit Overnight(msg.sender, 1200e18); 

        }

        else{
            payCoin.mint(_fss, 2000e18); 
            emit Overnight(_fss, 2000e18); 
        }
        
    }

    //DIRECT CHALLENGE
    
    function challengeStart(address directChallenged, uint256 flag) external {
        //token_exchange fss_exchange = token_exchange(_exchangeAddress); 
        //IT_PayCoin payCoin = IT_PayCoin(fss_exchange.payCoin());
        /*
        for(uint256 i = 0; i < _directFlag.length; i++){
            require(_directFlag[i] != flag , "Flag already used!");
        }
        */
        checkFlag(_directFlag, flag); 

        require(msg.sender != directChallenged, "The addresses must be different."); 
        //TODO require address must be of the teams. 

        //_directFlag.push(flag); 
        _startDirectChallenge[flag] = now;
        _directChallenger = msg.sender; 
        _directChallenged = directChallenged; 
        _directChallengeWon[flag] = false; 

        emit DirectChallenge(_directChallenger, _directChallenged, flag);
        payCoin.burnFrom(msg.sender, 50e18);          
    
    }

    function winDirectChallenge(uint256 flag) external returns(bool) {
        //token_exchange fss_exchange = token_exchange(_exchangeAddress); 
        //IT_PayCoin payCoin = IT_PayCoin(fss_exchange.payCoin());
        bool _flagFound = false; 

        payCoin.burnFrom(msg.sender, 50e18);
        
        require(msg.sender == _directChallenger || msg.sender == _directChallenged, "You must be either the challenger or the challenged."); 
        if(now >= _startDirectChallenge[flag] + 5 seconds){ //REMEMBER TO CHANGE BACK TO MINUTES!
            require(_directChallengeWon[flag] == false, "The challenge has already been won."); 
            /*
            for(uint256 i = 0; i < _directFlag.length; i++){
                //require( _flag[i] == flag , "Couldn't find yuor flag!");
                if (_directFlag[i] == flag ){
                    _flagFound = true; 
                    break; 
                }
            }
            require(_flagFound, "Couldn't find yuor flag!"); 
            */
            matchFlag(_directFlag, flag); 

            payCoin.mint(msg.sender, 1000e18);
            emit DirectChallengeWon(msg.sender, flag, 1000e18); 
            _directChallengeWon[flag] = true;  

            return true; 
        } 
        else{
            return false; 
        }

    }
    
    //TEAM CHALLENGE
    
    function challengeStart(uint256 flag) onlyTeam external {
        //token_exchange fss_exchange = token_exchange(_exchangeAddress); 
        //IT_PayCoin payCoin = IT_PayCoin(fss_exchange.payCoin());
        /*
        for(uint256 i = 0; i < _teamFlag.length; i++){
            require(_teamFlag[i] != flag , "Flag already used!");
        } 
        */
        //TODO require address must be of the teams.

        //_teamFlag.push(flag); 
        checkFlag(_teamFlag, flag); 

        _startTeamChallenge[flag] = now;
        _teamChallengeWon[flag] = false; 

        require(_teamAddresses.length == 3, "Challenge can't start until all teams regitered."); 
        for(uint256 i = 0; i < _teamAddresses.length; i++){
            if(msg.sender == _teamAddresses[i]){
                _teamChallenger = msg.sender; 
            }
            else{
                _teamChallenged.push(_teamAddresses[i]); 
            }
        }

        emit TeamChallenge(msg.sender, flag); 

        payCoin.burnFrom(msg.sender, 100e18); 

    }

    function winTeamChallenge(uint256 flag) onlyTeam external returns(bool) {
        //token_exchange fss_exchange = token_exchange(_exchangeAddress); 
        //IT_PayCoin payCoin = IT_PayCoin(fss_exchange.payCoin());    
        bool _flagFound = false; 

        payCoin.burnFrom(msg.sender, 100e18);

        //require(msg.sender == _teamChallenger || msg.sender == _teamChallenged[0] || msg.sender == _teamChallenged[1], "You must be either the challenger or one fo the challenged."); 
        if(now >= _startTeamChallenge[flag] + 5 seconds){//REMEMBER TO CHANGE BACK TO MINUTES!
            require(_teamChallengeWon[flag] == false, "The challenge has already been won."); 
            /*
            for(uint256 i = 0; i < _teamFlag.length; i++){
                //require( _flag[i] == flag , "Couldn't find yuor flag!");
                if (_teamFlag[i] == flag ){
                    _flagFound = true; 
                    break; 
                }
            }
            require(_flagFound, "Couldn't find yuor flag!"); 
            */
            matchFlag(_teamFlag, flag); 

            if(msg.sender == _teamChallenger){
                payCoin.mint(msg.sender, 1500e18);
                emit TeamChallengeWon(msg.sender, flag, 1500e18);
            }
            else{
                payCoin.mint(msg.sender, 1000e18);
                emit TeamChallengeWon(msg.sender, flag, 1000e18);
            }
             
            _teamChallengeWon[flag] = true;  

            return true; 
        } 
        else{
            return false; 
        }
    }


    //INTERNAL FUNCTION

    function checkFlag(uint256[] storage _flags, uint256 _flag) internal {

        for(uint256 i = 0; i < _flags.length; i++){
            require(_flags[i] != _flag , "Flag already used!");
        }

        _flags.push(_flag);

    }

    function matchFlag(uint256[] storage _flags, uint256 _flag) internal {
        bool _flagFound = false;

        for(uint256 i = 0; i < _flags.length; i++){
                //require( _flag[i] == flag , "Couldn't find yuor flag!");
                if (_flags[i] == _flag ){
                    _flagFound = true; 
                    break; 
                }
            }
            require(_flagFound, "Couldn't find yuor flag!");

    }






    //EXCHANGE & PAYCOIN ADDRESS
    /*
    function setExchange(address exchangeAddress) onlyAdmin external {
        fss_exchange = token_exchange(exchangeAddress); 
    }
    
    function setPayCoin(address payCoinAddress) onlyAdmin external {
        payCoin = IT_PayCoin(payCoinAddress); 
    }
    */

}