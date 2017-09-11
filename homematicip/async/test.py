import asyncio


class Test():
    def go(self):
        print("blocking gone")


class AsyncTest1(Test):
    @asyncio.coroutine
    def go(self):
        print("async gone using generator")


class AsyncTest2(Test):
    async def go(self):
        print("async gone using async method")


if __name__ == "__main__":
    tst = Test()
    tst.go()

    loop = asyncio.get_event_loop()

    tst = AsyncTest1()
    loop.run_until_complete(tst.go())

    tst = AsyncTest2()
    loop.run_until_complete(tst.go())
