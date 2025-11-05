import json
import pathlib
from web3 import Web3

ROOT = pathlib.Path(__file__).resolve().parents[3]  # MEDITRACK/
CONTRACT_JSON = ROOT / "backend" / "app" / "blockchain" / "contract.json"

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
if not w3.is_connected():
    raise RuntimeError("Cannot connect to Ganache at http://127.0.0.1:7545")

# Load contract info
with open(CONTRACT_JSON, "r", encoding="utf-8") as f:
    info = json.load(f)

CONTRACT_ADDRESS = Web3.to_checksum_address(info["address"])
ABI = info["abi"]

contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)

# Use the first Ganache account (unlocked) as sender
SENDER = w3.eth.accounts[0]
w3.eth.default_account = SENDER


def add_record_hex(record_hash_hex: str) -> dict:
    """
    Accepts a SHA-256 hex string (with or without 0x),
    converts to bytes32, and sends a transaction to addRecord(bytes32).
    Returns tx receipt dict.
    """
    rh = record_hash_hex
    if rh.startswith("0x"):
        rh_hex = rh
    else:
        rh_hex = "0x" + rh

    # ✅ FIX: use bytes.fromhex() instead of deprecated w3.toBytes()
    record_bytes = bytes.fromhex(rh_hex.replace("0x", ""))
    if len(record_bytes) != 32:
        raise ValueError("record hash must be 32 bytes (SHA-256)")

    tx_hash = contract.functions.addRecord(record_bytes).transact({"from": SENDER})
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    return {
        "tx_hash": receipt.transactionHash.hex(),
        "blockNumber": receipt.blockNumber,
        "status": receipt.status,
    }


def verify_record_hex(record_hash_hex: str) -> bool:
    rh = record_hash_hex
    if not rh.startswith("0x"):
        rh = "0x" + rh

    # ✅ FIX: same here
    record_bytes = bytes.fromhex(rh.replace("0x", ""))
    return contract.functions.verifyRecord(record_bytes).call()
