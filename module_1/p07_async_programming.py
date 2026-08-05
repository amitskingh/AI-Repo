import time
import asyncio


def make_coffe():
    print("Starting to make coffee...")
    time.sleep(3)  # Simulating a delay in making coffee
    print("Coffee is ready!")


def make_tea():
    print("Tea is ready!")


async def make_coffee_async():
    print("Starting to make coffee asynchronously...")
    await asyncio.sleep(3)  # Simulating a delay in making coffee
    print("Coffee is ready asynchronously!")


async def task(name: str, seconds: int):
    print(f"{name} started")

    await asyncio.sleep(seconds)

    print(f"{name} finished")


async def main():
    # This will finish in 2 seconds because the tasks are running concurrently.
    await asyncio.gather(
        task("LLM", 2),
        task("Database", 1),
        task("Vector DB", 1),
    )



if __name__ == "__main__":
    # Synchronous execution
    print("===================================================")
    make_coffe()

    print("===================================================")
    # Asynchronous execution
    asyncio.run(make_coffee_async())

    print("===================================================")
    asyncio.run(main())