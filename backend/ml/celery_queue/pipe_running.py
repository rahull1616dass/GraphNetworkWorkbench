"""Pipes executor"""
import asyncio


async def run_pipe(chain):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, chain.get)