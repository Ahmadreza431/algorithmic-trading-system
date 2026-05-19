import time
import json
import hashlib
import hmac
import requests


class Perp:
    def __init__(self, host, access_key, secret_key, *args, **kwargs):
        self.host = host
        self.__access_key = access_key
        self.__secret_key = secret_key
        self.timeout = kwargs["timeout"] if kwargs.get("timeout", None) else 10

    @staticmethod
    def _create_sign(access_key, secret_key, path: str, bodymod: str = None, params: dict = None):
        header = dict()
        apikey = access_key
        secret = secret_key
        timestamp = str(int(time.time() * 1000))
        if bodymod == 'application/x-www-form-urlencoded':
            if params:
                params = dict(sorted(params.items(), key=lambda e: e[0]))
                message = "&".join([f"{arg}={params[arg]}" for arg in params])
                signkey = f"xt-validate-appkey={apikey}&xt-validate-timestamp={timestamp}#{path}#{message}"
            else:
                signkey = f"xt-validate-appkey={apikey}&xt-validate-timestamp={timestamp}#{path}"
        elif bodymod == 'application/json':
            if params:
                message = json.dumps(params)
                signkey = f"xt-validate-appkey={apikey}&xt-validate-timestamp={timestamp}#{path}#{message}"
            else:
                signkey = f"xt-validate-appkey={apikey}&xt-validate-timestamp={timestamp}#{path}"
        else:
            assert False, f"not support this bodymod:{bodymod}"

        digestmodule = hashlib.sha256
        sign = hmac.new(secret.encode("utf-8"), signkey.encode("utf-8"), digestmod=digestmodule).hexdigest()
        header.update({
            'validate-signversion': "2",
            'xt-validate-appkey': apikey,
            'xt-validate-timestamp': timestamp,
            'xt-validate-signature': sign,
            'xt-validate-algorithms': "HmacSHA256"
        })
        return header

    @staticmethod
    def _fetch(method, url, params=None, body=None, data=None, headers=None, timeout=30, **kwargs):
        """
        Create a HTTP request.
           Args:
               method: HTTP request method. `GET` / `POST` / `PUT` / `DELETE`
               url: Request url.
               params: HTTP query params.
               body: HTTP request body, string or bytes format.
               data: HTTP request body, dict format.
               headers: HTTP request header.
               timeout: HTTP request timeout(seconds), default is 30s
               kwargs:
                   proxy: HTTP proxy.

           Return:
               code: HTTP response code.
               success: HTTP response data. If something wrong, this field is None.
               error: If something wrong, this field will holding a Error information, otherwise it's None.

           Raises:
               HTTP request exceptions or response data parse exceptions. All the exceptions will be captured and return
               Error information.
        """
        try:
            if method == "GET":
                response = requests.get(url, params=params, headers=headers, timeout=timeout, **kwargs)
            elif method == "POST":
                response = requests.post(url, params=params, data=body, json=data, headers=headers,
                                         timeout=timeout, **kwargs)
            elif method == "PUT":
                response = requests.put(url, params=params, data=body, json=data, headers=headers,
                                        timeout=timeout, **kwargs)
            elif method == "DELETE":
                response = requests.delete(url, params=params, data=body, json=data, headers=headers,
                                           timeout=timeout, **kwargs)
            else:
                error = "http method error!"
                return None, None, error
        except Exception as e:
            print("method:", method, "url:", url, "headers:", headers, "params:", params, "body:", body,
                  "data:", data, "Error:", e)
            return None, None, e
        code = response.status_code
        if code not in (200, 201, 202, 203, 204, 205, 206):
            text = response.text
            request_url = response.request.url
            print("method:", method, "url:", request_url, "headers:", headers, "params:", params, "body:", body,
                  "data:", data, "code:", code, "result:", text)
            return code, None, text
        try:
            result = response.json()
        except:
            result = response.text
            print("response data is not json format!")
            print("method:", method, "url:", url, "headers:", headers, "params:", params, "body:", body,
                  "data:", data, "code:", code, "result:", json.dumps(result))
        print("method:", method, "url:", url, "headers:", headers, "params:", params, "body:", body,
              "data:", data, "code:", code)
        return code, result, None

    def get_market_config(self, symbol):
        """
        @param symbol:
        @return: market config info
        """
        params = {"symbol": symbol}
        url = self.host + "/future/market" + '/v1/public/symbol/detail'
        code, success, error = self._fetch(method="GET", url=url, params=params, timeout=self.timeout)
        return code, success, error

    def get_all_pair_info(self):
        """
        :return: all pairs info
        """
        params = {}
        url = self.host + "/future/market" + '/v1/public/symbol/coins'
        code, success, error = self._fetch(method="GET", url=url, params=params, timeout=self.timeout)
        return code, success, error

    def get_funding_rate(self, symbol):
        """
        :return:funding rate
        """
        params = {"symbol": symbol}
        url = self.host + "/future/market" + '/v1/public/q/funding-rate'
        code, success, error = self._fetch(method="GET", url=url, params=params, timeout=self.timeout)
        return code, success, error

    def get_agg_tiker(self, symbol):
        """
        :return:agg ticker
        """
        params = {"symbol": symbol}
        url = self.host + "/future/market" + '/v1/public/q/agg-ticker'
        code, success, error = self._fetch(method="GET", url=url, params=params, timeout=self.timeout)
        return code, success, error

    def get_book_ticker(self, symbol):
        """
        :return:book ticker
        """
        params = {"symbol": symbol}
        url = self.host + "/future/market" + '/v1/public/q/ticker/book'
        code, success, error = self._fetch(method="GET", url=url, params=params, timeout=self.timeout)
        return code, success, error

    def get_last_price(self, symbol, length):
        """
        :return: last trade record
        """
        params = {"symbol": symbol, "num": length}
        url = self.host + "/future/market" + '/v1/public/q/deal'
        code, success, error = self._fetch(method="GET", url=url, params=params, timeout=self.timeout)
        return code, success, error

    def get_depth(self, symbol, depth):
        """
        :return:market depth
        """
        params = {"symbol": symbol, "level": depth}
        url = self.host + "/future/market" + '/v1/public/q/depth'
        code, success, error = self._fetch(method="GET", url=url, params=params, timeout=self.timeout)
        return code, success, error

    def get_mark_price(self, symbol):
        """
        :return:mark price
        """
        params = {"symbol": symbol}
        url = self.host + "/future/market" + '/v1/public/q/symbol-mark-price'
        code, success, error = self._fetch(method="GET", url=url, params=params, timeout=self.timeout)
        return code, success, error

    def get_k_line(self, symbol, interval, start_time=None, end_time=None, limit=None):
        """
        :param symbol:
        :param interval: interval string true 1m;5m;15m;30m;1h;4h;1d;1w
        :param start_time:
        :param end_time:
        :param limit:
        :return:
        """
        params = {
            "symbol": symbol,
            "interval": interval,
        }
        if start_time:
            params.update({"startTime": start_time})
        if end_time:
            params.update({"endTime": end_time})
        if limit:
            params.update({"limit": limit})

        url = self.host + "/future/market" + '/v1/public/q/kline'
        code, success, error = self._fetch(method="GET", url=url, params=params, timeout=self.timeout)
        return code, success, error

    def get_symbol_list(self):
        """
        :return: symbol list
        """
        params = {}
        url = self.host + "/future/market" + '/v3/public/symbol/list'
        code, success, error = self._fetch(method="GET", url=url, params=params, timeout=self.timeout)
        return code, success, error
    
    def get_funding_rate_record(self, symbol:str, direction:str="", id:str="", limit:str=""):
        """
        get funding rate record
        :param symbol: str, symbol, required
        :param direction: str, direction, optional, default: ""
        :param id: str, id, optional, default: ""
        :param limit: str, limit, optional, default: ""
        :return: code, success, error
        """
        params = {
            "symbol": symbol,
            "direction": direction,
            "id": id,
            "limit": limit
        }
        url = self.host + "/future/market" + '/v1/public/q/funding-rate-record'
        code, success, error = self._fetch(method="GET", url=url, params=params, timeout=self.timeout)
        return code, success, error
    
    def get_leverage_bracket_list(self):
        """
        :return: list of leverage brackets
        """
        params = {}
        url = self.host + "/future/market" + '/v1/public/leverage/bracket/list'
        code, success, error = self._fetch(method="GET", url=url, params=params, timeout=self.timeout)
        return code, success, error
    
    def get_leverage_bracket_detail(self, symbol:str):
        """
        :param symbol: symbol
        :return: leverage bracket detail
        """
        params = {
            "symbol": symbol
        }
        url = self.host + "/future/market" + '/v1/public/leverage/bracket/detail'
        code, success, error = self._fetch(method="GET", url=url, params=params, timeout=self.timeout)
        return code, success, error

    def get_tickers(self):
        """
        Get all tickers
        :return: code, success, error
        """
        params = {}
        url = self.host + "/future/market" + '/v1/public/q/tickers'
        code, success, error = self._fetch(method="GET", url=url, params=params, timeout=self.timeout)
        return code, success, error
    
    def get_ticker(self,symbol:str):
        """
        Get all tickers
        :return: code, success, error
        """
        params = {'symbol':symbol}
        url = self.host + "/future/market" + '/v1/public/q/ticker'
        code, success, error = self._fetch(method="GET", url=url, params=params, timeout=self.timeout)
        return code, success, error

    def get_account_capital(self):
        """
        :return: account capital
        """
        bodymod = "application/json"
        path = "/future/user" + '/v1/balance/list'
        url = self.host + path
        params = {}
        header = self._create_sign(self.__access_key, self.__secret_key, path=path, bodymod=bodymod,
                                   params=params)
        code, success, error = self._fetch(method="GET", url=url, headers=header, data=params, timeout=self.timeout)
        return code, success, error

    def get_listen_key(self):
        """
        :return: listen_key
        """
        bodymod = "application/json"
        path = "/future/user" + '/v1/user/listen-key'
        url = self.host + path
        params = {}
        header = self._create_sign(self.__access_key, self.__secret_key, path=path, bodymod=bodymod,
                                   params=params)
        code, success, error = self._fetch(method="GET", url=url, headers=header, data=params, timeout=self.timeout)
        return code, success, error

    def send_order(self, symbol, amount, order_side, order_type, position_side, price=None,
                   client_order_id=None, time_in_force=None, trigger_profit_price=None,
                   trigger_stop_price=None, close_position=None):
        """
        ارسال سفارش به صرافی
        """
        params = {
            "orderSide": order_side,
            "orderType": order_type,
            "origQty": amount,
            "positionSide": position_side,
            "symbol": symbol
        }
        if price:
            params["price"] = price
        if client_order_id:
            params["clientOrderId"] = client_order_id
        if time_in_force:
            params["timeInForce"] = time_in_force
        if trigger_profit_price:
            params["triggerProfitPrice"] = trigger_profit_price
        if trigger_stop_price:
            params["triggerStopPrice"] = trigger_stop_price
        if close_position is not None:
            params["closePosition"] = close_position  # اضافه کردن پارامتر closePosition
    
        bodymod = "application/json"
        path = "/future/trade" + '/v1/order/create'
        url = self.host + path
        header = self._create_sign(self.__access_key, self.__secret_key, path=path, bodymod=bodymod,
                                   params=params)
        code, success, error = self._fetch(method="POST", url=url, headers=header, data=params, timeout=self.timeout)
        return code, success, error
    
    def send_batch_order(self, order_list):
        """
        :return: send batch order
        """
        params = order_list

        bodymod = "application/json"
        path = "/future/trade" + "/v2/order/create-batch"
        url = self.host + path
        header = self._create_sign(self.__access_key, self.__secret_key, path=path, bodymod=bodymod,
                                   params=params)
        header.pop("validate-signversion")
        code, success, error = self._fetch(method="POST", url=url, headers=header, data=params, timeout=self.timeout)
        return code, success, error

    def get_position(self, symbol):
        """
        get_position
        :return:
        """
        bodymod = "application/x-www-form-urlencoded"
        path = "/future/user" + '/v1/position/list'
        url = self.host + path
        params = {
            "symbol": symbol,
        }
        header = self._create_sign(self.__access_key, self.__secret_key, path=path, bodymod=bodymod,
                                   params=params)
        header["Content-Type"] = "application/x-www-form-urlencoded"
        code, success, error = self._fetch(method="GET", url=url, headers=header, params=params, timeout=self.timeout)
        return code, success, error

    def cancel_order(self, order_id):
        """
        cancel_order
        :return:
        """
        bodymod = "application/json"
        path = "/future/trade" + '/v1/order/cancel'
        url = self.host + path
        params = {
            "orderId": order_id
        }
        header = self._create_sign(self.__access_key, self.__secret_key, path=path, bodymod=bodymod,
                                   params=params)
        code, success, error = self._fetch(method="POST", url=url, headers=header, data=params, timeout=self.timeout)
        return code, success, error

    def cancel_batch_order(self, order_id_list: list):
        """
        cancel_batch_order
        :return:
        {'returnCode': 0, 'msgInfo': 'success', 'error': None, 'result': True}
        """
        bodymod = "application/json"
        path = "/future/trade" + '/v1/order/cancel-batch'
        url = self.host + path
        params = {
            "orderIds": str(order_id_list)
        }
        header = self._create_sign(self.__access_key, self.__secret_key, path=path, bodymod=bodymod,
                                   params=params)
        code, success, error = self._fetch(method="POST", url=url, headers=header, data=params, timeout=self.timeout)
        return code, success, error

    def cancel_all_order(self, symbol):
        """
        :return: cancel_all_order
        """
        bodymod = "application/json"
        path = "/future/trade" + '/v1/order/cancel-all'
        url = self.host + path
        params = {
            "symbol": symbol
        }
        header = self._create_sign(self.__access_key, self.__secret_key, path=path, bodymod=bodymod,
                                   params=params)
        code, success, error = self._fetch(method="POST", url=url, headers=header, data=params, timeout=self.timeout)
        return code, success, error

    def get_order_id(self, order_id):
        """
        :return: get_order_id
        {'returnCode': 0, 'msgInfo': 'success', 'error': None, 'result': {'orderId': '137699581654889152', 'clientOrderId': None, 'symbol': 'btc_usdt', 'orderType': 'LIMIT', 'orderSide': 'BUY', 'positionSide': 'LONG', 'timeInForce': 'GTC', 'closePosition': False, 'price': '18500', 'origQty': '10', 'avgPrice': '0', 'executedQty': '0', 'marginFrozen': '18.5', 'triggerProfitPrice': None, 'triggerStopPrice': None, 'sourceId': None, 'forceClose': False, 'closeProfit': None, 'state': 'CANCELED', 'createdTime': 1662532138730}}
        """
        bodymod = "application/x-www-form-urlencoded"
        path = "/future/trade" + '/v1/order/detail'
        url = self.host + path
        params = {
            "orderId": order_id
        }
        header = self._create_sign(self.__access_key, self.__secret_key, path=path, bodymod=bodymod,
                                   params=params)
        code, success, error = self._fetch(method="GET", url=url, headers=header, params=params, timeout=self.timeout)
        return code, success, error

    def set_account_leverage(self, leverage, position_side, symbol):
        """
        :return: set_account_leverage
        """
        bodymod = "application/json"
        path = "/future/user" + '/v1/position/adjust-leverage'
        url = self.host + path
        params = {
            "leverage": leverage,
            "positionSide": position_side,
            "symbol": symbol
        }
        params = dict(sorted(params.items(), key=lambda e: e[0]))
        header = self._create_sign(self.__access_key, self.__secret_key, path=path, bodymod=bodymod,
                                   params=params)
        code, success, error = self._fetch(method="POST", url=url, headers=header, data=params, timeout=self.timeout)
        return code, success, error

    def get_account_order(self, state):
        """
        :return: get_account_order
        """
        bodymod = "application/x-www-form-urlencoded"
        path = "/future/trade" + '/v1/order/list'
        url = self.host + path
        params = {
            "state": state,
        }
        header = self._create_sign(self.__access_key, self.__secret_key, path=path, bodymod=bodymod,
                                   params=params)
        code, success, error = self._fetch(method="GET", url=url, headers=header, params=params, timeout=self.timeout)
        return code, success, error

  
    def create_take_profit_order(self, symbol, orig_qty, trigger_profit_price, expire_time, position_side):
        """
        ایجاد سفارش حد سود
        :param symbol: جفت معاملاتی (مثلاً 'btc_usdt')
        :param orig_qty: مقدار (تعداد قراردادها)
        :param trigger_profit_price: قیمت تریگر حد سود
        :param expire_time: زمان انقضا (بر حسب timestamp میلی‌ثانیه)
        :param position_side: جهت پوزیشن ('LONG' یا 'SHORT')
        """
        bodymod = "application/json"
        path = "/future/trade" + '/v1/entrust/create-profit'
        url = self.host + path
        params = {
            "symbol": symbol,
            "origQty": orig_qty,
            "triggerProfitPrice": trigger_profit_price,
            "expireTime": expire_time,
            "positionSide": position_side
        }
        header = self._create_sign(self.__access_key, self.__secret_key, path=path, bodymod=bodymod, params=params)
        code, success, error = self._fetch(method="POST", url=url, headers=header, data=params, timeout=self.timeout)
        return code, success, error

