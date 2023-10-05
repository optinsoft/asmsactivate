# Async API wrapper for sms-activate.org

## Installation

```bash
pip install git+https://github.com/optinsoft/asmsactivate.git
```

## Usage

```python
from asmsactivate import AsyncSmsActivate
import asyncio

async def test(apiKey: str):
    asmsactivate = AsyncSmsActivate(apiKey)
    print("getBalance\n", await asmsactivate.getBalance())    

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test('PUT_YOUR_API_KEY_HERE'))
```
