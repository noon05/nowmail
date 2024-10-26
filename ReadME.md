
# NowMail

**NowMail** is a powerful Python library for creating and managing temporary email accounts using the [1secmail.com](https://www.1secmail.com/) API. NowMail offers asynchronous and synchronous methods for generating temporary mailboxes, checking messages, and fetching detailed message content. Additionally, it includes a periodic checker to automate mailbox monitoring.

---

## Installation

Install NowMail using `pip`:

```bash
pip install nowmail
```

---

## Features

- **Generate temporary email addresses**: Create single or multiple random temporary email addresses.
- **Message checking and retrieval**: Check for new messages and fetch message content.
- **Automated mailbox monitoring**: Start a periodic checker to monitor mailboxes at defined intervals.
- **Error handling**: Includes built-in exception handling for network and API issues.

---

## Getting Started

Here's a quick guide to get started with NowMail.

### Synchronous Example

```python
from nowmail import generate, check, fetch

# Generate a temporary email address
email_addresses = generate(1)
print("Generated emails:", email_addresses)

# Parse login and domain from email
login, domain = email_addresses[0].split('@')

# Check the mailbox for messages
messages = check(login, domain)
if messages:
    message_id = messages[0].id
    # Fetch full message content
    message = fetch(login, domain, message_id)
    print("Message content:", message.body)
else:
    print("No new messages.")
```

### Asynchronous Example

```python
import asyncio
from nowmail.api.async_api import async_generate, async_check, async_fetch

async def main():
    # Generate email addresses asynchronously
    email_addresses = await async_generate(1)
    print("Generated emails:", email_addresses)

    login, domain = email_addresses[0].split('@')
    # Check for messages asynchronously
    messages = await async_check(login, domain)
    if messages:
        message_id = messages[0].id
        # Fetch full message content asynchronously
        message = await async_fetch(login, domain, message_id)
        print("Message content:", message.body)
    else:
        print("No new messages.")

asyncio.run(main())
```

### Periodic Mailbox Checker

Use NowMail's `start_checker` to continuously monitor an email account and automatically retrieve messages as they arrive.

```python
from nowmail import start_checker

# Start a periodic checker
checker = start_checker("example", "tempmail.com", interval=15, duration=60)
message = checker()
if message:
    print("New message:", message.body)
else:
    print("No new messages in the specified duration.")
```

---

## Detailed API

NowMail provides several modules for handling temporary mailboxes and periodic message checking.

### Core Modules

#### `client.py`

The `TempMailClient` class manages interactions with the tempmail API. It supports asynchronous mailbox generation, checking, and message fetching.

#### `periodic_checker.py`

`PeriodicChecker` automates email checking, enabling you to start a separate thread that continuously monitors an inbox for new messages.

#### `exceptions.py`

Custom exceptions to handle specific errors:

- `MailServiceError`: Base exception for NowMail.
- `NetworkError`: Raised for network-related issues.
- `APIError`: Raised when the API returns an error response.

### Configuration

You can configure NowMail using environment variables or the `config.py` module:

- **BASE_URL**: Set the base URL of the API.
- **TIMEOUT**: Define request timeout (default is 10 seconds).

---

## Dependencies

NowMail requires the following dependencies:

```plaintext
aiohappyeyeballs==2.4.3
aiohttp==3.10.10
aiosignal==1.3.1
async-timeout==4.0.3
certifi==2024.8.30
charset-normalizer==3.4.0
email_validator==2.2.0
lxml==5.3.0
nest-asyncio==1.6.0
pydantic==2.9.2
requests==2.32.3
tenacity==9.0.0
yarl==1.16.0
```

---

## Error Handling

NowMail includes robust error handling. If network issues or API errors occur, NowMail raises specific exceptions that provide details on the error type.

- **NetworkError**: Raised if there’s a connectivity issue.
- **APIError**: Raised if the API responds with an error message.

---

## Testing

To run tests, you can use `pytest`. Make sure to install the development dependencies listed in `install.me`.

```bash
pytest --cov=nowmail tests/
