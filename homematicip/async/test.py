import asyncio
from pprint import pprint


class Test():
    def go(self):
        print("blocking gone")


class AsyncTest1(Test):
    async def go(self):
        print("async gone using generator")


class AsyncTest2(Test):
    async def go(self):
        print("async gone using async method")


class A:
    def go(self):
        print("A")


class B:
    def go(self):
        print("B")


class C(A):
    pass


class K(C, B):
    def go(self):
        super().go()


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
    k.go()
    pprint(K.__mro__)
