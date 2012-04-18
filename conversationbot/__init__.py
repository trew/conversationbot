from ConversationBotHelpers import ConversationBotFactory, ConversationBotClient
from twisted.internet import reactor
from twisted.python import log

import sys

class Conversation(object):

    commands = []

    def __init__(self, owner, user):
        # start conversation and dispatch to commands depending on msg
        self.owner = owner
        self.user = user
        self._prev = None
        self._next = self.first # the first function to be called.

    def first(self, msg):
        pass

    def call(self, msg):
        """
        Pass user on to the next part of this conversation
        """
        if self in self.owner.active_conversations:
            if hasattr(self.next_call, '__call__'): # == if self.next_ is a function:
                self.next_call = None #set it to none, but self.prev_ is still saved.
                response = self._prev(msg)
                if self.next_call is None:
                    self.owner.end_conversation(self)
                return response
            else:
                return "I'm sorry, there is an unexpected error in the code that runs me. :-("
        else:
            return "This is not an open conversation, I wonder how you got here. ^_^"

    def set_next(self, _next):
        self._prev = self._next
        self._next = _next
    def get_next(self):
        return self._next
    next_call = property(fget=get_next, fset=set_next)

    @property
    def alive(self):
        return self.next_ is not None


class ConversationBot(object):
    """
    A generic conversation bot that can engage in conversations

    This is mainly a wrapper for twisted.words.protocols.irc.IRCClient
    and twisted.internet.protocol.ClientFactory.
    They are tied together with ConversationBotFactory and ConversationBotClient.
    """

    def __init__(self, nick, server, channel, port, logger=None):
        self.server = server
        self.port = port

        if logger is not None:
            log.startLogging(logger.file)
        self.factory = ConversationBotFactory(self, ConversationBotClient,
                                              nick,
                                              channel,
                                              logger)

    def run(self):
        reactor.connectTCP(self.server, self.port, self.factory)
        reactor.run()
