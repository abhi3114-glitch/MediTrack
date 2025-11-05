import json
from web3 import Web3
from solcx import compile_standard, install_solc
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[3]  # points to MEDITRACK/
CONTRACT_PATH = ROOT / "infra" / "contracts" / "HealthLedger.sol"
OUT_JSON = ROOT / "backend" / "app" / "blockchain" / "contract.json"

# 1) Ensure solc is installed
print("Installing solc 0.8.17 (if not present)...")
install_solc("0.8.17")

# 2) Read Solidity source
with open(CONTRACT_PATH, "r", encoding="utf-8") as f:
    source = f.read()

compiled = compile_standard(
    {
        "language": "Solidity",
        "sources": {"HealthLedger.sol": {"content": source}},
        "settings": {"outputSelection": {"*": {"*": ["abi", "evm.bytecode"]}}},
    },
    solc_version="0.8.17",
)

abi = compiled["contracts"]["HealthLedger.sol"]["HealthLedger"]["abi"]
bytecode = compiled["contracts"]["HealthLedger.sol"]["HealthLedger"]["evm"]["bytecode"]["object"]

# 3) Connect to Ganache local node
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
if not w3.is_connected():
    raise RuntimeError("Could not connect to Ganache at http://127.0.0.1:7545. Start Ganache first.")

acct = w3.eth.accounts[0]
w3.eth.default_account = acct
print("Using account:", acct)

# 4) Deploy contract
Health = w3.eth.contract(abi=abi, bytecode=bytecode)
tx_hash = Health.constructor().transact({"from": acct})
print("Deploy tx sent. Waiting for receipt...")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
contract_address = tx_receipt.contractAddress
print("Deployed HealthLedger at:", contract_address)

# 5) Save ABI + address to contract.json for use by backend
OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
with open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump({"address": contract_address, "abi": abi}, f, indent=2)

print("Saved contract info to:", OUT_JSON)
print("Done.")
