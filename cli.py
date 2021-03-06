import asyncio
import logging
import network
import timer
import time
import datetime
logging.getLogger().setLevel("INFO")

_TIMEOUT = datetime.timedelta(seconds=3)
_LONG = datetime.timedelta(seconds=5)
_SHORT = datetime.timedelta(seconds=1)

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
        if len(self._peer_list) == 0:
            print("Fail to find any node. Restart CLI")
            exit()
        for i in self._peer_list:
            print(i)
        index = int(input("node index:"))
        addr = self._peer_list[index][1]
        
        command = input("command:")
        if command == "insert":
            key = input("key:")
            value = input("value:")
            
            message = {
                "type": "delete",
                "uuid": self.uuid,
                "key": key,
                }
            self.send_message(message, (network.NETWORK_BROADCAST_ADDR, network.NETWORK_PORT))
            
            message = {
                "type": "insert",
                "uuid": self.uuid,
                "key": key,
                "value": value,
                }
            self.send_message(message, addr)
            
            index = (index + 1) % len(self._peer_list)
            addr = self._peer_list[index][1]
            self.send_message(message, addr)
            
            index = (index + 1) % len(self._peer_list)
            addr = self._peer_list[index][1]
            self.send_message(message, addr)
                
            
        elif command == "search":
            key = input("key:")
            message = {
                "type": "search",
                "uuid": self.uuid,
                "key": key,
                }
            self.send_message(message, (network.NETWORK_BROADCAST_ADDR, network.NETWORK_PORT))
            self.async_trigger(self.fail, _TIMEOUT)

        elif command == "delete":
            key = input("key:")
            message = {
                "type": "delete",
                "uuid": self.uuid,
                "key": key,
                }
            self.send_message(message, (network.NETWORK_BROADCAST_ADDR, network.NETWORK_PORT))
        pass

    async def fail(self):
        print("Fail")
        exit()

    def message_arrived(self, message, addr):
        if message["type"] == "heartbeat_pong":
            self._peer_list.append((message["uuid"],addr))
                              
        if message["type"] == "search_response":
            print("value:",message["value"])
            exit()
                              
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
