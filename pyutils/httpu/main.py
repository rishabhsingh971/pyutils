import json
import os

import requests

from pyutils.logu.main import logger


def _ensure_user_agent(headers: dict):
    if "User-Agent" in headers or "user-agent" in headers:
        return
    headers["User-Agent"] =  os.environ.get("PYU_USER_AGENT", __package__)
    return

def req(
    url,
    method="get",
    params=None,
    data=None,
    json=None,
    files=None,
    headers={},
    timeout=30,
    get_json=False,
    raise_exception=False,
    raise_for_status=True,
    cookies=None,
    ensure_user_agent=False,
    **kwargs

):
    if ensure_user_agent:
        _ensure_user_agent(headers)
    logger.debug("Request url: {}".format(url))
    res = None
    try:
        res = requests.request(
            method=method,
            url=url,
            params=params,
            data=data,
            json=json,
            files=files,
            headers=headers,
            timeout=timeout,
            cookies=cookies,
            **kwargs,
        )
        if raise_for_status:
            res.raise_for_status()
        if get_json:
            return res.json(), None
        return res, None
    except Exception as e:
        if raise_exception:
            raise e
        logger.debug(
            "Error while performing '{}' on url - {} with args - {}".format(
                method, url, locals()
            )
        )
        return res, e

def req_to_curl(req: requests.Request) -> str:
    return to_curl(
        url=req.url,
        method=req.method,
        headers=req.headers,
        cookies=getattr(req, "cookies", None),
        payload=getattr(req, "body", None),
    )


def to_curl(url:str, method: str, headers: dict, cookies: dict, payload: any) -> str:
    command = "curl -X {method} -H {headers} -d '{data}' '{uri}'"
    data = ""
    if cookies:
        headers["Cookies"] = ";".join([f"{k}:{v}" for k, v in cookies.items()])
    if payload:
        if isinstance(payload, str):
            data = payload
        elif isinstance(payload, bytes):
            data = payload.decode()
        else:
            data = json.dumps(payload)
    header_list = ['"{0}: {1}"'.format(k, v) for k, v in headers.items()]
    header = " -H ".join(header_list)
    return command.format(method=method, headers=header, data=data, uri=url)
