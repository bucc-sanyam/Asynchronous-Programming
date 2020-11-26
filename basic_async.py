import asyncio


async def count():
    print("One")
    await asyncio.sleep(1)
    print("Two")

async def main():
    await asyncio.gather(count(), count(), count())

if __name__ == "__main__":
    import time
    s = time.time()
    asyncio.run(main())
    elapsed = time.time() - s
    print(f"Execution time: {elapsed:0.2f} second.")