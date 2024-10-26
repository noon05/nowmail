from typing import List

from nowmail.core.models import Message
from nowmail.core.client import TempMailClient

async def async_generate(count: int = 1) -> List[str]:
    async with TempMailClient() as client:
        return await client.generate_random_mailbox(count)

async def async_check(login: str, domain: str) -> List[Message]:
    async with TempMailClient() as client:
        return await client.check_mailbox(login, domain)

async def async_fetch(login: str, domain: str, message_id: int) -> Message:
    async with TempMailClient() as client:
        return await client.fetch_message(login, domain, message_id)