import time

from pubnub.pubnub import PubNub 
from pubnub.pnconfiguration import PNConfiguration 
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNOperationType, PNStatusCategory

from backend.keys import PUBLISH_KEY, SUBSCRIBE_KEY 


pnconfig = PNConfiguration()
pnconfig.publish_key = PUBLISH_KEY
pnconfig.subscribe_key = SUBSCRIBE_KEY

# TEST_CHANNEL = "TEST_CHANNEL"
# BLOCK_CHANNEL = "BLOCK_CHANNEL"

CHANNELS = {
    "TEST": "TEST",
    "BLOCK": "BLOCK"
}


class Listener(SubscribeCallback):
    def message(self, pubnub, message_object):
        print(f'\n-- Channel: {message_object.channel} | Message: {message_object.message}')
        # print(f'\n-- Incoming message_object: {message_object}')



class PubSub():
    """
    Handles the publish/subscribe layer of the application
    Provides comm between the nodes of the blockchain network. 
    """
    def __init__(self):
        self.pubnub = PubNub(pnconfig) 
        # ...channels([ch1, ch2])
        self.pubnub.subscribe().channels(CHANNELS.values()).execute()
        self.pubnub.add_listener(Listener())

    def publish(self, channel, message):
        """
        Publish the message object to the channel
        """
        self.pubnub.publish().channel(channel).message(message).sync()

    def broadcastBlock(self, block):
        """
        Broadcast block to all blocks
        """
        self.publish(CHANNELS['BLOCK'], block.toJson())


def main():
    pubsub = PubSub()
    time.sleep(1)
    pubsub.publish(CHANNELS['TEST'], {"foo": "bar"})

if __name__ == "__main__":
    main()