pragma solidity ^0.5.0;

contract FaucetAdvance
{
    // mapping con tutti i conti
    mapping(address => uint256) internal balance; // indica quanto denaro possono ritirare

    //address payable private owner = msg.sender; 

   
    address payable private owner;

    constructor() public
    {
        owner=msg.sender;  //msg.sender qui coincide con chi ha fatto il deploy
    }

    event Refilled(address indexed receiver, address indexed sender, uint256 indexed amount );
    event Withdrawl(address indexed receiver, uint256 indexed amount );

    function withdraw(uint withdraw_amount) public
    {
        require (withdraw_amount <= balance[msg.sender], 'Too much');   //controllo sul credito presente sul conto
        balance[msg.sender]-=withdraw_amount;    // riscalamento (fatto prima di trasferire il denaro)
        msg.sender.transfer(withdraw_amount);   // trasferimento del denaro a chi l'ha richiesto
        emit Withdrawl(msg.sender,withdraw_amount);
    }

    function() external payable {} //se tengo funzione di fallback posso trasferire allo SC ehters utilizzando il metodo transfer

    function recharge(address payable account) public payable  //NB payable
    /* per inviare ether allo SC bisogna popolare il campo {'value': ______} alla chiamata della funzione (msg.value)*/
    {
        /* controllo che solo il proprietario possa ricaricare il conto dello SC e possa definire quanto ognuno può ritirare, e solo da qui. 
         Altrimenti esce.*/ 
        //Se si usa il campo {'from:'} msg.sender cambia e invio ethers dal wallet di msg.sender (se posso farlo)
        require (msg.sender==owner, 'Not the owner');        
        balance[account]+=msg.value;
        emit Refilled(account,msg.sender,msg.value);
    }

    function balanceOf(address account) external view returns (uint256)
    {
        return balance[account];
    }


}