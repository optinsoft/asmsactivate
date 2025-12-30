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

async def testAsyncSmsActivate(apiKey: str, httpProxy: StrOrURL = None, connectionErrorRetries: int = 0,
                               country: str = 'US', service: str = 'mm', max_price: float = 0.08,
                               operator: str = '', phone_exception: str = '', ref: str =''):
    logger = logging.Logger('testsmsactivate')

    logger.setLevel(logging.DEBUG)

    log_format = "%(asctime)s [%(levelname)s] %(message)s"
    log_path = './log/test.log'

    logFormatter = logging.Formatter(log_format)
    fileHandler = logging.FileHandler(log_path, encoding='utf8')
    fileHandler.setFormatter(logFormatter)
    logger.addHandler(fileHandler)

    asmsactivate = AsyncSmsActivate(apiKey, logger=logger, http_or_socks_proxy=httpProxy, connection_error_retries=connectionErrorRetries, ref=ref)

    print('--- asmsactivate test ---')

    await testApi('getBalance()', asmsactivate.getBalance())
    cc = asmsactivate.getCountryCode(country)
    await testApi(f'getPrices("{service}","{cc}")', asmsactivate.getPrices(service,cc))
    await testApi(f'getOperators("{service}","{cc}")', asmsactivate.getOperators(service,cc))
    await testApi(f'getNumbersStatus(""{cc}")', asmsactivate.getNumbersStatus(cc))
    await testApi(f'getTopCountriesByService("{service}")', asmsactivate.getTopCountriesByService(service))
    number = await testApi(f'getNumberV2("{service}","{cc}","{max_price}")', asmsactivate.getNumberV2(service,cc,str(max_price),operator,phone_exception))
    if number:
        await testApi(f'getSMS("{number["id"]}")', asmsactivate.getSMS(number['id']))
        await testApi(f'setStatus("8", "{number["id"]}")', asmsactivate.setStatus('8', number['id']))

    print('--- asmsactivate test completed ---')