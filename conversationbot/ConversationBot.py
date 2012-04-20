from ConversationBotHelpers import ConversationBotFactory, ConversationBotClient
from twisted.internet import reactor
from twisted.python import log
from twisted.python.logfile import LogFile

class ConversationBot(object):
    """
    A generic conversation bot that can engage in conversations

    This is mainly a wrapper for twisted.words.protocols.irc.IRCClient
    and twisted.internet.protocol.ClientFactory.
    They are tied together with ConversationBotFactory and ConversationBotClient.
    """

    def __init__(self, nick, server, channel, port, loggingfile=None):
        self.server = server
        self.port = port

        if loggingfile is not None:
            log.startLogging(LogFile.fromFullPath(loggingfile))
        self.factory = ConversationBotFactory(self, ConversationBotClient,
                                              nick,
                                              channel)

    def run(self):
        reactor.connectTCP(self.server, self.port, self.factory)
        reactor.run()
