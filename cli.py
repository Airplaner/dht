import asyncio
import logging
import network
logging.getLogger().setLevel("DEBUG")

class CLI(network.Network):
    async def start(self):
        message = {
            "type": "search"
        }
        self.send_message(message, (network.NETWORK_BROADCAST_ADDR, network.NETWORK_PORT))
        pass

    def message_arrived(self, message, addr):
        if message["type"] == "test":
            self._peer_list.append(addr)
            print(message)
            
    def __init__(self, loop): 
        network.Network.__init__(self, loop)
        self._peer_list = list()
        asyncio.ensure_future(self.start(), loop=self._loop)
        

def main():
    loop = asyncio.new_event_loop()
    CLI(loop)
    try:
        loop.run_forever()
    finally:
        loop.close()
    pass

if __name__ == "__main__":
    main()
