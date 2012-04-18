# twisted imports
from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from twisted.python import log

# system imports
from datetime import datetime

class ConversationBotFactory(protocol.ClientFactory):
    """A factory for ChallongeBots.

    A new protocol instance will be created each time we connect to the server.
    """

    def __init__(self, bot, client, nickname, channel, logger=None):
        self.client = client
        self.nickname = nickname
        self.channel = channel
        self.conversations = bot.conversations
        self.logger = logger

    def buildProtocol(self, addr):
        p = self.client(self.conversations, self.logger)
        p.factory = self
        return p

    def clientConnectionLost(self, connector, reason):
        """If we get disconnected, reconnect to server."""
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "connection failed:", reason
        reactor.stop()


class ConversationBotClient(irc.IRCClient):

    def __init__(self, conversations, logger=None):
        self.possible_conversations = conversations
        self.active_conversations = []
        self.logger = logger

    def find_conversation(self, user):
        for c in self.active_conversations:
            if user == c.user:
                return c

    def create_conversation(self, user, msg):
        import re
        command_parse = re.compile("^\s*(?P<command>\w+)\s*(?P<rest>.*)$")
        cmds = command_parse.match(msg)
        if cmds is None:
            return "I don't understand what you want to do."

        # split up the message in command + rest
        cmds = cmds.groupdict()
        cmd = cmds['command'].lower()
        rest = cmds['rest']


        # Every conversation has a 'commands'-list. Grab every such list and flatten it
        # to a long list of commands
        # FIXME No check is done if two conversations share the same command.
        command_list = [c.commands for c in self.possible_conversations]
        possible_commands = [command for sublist
                                     in command_list
                                        for command
                                        in sublist]

        if cmd not in possible_commands:
            return "I don't understand this command: %s" % cmd

        for c in self.possible_conversations:
            if cmd in c.commands:
                new_conversation = c(self, user)
                self.active_conversations.append(new_conversation)
                return new_conversation.call(msg)

    def end_conversation(self, conversation):
        self.active_conversations.remove(conversation)


    def log(self, msg):
        if self.logger is not None:
            self.logger.log(msg)


    @property
    def nickname(self):
        return self.factory.nickname

    def connectionMade(self):
        """
        Called when the bot has connected to the server.
        """
        irc.IRCClient.connectionMade(self)
        self.log("[ChallongeBot(%s) connected]" % self.nickname)

    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)
        self.log("[ChallongeBot(%s) disconnected]" % self.nickname)


    # callbacks for events

    def signedOn(self):
        """Called when bot has succesfully signed on to server."""
        self.join(self.factory.channel)

    def joined(self, channel):
        """Called when the bot joins the channel."""
        self.log("[I have joined %s]" % channel)

    def privmsg(self, username, channel, msg):
        """This will get called when the bot receives a message."""

        # shouldn't have conversations in public channel
        if channel != self.nickname:
            return

        user = username.split('!', 1)[0]
        self.log("<%s> %s" % (user, msg))

        conversation = self.find_conversation(user)
        if conversation is None:
            response = self.create_conversation(user, msg)
        else:
            response = conversation.call(msg)
        self.msg(user, response)
        self.log("<%s> to <%s>: %s" % (self.nickname, user, response))

    def action(self, user, channel, msg):
        """This will get called when the bot sees someone do an action."""
        user = user.split('!', 1)[0]
        self.log("* %s %s" % (user, msg))

    def userKicked(self, kickee, channel, kicker, message):
        """Called when the bot observe someone else being kicked from a channel"""
        user = user.split('!', 1)[0]
        self.log("%s has been kicked by %s. Message: %s.") % (kickee, kicker, message)

    def userLeft(self, user, channel):
        """Called when the bot see another user leaving the channel"""
        user = user.split('!', 1)[0]
        self.log("%s has left the channel." % user)

    def userRenamed(self, oldname, newname):
        """A user changed their name from oldname to newname"""
        oldname = oldname.split('!', 1)[0]
        newname = newname.split('!', 1)[0]
        self.log("%s is now known as %s" % (oldname, newname))



def parse_args():
    """
    Parses sys.argv when program starts from __main__.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Arguments for the Challonge IRC Bot")
    parser.add_argument("-n", "--nickname", type=str, help="Nickname to connect with. (Default:\"challongeBot\")", default="challongeBot")
    parser.add_argument("-c", "--channel", type=str, help="Channel to connect to. (wrapped in quotation marks(\") and including '#')", required=True)
    parser.add_argument("-s", "--server", type=str, help="Server to connect to. (Default:\"irc.freenode.net\")", default="irc.freenode.net")
    parser.add_argument("-p", "--port", type=int, help="Port to connect with. (Default:\"6667\")", default=6667)

    args = vars(parser.parse_args())

    nickname = args['nickname']
    channel = args['channel']
    server = args['server']
    port = args['port']

    print "Setting up challonge IRC Bot with settings: \n"\
          "    Nickname: %s\n"\
          "    Channel : %s\n"\
          "    Server  : %s\n"\
          "    Port    : %s\n" % (nickname, channel, server, port)
    return nickname, channel, server, port


if __name__ == '__main__':

    # parse the command line and initialize
    nickname, channel, server, port = parse_args()

    # initialize logging