api_key = "Your Api Key"
secret_key = "Your Secret Key"
host = "https://fapi.xt.com"
perp_api = Perp(host, api_key, secret_key)


def handler(pd: "pipedream"):
    # دریافت مقدار target2 و ذخیره آن در symb
    value = float(pd.steps["trigger"]["event"]["body"]["valu"])
    entr = pd.steps["trigger"]["event"]["body"]["entry"]
    sid = pd.steps["trigger"]["event"]["body"]["entry2"]
    target1 = pd.steps["trigger"]["event"]["body"]["target1"]
    target3  = pd.steps["trigger"]["event"]["body"]["target3"]
    valexi1 = float(pd.steps["trigger"]["event"]["body"]["valexi1"])
    valexi2 = float(pd.steps["trigger"]["event"]["body"]["valexi2"]) 
    stop = pd.steps["trigger"]["event"]["body"]["stop"]  
    sym = pd.steps["trigger"]["event"]["body"]["target2"]
    symbol = sym.replace('-', '_')
#////////////////////////////////////////////////////////////////////////
    code, success, error = perp_api.cancel_all_order(symbol)
    
    if code == 200 and success:
        print("All orders cancelled successfully")
    else:
        print("Error cancelling orders:", error) 

#///////////////////////////////////////////////////////////////
    # مشخصات بستن پوزیشن
    code, success, error = perp_api.get_position(symbol)
    if code == 200 and success:
        # بررسی اینکه آیا پوزیشن باز وجود دارد
        if success['returnCode'] == 0 and success['result']:
            # پیمایش در پوزیشن‌ها و نمایش سایز پوزیشن
            positions = success['result']
            for position in positions:
                position_size = position.get('positionSize')
                position_side = position.get('positionSide')
                inside = position_side
                if position_side == "LONG":
                    inside = "SELL"
                else:
                    inside = "BUY"
                  # بستن پوزیشن
                code, success, error = perp_api.send_order(
                    symbol=symbol,
                    amount=position_size,
                    order_side=inside,        # برای بستن پوزیشن لانگ، باید سفارش فروش ارسال کنید
                    order_type="MARKET",
                    position_side=position_side,
                    close_position=True       # بستن کل پوزیشن
                )
        else:
            print("پوزیشن بازی یافت نشد.")
    else:
        print("خطا در دریافت اطلاعات پوزیشن:", error)
