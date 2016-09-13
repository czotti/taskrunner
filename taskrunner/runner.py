# -*- coding: utf-8 -*-

import subprocess
import uuid
import redis
import os
import itertools as it

"""
Class get from:
http://peter-hoffmann.com/2012/python-simple-queue-redis-queue.html
"""

QUEUE_NAME = 'taskrunner'
QUEUE_CUR = 'taskrunner_cur'
QUEUE_DONE = 'taskrunner_done'

class RedisQueue(object):
    """Simple Queue with Redis Backend"""

    def __init__(self, name, namespace='queue', **redis_kwargs):
        """The default connection parameters are: host='localhost', port=6379, db=0"""
        self.__db = redis.Redis(**redis_kwargs)
        self.namespace = namespace
        self.key = '%s:%s' % (namespace, name)

    def listing(self):
        key = "{}:{}".format(self.namespace, QUEUE_DONE)
        lst_done = ["(done) {}: {}".format(i, self.__db.lindex(key, i))
                   for i in range(self.__db.llen(key))]

        key = "{}:{}".format(self.namespace, QUEUE_CUR)
        lst_cur = ["(running) {}: {}".format(i, self.__db.lindex(key, i))
                   for i in range(self.__db.llen(key))]

        lst_pend = ["(pending) {}: {}".format(i, self.__db.lindex(self.key, i))
                    for i in range(self.qsize())]

        lst = list(it.chain(lst_done,
                            ['\n\n**** TASK RUNNING ****'], lst_cur,
                            ['\n\n**** TASK PENDING ****'], lst_pend))

        return '\n'.join(lst)

    def clean(self):
        while self.qsize() > 0:
            self.__db.lpop(self.key)

        key = "{}:{}".format(self.namespace, QUEUE_DONE)
        while self.__db.llen(key) > 0:
            self.__db.lpop(key)

        key = "{}:{}".format(self.namespace, QUEUE_CUR)
        while self.__db.llen(key) > 0:
            self.__db.lpop(key)

    def qsize(self):
        """Return the approximate size of the queue."""
        return self.__db.llen(self.key)

    def empty(self):
        """Return True if the queue is empty, False otherwise."""
        return self.qsize() == 0

    def put(self, item):
        """Put item into the queue."""
        self.__db.rpush(self.key, item)

    def get(self, block=True, timeout=None):
        """Remove and return an item from the queue.

        If optional args block is true and timeout is None (the default), block
        if necessary until an item is available."""
        if block:
            item = self.__db.blpop(self.key, timeout=timeout)
        else:
            item = self.__db.lpop(self.key)

        if item:
            item = item[1]
        return item

    def get_nowait(self):
        """Equivalent to get(False)."""
        return self.get(False)


class Jobs(object):
    def __init__(self, command, logger, base_dir="TASK_RUNNER"):
        self.command = command
        self.logger = logger
        self.out_dir = os.path.join(base_dir, "{}_{}".format(uuid.uuid4(), command[2]))
        if not os.path.exists(self.out_dir):
            os.makedirs(self.out_dir)
        self.out_file = os.path.join(self.out_dir, 'command.out')
        self.err_file = os.path.join(self.out_dir, 'command.err')

    def running(self):
        current = RedisQueue(QUEUE_CUR)
        finish = RedisQueue(QUEUE_DONE)
        current.put(self.command)
        subprocess.check_call(self.command,
                              stdout=open(self.out_file, 'w'),
                              stderr=open(self.err_file, 'w'))
        current.get()
        finish.put(self.command)
