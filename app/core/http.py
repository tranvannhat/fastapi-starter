import aiohttp
import requests
import json


class JSONHTTPClient(object):
    @staticmethod
    async def get(url, params=None, headers=None, timeout=10):
        if headers is None:
            headers = {}
        if headers.get("Content-Type") is None:
            headers["Content-Type"] = "application/json"

        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url, params=params, timeout=timeout, verify_ssl=False) as response:
                if (response.status == 200) or (response.status == 201):
                    resp = await response.json()
                    return resp
                else:
                    try:
                        resp = await response.json()
                        return resp
                    except Exception as e:
                        print("JSONHTTPClient Get Exception: ", e)
                        return {
                            "data": 0,
                            "code": "HTTP_ERROR",
                            "message": await response.text(),
                            "status": response.status
                        }

    @staticmethod
    async def post(url, data, headers=None, timeout=10):
        if headers is None:
            headers = {}
        if headers.get("Content-Type") is None:
            headers["Content-Type"] = "application/json"

        async with aiohttp.ClientSession(headers=headers, json_serialize=json.dumps) as session:
            async with session.post(url, json=data, timeout=timeout, verify_ssl=False) as response:
                if (response.status == 200) or (response.status == 201):
                    resp = await response.json()
                    return resp
                else:
                    return {
                        "data": 0,
                        "code": "HTTP_ERROR",
                        "message": await response.text(),
                        "status": response.status
                    }


class XFORMHTTPClient(object):
    @staticmethod
    async def get(url, params=None, headers=None, timeout=10):
        if headers is None:
            headers = {}
        if headers.get("Content-Type") is None:
            headers["Content-Type"] = "application/x-www-form-urlencoded"

        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url, params=params, timeout=timeout, verify_ssl=False) as response:
                if (response.status == 200) or (response.status == 201):
                    resp = await response.json()
                    return resp
                else:
                    try:
                        resp = await response.json()
                        return resp
                    except Exception as e:
                        print("JSONHTTPClient Get Exception: ", e)
                        return {
                            "data": 0,
                            "code": "HTTP_ERROR",
                            "message": await response.text(),
                            "status": response.status
                        }

    @staticmethod
    async def post(url, data, headers=None, timeout=10):
        if headers is None:
            headers = {}
        if headers.get("Content-Type") is None:
            headers["Content-Type"] = "application/x-www-form-urlencoded"

        async with aiohttp.ClientSession(headers=headers, json_serialize=json.dumps) as session:
            async with session.post(url, data=data, timeout=timeout, verify_ssl=False) as response:
                if (response.status == 200) or (response.status == 201):
                    resp = await response.json()
                    return resp
                else:
                    return {
                        "data": 0,
                        "code": "HTTP_ERROR",
                        "message": await response.text(),
                        "status": response.status
                    }


class SyncJSONHTTPClient(object):
    @staticmethod
    def get(url, params=None, headers=None, timeout=10):
        if headers is None:
            headers = {}
        if headers.get("Content-Type") is None:
            headers["Content-Type"] = "application/json"

        session = requests.Session()
        response = session.get(url, params=params, timeout=timeout, headers=headers)
        return response

    @staticmethod
    def post(url, data, headers=None, timeout=10):
        if headers is None:
            headers = {}
        if headers.get("Content-Type") is None:
            headers["Content-Type"] = "application/json"

        session = requests.Session()
        response = session.post(url, json=data, timeout=timeout, headers=headers)
        return response


class SyncXFORMHTTPClient(object):
    @staticmethod
    def get(url, params=None, headers=None, timeout=10):
        if headers is None:
            headers = {}
        if headers.get("Content-Type") is None:
            headers["Content-Type"] = "application/x-www-form-urlencoded"

        session = requests.Session()
        response = session.get(url, params=params, timeout=timeout, headers=headers, verify_ssl=False)
        return response

    @staticmethod
    def post(url, data, headers=None, timeout=10):
        if headers is None:
            headers = {}
        if headers.get("Content-Type") is None:
            headers["Content-Type"] = "application/x-www-form-urlencoded"

        session = requests.Session()
        response = session.post(url, data=data, timeout=timeout, headers=headers, verify_ssl=False)
        return response