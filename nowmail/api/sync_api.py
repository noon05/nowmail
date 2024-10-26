import asyncio

from typing import List

from nowmail.core.models import Message
from nowmail.api.async_api import async_generate, async_check, async_fetch


def generate(count: int = 1) -> List[str]:
    return asyncio.run(async_generate(count))

def check(login: str, domain: str) -> List[Message]:
    return asyncio.run(async_check(login, domain))

def fetch(login: str, domain: str, message_id: int) -> Message:
    return asyncio.run(async_fetch(login, domain, message_id))