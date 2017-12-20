import asyncio
import dht
import logging
logging.getLogger().setLevel("DEBUG")

def main():
    class cli():
        async def doSomething(self):
            while True:
                command = input("command:")
                if command == "list":
                    print(mydht._context.peer_list)
                    

                if command == "insert":
                    key = input("key:")
                    value = input("value:")
                    message = {
                        "type": "insert",
                        "key": key,
                        "value": value,
                        }
                    break
                
                
        def __init__(self, loop):
            self._loop = loop
            asyncio.ensure_future(self.doSomething(), loop=self._loop)
        
    loop = asyncio.new_event_loop()
    mydht = dht.DHT(loop)
    cli(loop)
    
    try:
        loop.run_forever()
    finally:
        loop.close()
    pass

if __name__ == "__main__":
    main()
