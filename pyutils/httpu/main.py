import requests
import os
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
