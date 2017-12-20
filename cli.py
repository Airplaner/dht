import asyncio
import logging
import network
import timer
import time
import datetime
logging.getLogger().setLevel("DEBUG")

_TIMEOUT = datetime.timedelta(seconds=3)

class CLI(network.Network, timer.Timer):
    async def start(self):
        message = {
            "type": "heartbeat_ping",
            "uuid": self.uuid,
        }
        logging.info("cli start send")
        self.send_message(message, (network.NETWORK_BROADCAST_ADDR, network.NETWORK_PORT))
        self.async_trigger(self.command, _TIMEOUT)
        pass

    async def command(self):
        print(self._peer_list)
        command = input("connect index:")
        if command == "insert":
            key = input("key:")
            value = input("value:")
            message = {
                "type": "insert",
                "uuid": self.uuid,
                "key": key,
                "value": value,
                }
        pass

    def message_arrived(self, message, addr):
        if message["type"] == "heartbeat_pong":
            self._peer_list.append((message["uuid"],addr))
            

            
                
    def __init__(self, loop):
        network.Network.__init__(self, loop)
        self._peer_list = list()
        import uuid
        self.uuid = str(uuid.uuid1())
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
