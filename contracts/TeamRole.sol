pragma solidity ^0.5.0;

import "OpenZeppelin/openzeppelin-contracts@2.5.0/contracts/GSN/Context.sol";
import "OpenZeppelin/openzeppelin-contracts@2.5.0/contracts/access/Roles.sol";

contract TeamRole is Context {
    using Roles for Roles.Role;

    event TeamAdded(address indexed account);
    event TeamRemoved(address indexed account);

    Roles.Role private _teams;

    constructor () internal {
        _addTeam(_msgSender());
    }

    modifier onlyTeam() {
        require(isTeam(_msgSender()), "TeamRole: caller does not have the Team role");
        _;
    }

    function isTeam(address account) public view returns (bool) {
        return _teams.has(account);
    }

    function addTeam(address account) public onlyTeam {
        _addTeam(account);
    }

    function renounceTeam() public {
        _removeTeam(_msgSender());
    }

    function _addTeam(address account) internal {
        _teams.add(account);
        emit TeamAdded(account);
    }

    function _removeTeam(address account) internal {
        _teams.remove(account);
        emit TeamRemoved(account);
    }
}
