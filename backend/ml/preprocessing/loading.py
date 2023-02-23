import tempfile

import aiohttp
import asyncio

from core.types import MLTask
from core.logging_helpers import timeit


async def download_file(file_url: str) -> str:
    """Returns the absolute path of the temporal file where the content is saved"""
    async with aiohttp.ClientSession() as session:
        async with session.get(file_url, headers={"Content-Type": "text/csv"})  as response:
            with tempfile.NamedTemporaryFile(delete=False, mode="wb") as target_file:
                async for every_chunk in response.content.iter_chunked(1024):
                    target_file.write(every_chunk)
    return target_file.name


def download_network_files(task: MLTask) -> dict[str, str]:
    nodes = asyncio.run(download_file(task.nodes_file_url))
    edges = asyncio.run(download_file(task.edges_file_url))
    return {
        'nodes': nodes,
        'edges': edges,
    }
