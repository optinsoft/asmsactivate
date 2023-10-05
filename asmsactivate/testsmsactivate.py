from .asyncsmsactivate import AsyncSmsActivate, AsyncSmsActivateException, NoSMSException
from typing import Coroutine

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

async def testAsyncSmsActivate(apiKey: str):
    asmsactivate = AsyncSmsActivate(apiKey)

    print('--- asmsactivate test ---')

    await testApi('getBalance()', asmsactivate.getBalance())
    await testApi('getPrices("mm","0")', asmsactivate.getPrices('mm','0'))
    cc = asmsactivate.getCountryCode('RU')
    number = await testApi(f'getNumber("mm","{cc}")', asmsactivate.getNumber('mm',cc))
    if number:
        await testApi(f'getSMS("{number["id"]}")', asmsactivate.getSMS(number['id']))
        await testApi(f'setStatus("8", "{number["id"]}")', asmsactivate.setStatus('8', number['id']))

    print('--- asmsactivate test completed ---')