#/////////////////////////////////////////////////////////////
    leverage = 12
    pside = entr
    # تنظیم لوریج برای جفت معاملاتی مشخص
    code, success, error = perp_api.set_account_leverage(leverage, pside, symbol)
    
    if code == 200 and success:
        print(f"لوریج برای {symbol} با موفقیت به {leverage} تنظیم شد.")
    else:
        print(f"خطا در تنظیم لوریج برای {symbol}: {error}")  
#/////////////////////////////////////////////////////////////
    def get_contract_size(symbol):
        """
        دریافت مقدار contractSize برای یک جفت معاملاتی مشخص از صرافی XT
    
        :param symbol: جفت معاملاتی به صورت رشته، مثلاً 'BNB_USDT'
        :return: مقدار contractSize یا None اگر جفت معاملاتی پیدا نشد
        """
        url = "https://fapi.xt.com/future/market/v1/public/cg/contracts"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                # پیمایش در لیست قراردادها
                for contract in data:
                    # تبدیل symbol به حروف کوچک برای مقایسه
                    contract_symbol = contract.get('symbol', '').lower()
                    # تبدیل جفت معاملاتی ورودی به حروف کوچک و جایگزینی '-' با '_'
                    input_symbol = symbol.replace('-', '_').lower()
                    if contract_symbol == input_symbol:
                        contract_size = contract.get('contractSize')
                        #print(f"Contract size for {symbol} is {contract_size}")
                        return contract_size
                print(f"Symbol {symbol} not found.")
            else:
                print(f"Error: {response.status_code}")
        except Exception as e:
            print(f"An error occurred: {e}")
        return None
  
    zarib = (1/get_contract_size(symbol))
