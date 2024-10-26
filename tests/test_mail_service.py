import pytest
from nowmail.core.mail_service import AsyncMailService

@pytest.mark.asyncio
async def test_generate_random_mailbox():
    mail_service = AsyncMailService()
    mailboxes = await mail_service.generate_random_mailbox(1)
    assert len(mailboxes) == 1
    assert '@' in mailboxes[0]
    await mail_service.close()

@pytest.mark.asyncio
async def test_generate_multiple_mailboxes():
    mail_service = AsyncMailService()
    mailboxes = await mail_service.generate_random_mailbox(5)
    assert len(mailboxes) == 5
    assert all('@' in mailbox for mailbox in mailboxes)
    await mail_service.close()

@pytest.mark.asyncio
async def test_empty_mailbox():
    mail_service = AsyncMailService()
    mailbox = await mail_service.generate_random_mailbox(1)
    login, domain = mailbox[0].split('@')
    messages = await mail_service.check_mailbox(login, domain)
    assert messages == []
    await mail_service.close()

@pytest.mark.asyncio
async def test_fetch_message_by_id():
    mail_service = AsyncMailService()
    mailbox = await mail_service.generate_random_mailbox(1)
    login, domain = mailbox[0].split('@')

   
    messages = await mail_service.check_mailbox(login, domain)
    if messages:
        message_id = messages[0].id
        message = await mail_service.fetch_message(login, domain, message_id)
        assert message is not None
        assert hasattr(message, 'subject') 
    await mail_service.close()

@pytest.mark.asyncio
async def test_invalid_login_or_domain():
    mail_service = AsyncMailService()
    login, domain = "invalid", "domain.com"
    messages = await mail_service.check_mailbox(login, domain)
    assert messages == []
    await mail_service.close()



