pragma solidity ^0.6.0;

import './ERC20Burnable.sol';
import './AccessControl.sol';

contract myToken is ERC20Burnable, AccessControl
{
	address payable	_owner;
	constructor() public ERC20('Libry', 'LBY')			//Imposto nome e simbolo, definisco l'owner del Tkn dal quale vengono distribuiti i Tkn e ha tutti i privilegi
	{
		_owner=_msgSender();
		_setupRole(DEFAULT_ADMIN_ROLE, _owner);
		_setupRole(MINTER_ROLE, _owner);
		_setupRole(BURNER_ROLE, _owner);
	}

	bytes32 private constant MINTER_ROLE = keccak256('MINTER_ROLE');
	bytes32 private constant BURNER_ROLE = keccak256('BURNER_ROLE');


	function MakeMinter(address account) public
	{
		_setupRole(MINTER_ROLE, account);
	}

	function MakeBurner(address account) public
	{
		_setupRole(MINTER_ROLE, account);
	}

	function Burn(address account, uint256 amount) external returns (bool)
	{
		require(hasRole(BURNER_ROLE, _msgSender()),'Not a burner');
		burnFrom(account, amount);
		return true;
	}

	function mint(address account, uint256 amount) external returns (bool)
	{
		require(hasRole(MINTER_ROLE, _msgSender()),'Not a minter');
		_mint(account,amount);
	}

}