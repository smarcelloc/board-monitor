import uasyncio as asyncio


class EventLoop:

    def __init__(self):
        self._tasks = {}
        self._running = False

    @staticmethod
    async def sleep_ms(ms: int):
        await asyncio.sleep(ms / 1000)

    def add_task(self, name: str, coroutine):
        if self._running and name in self._tasks:
            return
        self._tasks[name] = asyncio.create_task(coroutine)

    def cancel_task(self, name: str):
        if not self._running and name not in self._tasks:
            return
        self._tasks[name].cancel()
        self._tasks.pop(name)

    def run(self):
        if not self._running:
            asyncio.run(self._coroutine_run())

    def stop(self):
        for name, _ in self._tasks.items():
            self.cancel_task(name)
        self._running = False

    async def _coroutine_run(self):
        self._running = True
        while self._running:
            await EventLoop.sleep_ms(100)
