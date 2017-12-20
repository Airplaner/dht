import asyncio
import logging
import network
logging.getLogger().setLevel("DEBUG")

while True:
    command = input("command:")
    if command == "list":
        message = {
            "type": "get_leader"
            }
        send_message(message, (network.NETWORK_BROADCAST_ADDR, network.NETWORK_PORT))
        
