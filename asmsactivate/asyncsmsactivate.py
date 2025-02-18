import aiohttp
import ssl
import certifi
import json
from urllib.parse import urlencode
import logging
from functools import reduce

class AsyncSmsActivateException(Exception):
    pass

class NoSMSException(AsyncSmsActivateException):
    pass

class EarlyCancelException(AsyncSmsActivateException):
    pass

class NoNumbersException(AsyncSmsActivateException):
    pass

class WrongMaxPriceException(AsyncSmsActivateException):
    pass

class BannedException(AsyncSmsActivateException):
    pass

class ChannelsLimitException(AsyncSmsActivateException):
    pass

class AsyncSmsActivate:
    def __init__(self, apiKey: str, apiUrl: str = 'https://api.sms-activate.org/stubs/handler_api.php', logger: logging.Logger = None, http_timeout: int = 15,
                 http_proxy: aiohttp.typedefs.StrOrURL = None):
        self.logger = logger
        self.apiKey = apiKey
        self.apiUrl = apiUrl
        self.http_timeout = http_timeout
        self.http_proxy = http_proxy
        self.iso_country_dict = {
            "AE":"95",  "AF":"74",  "AG":"169", "AI":"181", "AL":"155", "AM":"148", "AO":"76",  "AR":"39", 
            "AT":"50",  "AU":"175", "AW":"179", "AZ":"35",  "BA":"108", "BB":"118", "BD":"60",  "BE":"82", 
            "BF":"152", "BG":"83",  "BH":"145", "BI":"119", "BJ":"120", "BM":"158", "BN":"121", "BO":"92", 
            "BR":"73",  "BS":"122", "BW":"123", "BY":"51",  "BZ":"124", "CA":"36",  "CD":"150", "CF":"125", 
            "CG":"18",  "CH":"173", "CI":"27",  "CL":"151", "CM":"41",  "CN":"3",   "CO":"33",  "CR":"93",  "CU": "113",
            "CV":"186", "CY":"77",  "CZ":"63",  "DE":"43",  "DJ":"168", "DK":"172", "DM":"126", "DO":"109", 
            "DZ":"58",  "EC":"105", "EE":"34",  "EG":"21",  "ER":"176", "ES":"56",  "ET":"71",  "FI":"163", 
            "FJ":"189", "FR":"78",  "GA":"154", "GB":"16",  "GD":"127", "GE":"128", "GF":"162", "GH":"38", 
            "GI":"201", "GM":"28",  "GN":"68",  "GP":"160", "GQ":"167", "GR":"129", "GT":"94",  "GW":"130", 
            "GY":"131", "HK":"14",  "HN":"88",  "HR":"45",  "HT":"26",  "HU":"84",  "ID":"6",   "IE":"23", 
            "IL":"13",  "IN":"22",  "IQ":"47",  "IR":"57",  "IS":"132", "IT":"86",  "JM":"103", "JO":"116", "JP":"182", 
            "KE":"8",   "KG":"11",  "KH":"24",  "KM":"133", "KN":"134", "KW":"100", "KY":"170", "KZ":"2", 
            "LA":"25",  "LB":"153", "LC":"164", "LK":"64",  "LR":"135", "LS":"136", "LT":"44",  "LU":"165", 
            "LV":"49",  "LY":"102", "MA":"37",  "MC":"144", "MD":"85",  "ME":"171", "MG":"17",  "MK":"183", 
            "ML":"69",  "MM":"5",   "MN":"72",  "MO":"20",  "MR":"114", "MS":"180", "MU":"157", "MV":"159", 
            "MW":"137", "MX":"54",  "MY":"7",   "MZ":"80",  "NA":"138", "NC":"185", "NE":"139", "NG":"19", 
            "NI":"90",  "NL":"48",  "NO":"174", "NP":"81",  "NZ":"67",  "OM":"107", "PA":"112", "PE":"65", 
            "PG":"79",  "PH":"4",   "PK":"66",  "PL":"15",  "PR":"97",  "PT":"117", "PY":"87",  "QA":"111", 
            "RE":"146", "RO":"32",  "RS":"29",  "RU":"0",   "RW":"140", "SA":"53",  "SC":"184", "SD":"98", 
            "SE":"46",  "SG":"196", "SI":"59",  "SK":"141", "SL":"115", "SN":"61",  "SO":"149", "SR":"142", 
            "SS":"177", "ST":"178", "SV":"101", "SZ":"106", "TD":"42",  "TG":"99",  "TH":"52",  "TJ":"143", 
            "TL":"91",  "TM":"161", "TN":"89",  "TR":"62",  "TT":"104", "TW":"55",  "TZ":"9",   "UA":"1", 
            "UG":"75",  "US":"187", "US":"12",  "UY":"156", "UZ":"40",  "VC":"166", "VE":"70",  "VN":"10", 
            "YE":"30",  "ZA":"31",  "ZM":"147", "ZW":"96"
        }
        self.country_iso_dict = {}
        for item in self.iso_country_dict.items(): 
            self.country_iso_dict[item[1]] = item[0]

    def checkResponse(self, respList: list, successCode: str, noSmsCode: str):
        if len(successCode) > 0:
            if len(respList) > 0:            
                code = respList[0]
                if successCode.endswith('_'):
                    if not code.startswith(successCode):
                        if len(noSmsCode) > 0 and code == noSmsCode:
                            raise NoSMSException("No SMS")
                        if "EARLY_CANCEL_DENIED" == code:
                            raise EarlyCancelException("Yearly cancel denied")
                        if "NO_NUMBERS" == code:
                            raise NoNumbersException("No numbers")
                        if "WRONG_MAX_PRICE" == code:
                            raise WrongMaxPriceException(f'Wrong max. price {":".join(respList[1:])}')
                        if "BANNED" == code:
                            raise BannedException(f'Banned {":".join(respList[1:])}')
                        if "CHANNELS_LIMIT" == code:
                            raise ChannelsLimitException("Channels limit")
                        raise AsyncSmsActivateException(f'Error "{code}": {":".join(respList)}')
                else:
                    if code != successCode:
                        if len(noSmsCode) > 0 and code == noSmsCode:
                            raise NoSMSException("No SMS")
                        if "EARLY_CANCEL_DENIED" == code:
                            raise EarlyCancelException("Yearly cancel denied")
                        if "NO_NUMBERS" == code:
                            raise NoNumbersException("No numbers")
                        if "WRONG_MAX_PRICE" == code:
                            raise WrongMaxPriceException(f'Wrong max. price {":".join(respList[1:])}')
                        if "BANNED" == code:
                            raise BannedException(f'Banned {":".join(respList[1:])}')
                        if "CHANNELS_LIMIT" == code:
                            raise ChannelsLimitException("Channels limit")
                        raise AsyncSmsActivateException(f'Error "{code}": {":".join(respList)}')
            else:
                raise AsyncSmsActivateException(f"Empty response")
        return respList

    def logRequest(self, query, response: dict):
        if not self.logger is None:
            def escapeString(s):
                return s.replace('\\','\\\\').replace('"', '\\"').replace("\r",'\\r').replace("\n","\\n")
            self.logger.debug(
                'query: {'+reduce(lambda x,y: (x+', ' if len(x) > 0 else '')+y+':"'+('*...*' if y== 'api_key' else escapeString(query[y]))+'"', query.keys(),'')+'}'+
                ', response {'+reduce(lambda x,y: (x+', ' if len(x) > 0 else '')+y+':"'+escapeString(str(response[y]))+'"', response.keys(),'')+'}'
            )

    async def doListRequest(self, query: dict, successCode: str = 'ACCESS_', noSmsCode: str = ''):
        url = self.apiUrl + '?' + urlencode(query)
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        conn = aiohttp.TCPConnector(ssl=ssl_context)
        async with aiohttp.ClientSession(connector=conn, raise_for_status=False, timeout=aiohttp.ClientTimeout(total=self.http_timeout)) as session:
            async with session.get(url, timeout=self.http_timeout, proxy=self.http_proxy) as resp:
                if resp.status != 200:
                    respText = await resp.text()
                    self.logRequest(query, {'status':resp.status,'text':respText})
                    raise AsyncSmsActivateException(f"Request failed:\nStatus Code: {resp.status}\nText: {respText}")
                try:
                    respText = await resp.text()
                    self.logRequest(query, {'status':resp.status,'text':respText})
                    respList = respText.split(':')
                except ValueError as e:
                    raise AsyncSmsActivateException(f"Request failed: {str(e)}")
                return self.checkResponse(respList, successCode, noSmsCode)

    async def doJsonRequest(self, query):
        url = self.apiUrl + '?' + urlencode(query)
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        conn = aiohttp.TCPConnector(ssl=ssl_context)
        async with aiohttp.ClientSession(connector=conn, raise_for_status=False, timeout=aiohttp.ClientTimeout(total=self.http_timeout)) as session:
            async with session.get(url, timeout=self.http_timeout, proxy=self.http_proxy) as resp:
                if resp.status != 200:
                    respText = await resp.text()
                    self.logRequest(query, {'status':resp.status,'text':respText})
                    raise AsyncSmsActivateException(f"Request failed:\nStatus Code: {resp.status}\nText: {respText}")
                try:
                    respText = await resp.text()
                    self.logRequest(query, {'status':resp.status,'text':respText})
                    respJson = json.loads(respText)
                except ValueError as e:
                    raise AsyncSmsActivateException(f"Request failed: {str(e)}")
                return respJson

    async def getNumber(self, service: str, country_code: str, max_price: str = ''):
        query = {'action':'getNumber','service':service,'api_key':self.apiKey,'country':country_code}
        if max_price > 0:
            query['maxPrice'] = str(max_price)
        respList = await self.doListRequest(query, 'ACCESS_NUMBER')
        return {"response": 1, "id": respList[1], "number": respList[2]}

    async def setStatus(self, status: str, id: str):
        query = {'action':'setStatus','status':status,'id':id,'api_key':self.apiKey}
        respList = await self.doListRequest(query)
        return {"response": 1, "text": ":".join(respList)}
    
    async def getStatus(self, id: str):
        query = {'action':'getStatus','id':id,'api_key':self.apiKey}
        respList = await self.doListRequest(query)
        return {"response": 1, "status": ":".join(respList)}
    
    async def getSMS(self, id: str):
        query = {'action':'getStatus','id':id,'api_key':self.apiKey}
        respList = await self.doListRequest(query, 'STATUS_OK', 'STATUS_WAIT_CODE')
        return {"response": 1, "sms": respList[1]}

    async def getBalance(self):
        query = {'action':'getBalance','api_key':self.apiKey}
        respList = await self.doListRequest(query)
        return {"response": 1, "amount": respList[1]}
    
    async def getPrices(self, service: str, country_code: str):
        query = {'action':'getPrices','service':service,'api_key':self.apiKey,'country':country_code}
        respJson = await self.doJsonRequest(query)
        return {"response": 1, "prices":respJson}

    def getCountryCode(self, iso_country: str):
        return self.iso_country_dict[iso_country]
    
    def getIsoCountry(self, country_code: str, default: str):
        return self.country_iso_dict.get(country_code, default)
