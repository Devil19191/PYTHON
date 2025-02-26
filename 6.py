from bitcoinlib.keys import Key  # For Bitcoin address generation
import os
import requests  # For making HTTP requests to the blockchain API
from colorama import Fore, Style  # For colored text output
# import time

# Target Bitcoin address
TARGET_ADDRESS = "1MVDYgVaSN6iKKEsbzRUAYFrYJadLYZvvZ"

# Starting and ending range for the private key search
START_RANGE = 0x6bbcdefabcdefabcd  # Starting range in hexadecimal
END_RANGE = 0x99999999999999999    # Ending range in hexadecimal

# Generate a secure private key
def generate_private_key(key_size=256):
    """
    Generate a cryptographically secure private key.
    :param key_size: Size of the key in bits (default: 256 bits).
    :return: A random private key as bytes.
    """
    return os.urandom(key_size // 8)  # Convert bits to bytes

# Decode a private key and generate its Bitcoin address
def decode_private_key(private_key_hex):
    """
    Decode a private key (hexadecimal) and generate its corresponding Bitcoin address.
    :param private_key_hex: The private key as a hexadecimal string.
    :return: The Bitcoin address.
    """
    try:
        # Create a Key object from the private key
        key = Key(private_key_hex)
        # Generate the Bitcoin address from the public key
        address = key.address()
        return address
    except Exception as e:
        print(f"Error decoding private key: {e}")
        return None

# Function to query the real balance of a Bitcoin address using Blockstream API
def get_real_balance(address):
    """
    Query the real balance of a Bitcoin address using the Blockstream API.
    :param address: The Bitcoin address.
    :return: The balance in satoshis.
    """
    try:
        # Blockstream API endpoint for address balance
        url = f"https://blockstream.info/api/address/{address}"
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()
        # The balance is returned in satoshis
        balance_satoshi = data.get("chain_stats", {}).get("funded_txo_sum", 0) - data.get("chain_stats", {}).get("spent_txo_sum", 0)
        return balance_satoshi
    except requests.exceptions.RequestException as e:
        print(f"Error querying balance: {e}")
        return None

# Function to check if a private key corresponds to the target address
def check_private_key(private_key_int):
    """
    Check if a private key (integer) corresponds to the target Bitcoin address.
    :param private_key_int: The private key as an integer.
    :return: True if the address matches the target, False otherwise.
    """
    try:
        # Convert the private key to hexadecimal
        private_key_hex = hex(private_key_int)[2:]  # Remove '0x' prefix
        # Create a Key object from the private key
        key = Key(private_key_hex)
        # Generate the Bitcoin address from the public key
        address = key.address()
        # Check if the address matches the target
        if address == TARGET_ADDRESS:
            print(f"Found matching private key: {private_key_hex}")
            print(f"Corresponding Bitcoin Address: {address}")
            return True
        return False
    except Exception as e:
        print(f"Error processing private key: {e}")
        return False

# Main function to demonstrate decoding a private key and checking real balance
def main():
    print("=== Bitcoin Wallet Generator ===")
    print("Running the program 100 times...\n")

    # Run the program 100 times
    for i in range(1, 1018889799799797):
        print(f"\n--- Iteration {i} ---")
        print("Generating a new Bitcoin wallet...")

        # Step 1: Generate a private key
        private_key_bytes = generate_private_key()
        private_key_hex = private_key_bytes.hex()
        print(f"Generated Private Key (hex): {private_key_hex}")

        # Step 2: Decode the private key and generate the Bitcoin address
        address = decode_private_key(private_key_hex)
        if address:
            print(f"Corresponding Bitcoin Address: {address}")

            # Step 3: Query the real balance of the address
            print("\nQuerying real balance from the blockchain...")
            balance_satoshi = get_real_balance(address)
            if balance_satoshi is not None:
                balance_btc = balance_satoshi / 1e8  # Convert satoshis to BTC
                print("\n=== Wallet Details ===")
                print(f"Private Key (hex): {private_key_hex}")
                print(f"Bitcoin Address: {address}")

                # Highlight balance in red if it is 0 satoshis, otherwise in green
                if balance_satoshi == 0:
                    print(f"Real Balance: {Fore.RED}{balance_btc:.8f} BTC ({balance_satoshi} satoshis){Style.RESET_ALL}")
                else:
                    print(f"Real Balance: {Fore.GREEN}{balance_btc:.8f} BTC ({balance_satoshi} satoshis){Style.RESET_ALL}")
                    print(f"{Fore.GREEN}Balance greater than 0 satoshis found! Stopping the program...{Style.RESET_ALL}")
                    break  # Stop the program if a non-zero balance is found
            else:
                print("\nFailed to query real balance.")
        else:
            print("\nFailed to generate Bitcoin address.")

        print("\n" + "=" * 40)  # Separator for readability

    # Step 4: Search for the target address within the specified range
    print("\n=== Searching for Target Address ===")
    print(f"Searching for private key in range {hex(START_RANGE)} to {hex(END_RANGE)}...\n")
    start_time = time.time()

    # Iterate through the range
    for private_key_int in range(START_RANGE, END_RANGE + 1):
        if check_private_key(private_key_int):
            print("Private key found!")
            break
        # Print progress every 100,000 keys
        if private_key_int % 100000 == 0:
            print(f"Checked up to {hex(private_key_int)}...")

    # end_time = time.time()
    # print(f"Search completed in {end_time - start_time:.0.1f} seconds.")

if __name__ == "__main__":
    main()