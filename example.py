from conversationbot import ConversationBot, Conversation
from datetime import datetime

class MessageLogger:
    """
    A logger
    """

    def __init__(self, file):
        self.file = file

    def log(self, message):
        """Write a message to the file."""
        timestamp = datetime.now().replace(microsecond=0).isoformat()
        self.file.write('%s %s\n' % (timestamp, message))
        self.file.flush()

    def close(self):
        self.file.close()

class HelloConversation(Conversation):
    """
    A user says 'hello' to the bot. The bot asks for the users name and then
    replies with the name.
    """

    commands = ["hello",'hi']

    def first(self, message):
        self.next_call = self.second
        return "Hello there! What is your name?"

    def second(self, message):
        return "Oh hello %s! Have a nice day!" % message

class HelloBot(ConversationBot):

    conversations = [HelloConversation]

    def __init__(self,nick,server,chan,port,logger=None):
        super(HelloBot, self).__init__(
                    nick,
                    server,
                    chan,
                    port,
                    logger)

# Initiate a logger
logger = MessageLogger(open("log/#trew.txt", "a"))

# Create a new bot
hBot = HelloBot("HelloBot",         #nickname
                "irc.freenode.net", #server
                "#trew",            #channel
                6667,                #port
                logger)

# Connect to the server/channel and start 
# listening to users.
hBot.run()

# close the logger
logger.close()
