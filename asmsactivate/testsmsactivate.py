from .asyncsmsactivate import AsyncSmsActivate, AsyncSmsActivateException, NoSMSException
from typing import Coroutine
import logging
from aiohttp.typedefs import StrOrURL

async def testApi(apiName: str, apiRoutine: Coroutine):
    print(apiName)
    try:
        response = await apiRoutine
        print(response)
        return response
    except NoSMSException:
        print("No SMS")
    except AsyncSmsActivateException as e:
        print("AsyncSmsActivateException:", e)
    return None

async def testAsyncSmsActivate(apiKey: str, httpProxy: StrOrURL = None):
    logger = logging.Logger('testsmsactivate')

    logger.setLevel(logging.DEBUG)

    log_format = "%(asctime)s [%(levelname)s] %(message)s"
    log_path = './log/test.log'

    logFormatter = logging.Formatter(log_format)
    fileHandler = logging.FileHandler(log_path)
    fileHandler.setFormatter(logFormatter)
    logger.addHandler(fileHandler)

    asmsactivate = AsyncSmsActivate(apiKey, logger=logger, http_or_socks_proxy=httpProxy)

    print('--- asmsactivate test ---')

    await testApi('getBalance()', asmsactivate.getBalance())
    cc = asmsactivate.getCountryCode('BR')
    await testApi(f'getPrices("mm","{cc}")', asmsactivate.getPrices('mm',cc))
    number = await testApi(f'getNumber("mm","{cc}")', asmsactivate.getNumber('mm',cc,0.2))
    if number:
        await testApi(f'getSMS("{number["id"]}")', asmsactivate.getSMS(number['id']))
        await testApi(f'setStatus("8", "{number["id"]}")', asmsactivate.setStatus('8', number['id']))

    print('--- asmsactivate test completed ---')