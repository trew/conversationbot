# ConversationBot
This is skeleton to an IRC bot that can engage in conversations.

## Example

    class HelloConversation(Conversation):

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
                        port)

    # Create a new bot
    hBot = HelloBot("HelloBot",         #nickname
                    "irc.freenode.net", #server
                    "#trew",            #channel
                    6667)                #port

    # Connect to the server/channel and start 
    # listening to users.
    hBot.run()

