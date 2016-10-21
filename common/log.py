"""
Logging functionality for classes and module level functions.
"""

from inspect import stack
from inspect import getmodule

from logging import DEBUG
from logging import INFO
from logging import WARNING
from logging import ERROR
from logging import CRITICAL

from twisted.python import log
# Have the Twisted logger emit to the Kivy log for the client.
log.addObserver(log.PythonLoggingObserver('kivy').emit)

class Loggable(object):
    """
    Mixin for classes that need logging functionality.
    """
    def log(self, msg, kwargs, level):
        """
        Write a message to the log containg the logging classes name along with
        the message to be logged.

        @param msg: The message to be logged.
        @type msg: C{str}

        @param kwargs: the keyword arguments forwarding to C{format} the log
            message.
        @type kwargs: C{dict}

        @param level: the log level of the message.
        @type level: C{int}
        """
        log.msg(self.__class__.__name__
            + ': '
            + msg.format(**kwargs),
            logLevel=level)

    # shortcuts
    def debug(self, msg, **kwargs):
        self.log(msg, kwargs, DEBUG)

    def info(self, msg, **kwargs):
        self.log(msg, kwargs, INFO)

    def warn(self, msg, **kwargs):
        self.log(msg, kwargs, WARNING)

    def err(self, msg, **kwargs):
        self.log(msg, kwargs, ERROR)

    def crit(self, msg, **kwargs):
        self.log(msg, kwargs, CRITICAL)

class ModuleLogger(Loggable):
    '''
    A class extending Loggable that includes the module from which its log
    method was called from in the log messages it outputs.
    '''
    def log(self, msg, kwargs, level):
        log.msg(getmodule(stack()[2][0]).__name__
            + ': '
            + msg.format(**kwargs),
            logLevel=level)

logger = ModuleLogger()
