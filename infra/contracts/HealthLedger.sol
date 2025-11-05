// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

contract HealthLedger {
    event HealthRecordAdded(address indexed user, bytes32 indexed recordHash, uint256 timestamp);

    mapping(bytes32 => bool) public exists;

    function addRecord(bytes32 recordHash) public {
        require(!exists[recordHash], "Already stored");
        exists[recordHash] = true;
        emit HealthRecordAdded(msg.sender, recordHash, block.timestamp);
    }

    function verifyRecord(bytes32 recordHash) public view returns (bool) {
        return exists[recordHash];
    }
}
