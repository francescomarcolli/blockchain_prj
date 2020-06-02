pragma solidity ^0.5.0;

import "OpenZeppelin/openzeppelin-contracts@2.5.0/contracts/GSN/Context.sol";
import "OpenZeppelin/openzeppelin-contracts@2.5.0/contracts/access/Roles.sol";

contract BrokerRole is Context {
    using Roles for Roles.Role;

    event BrokerAdded(address indexed account);
    event BrokerRemoved(address indexed account);

    Roles.Role private _brokers;

    constructor () internal {
        _addBroker(_msgSender());
    }

    modifier onlyBroker() {
        require(isBroker(_msgSender()), "BrokerRole: caller does not have the Broker role");
        _;
    }

    function isBroker(address account) public view returns (bool) {
        return _brokers.has(account);
    }

    function addBroker(address account) public onlyBroker {
        _addBroker(account);
    }

    function renounceBroker() public {
        _removeBroker(_msgSender());
    }

    function _addBroker(address account) internal {
        _brokers.add(account);
        emit BrokerAdded(account);
    }

    function _removeBroker(address account) internal {
        _brokers.remove(account);
        emit BrokerRemoved(account);
    }
}
