"""
Copyright (c) 2016-2018 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import logging

from programy.storage.stores.logger.store.loggerstore import LoggerStore
from programy.storage.entities.conversation import ConversationStore


class LoggerConversationStore(LoggerStore, ConversationStore):

    def __init__(self, storage_engine):
        LoggerStore.__init__(self, storage_engine)

    def store_conversation(self, clientid, userid, botid, brainid, depth, question, response):
        convo_logger = logging.getLogger(self._storage_engine.configuration.conversation_logger)
        if convo_logger:
            convo_logger.info("[%s] [%s] [%s] [%s] [%s] [%s] [%s]\n"%(clientid, userid, botid, brainid, depth, question, response))
