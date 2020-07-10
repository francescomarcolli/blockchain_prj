pragma solidity ^0.6.0;

import './myToken.sol';
//import './TokenTimeLock.sol';


contract MyTokenBuy is myToken
{

	uint256 private _TknValue;
	uint256 private _TknMaxNum;
	address payable private _safe;
	
	uint256 private constant _TknBase = 1e18;
	bytes32 private constant SETVALUE_ROLE = keccak256('SETVALUE_ROLE');
	bytes32 private constant SETSAFE_ROLE = keccak256('SETSAFE_ROLE');

	mapping(address => uint256) TimeLimit;

	constructor(uint256 TknValue, uint256 TknMaxNum, address payable Safe) public myToken()
	{
		_TknValue=TknValue;
		_TknMaxNum=TknMaxNum;
		_safe=Safe;
		_mint(_owner,_TknBase);					//assegno all'owner una quantità di Tkn base
	}

	function setPrice(uint256 value) external returns (bool)
	{
		require(hasRole(SETVALUE_ROLE,_msgSender()),'Not autorized');
		_TknValue=value;
		return true;
	}

	function setSafe(address payable NewSafe) external returns (bool)  //definisce l'indirizzo "cassaforte", al quale vengono inviati i proventi della vendita dei Tkn
	{
		require(hasRole(SETSAFE_ROLE,_msgSender()),'Not autorized');
		_safe=NewSafe;
		return true;
	}

	function getFee(uint256 amount) external view returns(uint256)
	{
		return amount*_TknValue;
	}

	function BuyTkns(uint256 amount) external payable		//da popolare msg.value e from
	{
		_buyTkns(_owner,_msgSender(),amount);	//i Tkn vengono comprati dall'owner del contratto
		_safe.transfer(msg.value); 	//trasferimento del denaro alla cassaforte
	}

	function _buyTkns(address sender, address beneficiary, uint256 amount) internal
	{
		require(msg.value>=amount*_TknValue,'Not enough Ether to purchase Tkn');
		require(amount<=_TknMaxNum,'Too much Tkns requested');
		require(TimeLimit[beneficiary]+ 5 minutes <= block.timestamp ,'Wait 5 minutes at least to purchase again');  //setto il limite di tempo tra un acquisto e l'altro
		_transfer(_owner,_msgSender(),amount);
		TimeLimit[beneficiary]=block.timestamp;
	}

	function BuyTkns() external payable
	{
		uint256 NumTkns= msg.value / _TknValue;
		uint256 Change= msg.value % _TknValue;
		_buyTkns(_owner,_msgSender(),NumTkns);
		_msgSender().transfer(Change);
		_safe.transfer(msg.value-Change);
	}
}