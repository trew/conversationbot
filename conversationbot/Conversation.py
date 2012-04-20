
class Conversation(object):

    commands = []

    def __init__(self, client, user):
        # start conversation and dispatch to commands depending on msg
        self.bot = client.bot
        self.client = client
        self.user = user
        self._prev = None
        self._next = self.first # the first function to be called.

    def first(self, msg):
        pass

    def call(self, msg):
        """
        Pass user on to the next part of this conversation
        """
        if self in self.client.active_conversations:
            if hasattr(self.next_call, '__call__'): # == if self.next_ is a function:
                self.next_call = None #set it to none, but self.prev_ is still saved.
                response = self._prev(msg)
                if self.next_call is None:
                    self.client.end_conversation(self)
                return response
            else:
                self.client.end_conversation(self)
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
