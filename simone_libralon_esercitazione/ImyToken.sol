
pragma solidity ^0.6.0;

interface ImyToken 
{
	function buyTkns(uint256 amount) external payable;

	function buyTkns() external payable;

	function getFee(uint256 amount) external view returns(uint256);
}