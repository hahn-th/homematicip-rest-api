import asyncio
from pprint import pprint

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


class A:
    def go(self):
        print("A")


class B(A):
    def go1(self):
        self.go()


class C:
    def go(self):
        print('C')


class K(C,B):
    def go2(self):
        self.go1()


if __name__ == "__main__":
    # tst = Test()
    # tst.go()
    #
    # loop = asyncio.get_event_loop()
    #
    # tst = AsyncTest1()
    # loop.run_until_complete(tst.go())
    #
    # tst = AsyncTest2()
    # loop.run_until_complete(tst.go())

    k = K()
    k.go2()
    pprint(K.__mro__)
