from asyncio import Queue
from asyncio import CancelledError
from asyncio import TimeoutError
from asyncio import wait_for
from asyncio import sleep
from time import time

from db import db


class ResultController(object):
    async def insert(self, obj):
        await db.create(obj)


class VoteController(object):
    def __init__(self, app, workers=5, timeout=2, max_size=1000):
        self.queue = Queue()
        self.workers_size = workers
        self.workers = []
        self.timeout = timeout
        self.max_size = max_size
        app.on_startup.append(self.start)
        app.on_cleanup.append(self.stop)

    def start(self, app):
        for i in range(self.workers_size):
            self.workers.append(app.loop.create_task(self._consumer(i)))

    def stop(self, app):
        for worker in self.workers:
            worker.cancel()

    async def insert(self, obj):
        await self.queue.put(obj)

    async def _consumer(self, num=0):
        reset = lambda: (0, {}, time())
        await sleep(0.3*num) # So workes do not persist at the same time
        size, data, t0 = reset()
        print("Hi! I'm worker {}. And I'm ready to ROCK!".format(num))
        try:
            while True:
                try:
                    obj = await wait_for(self.queue.get(), self.timeout)
                    data = self._process_data(data, obj)
                    size += 1
                except TimeoutError:
                    pass

                if time() - t0 > self.timeout or size >= self.max_size:
                    if data:
                        await db.update(data)
                    size, data, t0 = reset()

        except CancelledError:
            pass

    def _process_data(self, data, obj):
        poll_id = obj['pollResourceId']
        option_id = obj['optionId']

        if poll_id not in data:
            data[poll_id] = {}
        if option_id not in data[poll_id]:
            data[poll_id][option_id] = 1
        else:
            data[poll_id][option_id] += 1

        return data
