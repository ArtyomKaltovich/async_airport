import argparse
import asyncio
import heapq
import logging
import random
import time
from collections import namedtuple
from datetime import datetime, timedelta
from threading import Thread

logger = logging.getLogger(__name__)
Task = namedtuple("Task", ("start_time", "operation", "args"))


class Airport:
    def __init__(self, n_planes, n_runway):
        self.n_planes = n_planes
        self.n_runway = n_runway
        self._tasks = []
        # time when runway is ready to work and its number
        self._available_runways = [(datetime.now(), n) for n in range(n_runway)]
        self._working_modes = dict(none=self.none, thread=self.thread, awaiting=self.awaiting)
        self._async_variants = {self.land: self.async_land}

    def work(self, mode):
        self._schedule_tasks()
        if mode == "awaiting":
            asyncio.run(self.async_work())
        else:
            while self._tasks:
                self._working_modes[mode](*heapq.heappop(self._tasks))

    async def async_work(self):
        tasks = []
        while self._tasks:
            tasks.append(asyncio.create_task(self.awaiting(*heapq.heappop(self._tasks))))
        for t in tasks:
            await t

    def none(self, start_time, operation, args):
        now = datetime.now()
        if now < start_time:
            logger.info(f"Wait for {start_time}", extra=dict(topic="wait"))
            time.sleep((start_time - now).seconds)
        logger.info(f"Start {operation.__name__}{args}", extra=dict(topic="start"))
        operation(*args)

    def thread(self, start_time, operation, args):
        now = datetime.now()
        if now < start_time:
            logger.info(f"Wait for {start_time}", extra=dict(topic="wait"))
            time.sleep((start_time - now).seconds + 1)
        logger.info(f"Start {operation.__name__}{args}", extra=dict(topic="start"))
        t = Thread(target=operation, args=args)
        t.start()

    async def awaiting(self, start_time, operation, args):
        now = datetime.now()
        if now < start_time:
            #logger.info(f"Wait for {start_time}", extra=dict(topic="wait"))
            await asyncio.sleep((start_time - now).seconds + 1)
        logger.info(f"Start {operation.__name__}{args}", extra=dict(topic="start"))
        return await self.async_land(*args)

    def _schedule_tasks(self, min_land_time=1, max_land_time=5):
        for plain in range(self.n_planes):
            time_when_free, runway = heapq.heappop(self._available_runways)
            time_to_land = random.randrange(min_land_time, max_land_time)
            time_when_free = max(time_when_free, datetime.now())
            logger.info(f"Runway {runway} will be assigned to {plain} in {time_when_free} "
                        f"for {time_to_land} seconds", extra=dict(topic="assigned"))
            heapq.heappush(self._available_runways, (time_when_free + timedelta(seconds=time_to_land), runway))
            heapq.heappush(self._tasks, Task(time_when_free, self.land, (plain, runway, time_to_land)))

    def land(self, plain, runway, time_to_land):
        time.sleep(time_to_land)
        logger.info(f"Plain {plain} landed on {runway}", extra=dict(topic="landed"))

    async def async_land(self, plain, runway, time_to_land):
        await asyncio.sleep(time_to_land)
        logger.info(f"Plain {plain} landed on {runway}", extra=dict(topic="landed"))


def _create_logger():
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(topic)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=f"Program for stupid airport simulation.")
    parser.add_argument("mode", help="Type of parallel work organization", default="none", nargs='?',
                        choices=["none", "thread", "awaiting"])
    parser.add_argument("--n_planes", "-n", help="Number of planes to service", default=1000, type=int)
    parser.add_argument("--n_runways", "-m", help="Number of available runways", default=100, type=int)
    args = parser.parse_args()
    _create_logger()
    airport = Airport(args.n_planes, args.n_runways)
    airport.work(args.mode)
