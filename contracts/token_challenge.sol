pragma solidity ^0.5.0;

// import "OpenZeppelin/openzeppelin-contracts@2.5.0/contracts/GSN/Context.sol";
import "./token_exchange.sol" ; 
import "./TeamRole.sol" ; 

contract token_challenge is AdminRole, TeamRole {

    //address _exchangeAddress; 
    address private _fss_admin = 0x2b177c1854DE132E96326B454055005E62feBDc7; 
    address private _fss_trading = 0x85A8d7241Ffffee7290501473A9B11BFdA2Ae9Ff ;

    //EXCHANGE & PAYCOIN
    token_exchange fss_exchange; 
    PayCoin payCoin; 

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
    address _directChallenger; 
    address _directChallenged; 
    
    mapping (uint256 => bool) _directChallengeWon;
    mapping (uint256 => uint256) _startDirectChallenge; 

    event DirectChallenge(address indexed challenger, address indexed challenged, uint256 _flag); 
    event DirectChallengeWon(address indexed winner, uint256 indexed _flag, uint256 indexed _amount); 

    //TEAM CHALLENGE VARIABLES
    uint256[] _teamFlag; 
    address _teamChallenger; 
    address[] _teamChallenged;
    
    mapping (uint256 => uint256) _startTeamChallenge; 
    mapping (uint256 => bool) _teamChallengeWon; 
    
    event TeamChallenge(address indexed challenger, uint256 _flag);
    event TeamChallengeWon(address indexed winner, uint256 indexed _flag, uint256 indexed _amount);  

    //CONSTRUCTOR
    constructor (address exchangeAddress, address payCoinAddress) public {
        fss_exchange = token_exchange(exchangeAddress);
        payCoin = PayCoin(payCoinAddress);

        if (!(isAdmin(_fss_admin))){
            addAdmin(_fss_admin);
        }

        if (!(isAdmin(_fss_trading))){
            addAdmin(_fss_trading);
        }

        _teamAddresses.push(_fss_trading); 

    }

    //SIGNING UP & CHECKING FUNCTIONS
    function register(address teamAddress) external {
        bool _alreadyRegistered = false; 

        require(!(fss_exchange.isOpen()), "The market is still open, come back later");

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
        require(!(fss_exchange.isOpen()), "The market is still open, come back later");
        
        _startOvernightChallenge = now; 
        _last_id_price = fss_exchange.setNewPrice(new_delta_price);
        _overnightWon = false;  
        payCoin.burnFrom(_msgSender(), 200e18); 

    }

    function overnightCheck(uint256 id_price) onlyTeam external {

        require(id_price == _last_id_price, "Wrong id price."); 
        if( now > _startOvernightChallenge && now < _startOvernightChallenge + 1 hours){
            require(_overnightWon == false, "The challenge has already been won."); 

            payCoin.mint(_msgSender(), 1200e18); 
            _overnightWon = true;
            emit Overnight(_msgSender(), 1200e18); 

        }

        else{
            payCoin.mint(_fss_trading, 2000e18); 
            emit Overnight(_fss_trading, 2000e18); 
        }
        
    }

    //DIRECT CHALLENGE
    
    function challengeStart(address directChallenged, uint256 flag) onlyTeam external {
        checkFlag(_directFlag, flag); 

        require(_msgSender() != directChallenged, "The addresses must be different.");  

        _startDirectChallenge[flag] = now;
        _directChallenger = _msgSender(); 
        _directChallenged = directChallenged; 
        _directChallengeWon[flag] = false; 

        emit DirectChallenge(_directChallenger, _directChallenged, flag);
        payCoin.burnFrom(_msgSender(), 50e18);          
    
    }

    function winDirectChallenge(uint256 flag) onlyTeam external returns(bool) {
        bool _flagFound = false; 

        payCoin.burnFrom(_msgSender(), 50e18);
        
        require(_msgSender() == _directChallenger || _msgSender() == _directChallenged, "You must be either the challenger or the challenged."); 
        if(now >= _startDirectChallenge[flag] + 5 minutes){ 
            require(_directChallengeWon[flag] == false, "The challenge has already been won."); 
    
            matchFlag(_directFlag, flag); 

            payCoin.mint(_msgSender(), 1000e18);
            emit DirectChallengeWon(_msgSender(), flag, 1000e18); 
            _directChallengeWon[flag] = true;  

            return true; 
        } 
        else{
            return false; 
        }

    }
    
    //TEAM CHALLENGE
    
    function challengeStart(uint256 flag) onlyTeam external {
    
        checkFlag(_teamFlag, flag); 

        _startTeamChallenge[flag] = now;
        _teamChallengeWon[flag] = false; 

        require(_teamAddresses.length == 3, "Challenge can't start until all teams regitered."); 
        for(uint256 i = 0; i < _teamAddresses.length; i++){
            if(_msgSender() == _teamAddresses[i]){
                _teamChallenger = _msgSender(); 
            }
            else{
                _teamChallenged.push(_teamAddresses[i]); 
            }
        }

        emit TeamChallenge(_msgSender(), flag); 

        payCoin.burnFrom(_msgSender(), 100e18); 

    }

    function winTeamChallenge(uint256 flag) onlyTeam external returns(bool) {    
        bool _flagFound = false; 

        payCoin.burnFrom(_msgSender(), 100e18);
 
        if(now >= _startTeamChallenge[flag] + 5 minutes){
            require(_teamChallengeWon[flag] == false, "The challenge has already been won."); 
        
            matchFlag(_teamFlag, flag); 

            if(_msgSender() == _teamChallenger){
                payCoin.mint(_msgSender(), 1500e18);
                emit TeamChallengeWon(_msgSender(), flag, 1500e18);
            }
            else{
                payCoin.mint(_msgSender(), 1000e18);
                emit TeamChallengeWon(_msgSender(), flag, 1000e18);
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
                if (_flags[i] == _flag ){
                    _flagFound = true; 
                    break; 
                }
            }
            require(_flagFound, "Couldn't find yuor flag!");

    }

    //EXCHANGE & PAYCOIN ADDRESS
    function setExchange(address exchangeAddress) onlyAdmin external {
        fss_exchange = token_exchange(exchangeAddress); 
    }
    
    function setPayCoin(address payCoinAddress) onlyAdmin external {
        payCoin = PayCoin(payCoinAddress); 
    }
    

}