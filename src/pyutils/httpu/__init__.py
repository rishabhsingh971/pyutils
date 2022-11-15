import requests
import os
from logu import logger


user_agents = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:70.0) Gecko/20100101 Firefox/70.0",
    "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 \
(KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
    "Googlebot/2.1 (+http://www.google.com/bot.html)",
]
USER_AGENT = os.environ.get("PYU_USER_AGENT", user_agents[2])
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
):
    if "User-Agent" not in headers and "user-agent" not in headers and USER_AGENT:
        headers["User-Agent"] = USER_AGENT
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