#//////////////////////////////////////////////////////////////
    amount = round(float(zarib) * value)   # مقدار بیت‌کوین که می‌خواهید بخرید
    order_side = sid
    order_type = "MARKET"
    position_side = entr
    
    code, success, error = perp_api.send_order(
        symbol=symbol,
        amount=str(amount),
        order_side=order_side,
        order_type=order_type,
        position_side=position_side
    )
    
    if code == 200 and success:
        print("Order placed successfully:", success)
    else:
        print("Error placing order:", error)
#//////////////////////////////////////////////////////////////////        
    # مشخصات سفارش حد سود
    orig_qty = round(float(zarib) * valexi1 )          # مقدار قرارداد (تعداد)
    trigger_profit_price = target1  # قیمت تریگر حد سود
    expire_time = int(time.time() * 1000) + 72 * 60 * 60 * 1000  # زمان انقضا (مثلاً 24 ساعت بعد)
    position_side = entr        # جهت پوزیشن
    
    # ایجاد سفارش حد سود
    code, success, error = perp_api.create_take_profit_order(
        symbol=symbol,
        orig_qty=str(orig_qty),
        trigger_profit_price=trigger_profit_price,
        expire_time=expire_time,
        position_side=position_side
    )
    
    if code == 200 and success:
        print("Take Profit Order1 placed successfully:", success)
    else:
        print("Error placing Take Profit Order1:", error)
    
    # مشخصات سفارش حد سود
    orig_qty = round(float(zarib) * valexi2)        # مقدار قرارداد (تعداد)
    trigger_profit_price = target3  # قیمت تریگر حد سود
    expire_time = int(time.time() * 1000) + 72 * 60 * 60 * 1000  # زمان انقضا (مثلاً 24 ساعت بعد)
    position_side = entr        # جهت پوزیشن
    
    # ایجاد سفارش حد سود
    code, success, error = perp_api.create_take_profit_order(
        symbol=symbol,
        orig_qty=str(orig_qty),
        trigger_profit_price=trigger_profit_price,
        expire_time=expire_time,
        position_side=position_side
    )
    
    if code == 200 and success:
        print("Take Profit Order2 placed successfully:", success)
    else:
        print("Error placing Take Profit Order2:", error) 
  
  
    return


