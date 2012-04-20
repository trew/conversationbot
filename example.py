from conversationbot import ConversationBot, Conversation
from datetime import datetime

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

# Create a new bot
hBot = HelloBot("HelloBot",         #nickname
                "irc.freenode.net", #server
                "#trew",            #channel
                6667,                #port
                "log/#trew.txt")

# Connect to the server/channel and start 
# listening to users.
hBot.run()
