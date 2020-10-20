import asyncio

from aioqiwi import Wallet

async def qiwi():
    async with Wallet("a77984cb26c3cb2444f6d79c5f628791") as w:
        w.phone_number = '+79852520741'  # phone number is not required by default, but some methods need it
        balance = await w.balance()
        print("ACCOUNTS:")
        for acc in balance.accounts:
            print(acc.alias, acc.balance)

asyncio.run(qiwi())