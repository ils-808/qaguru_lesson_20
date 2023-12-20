import json
import logging

import requests
from allure import step, attach
from allure_commons.types import AttachmentType


def add_to_cart(url, data=None, cookies = None):
    with step('Add item to cart'):
        resp = requests.post(url, data=data, cookies= cookies)

        attach(body=resp.request.url, name="Request url", attachment_type=AttachmentType.TEXT)
        attach(body=json.dumps(resp.request.body, indent=4, ensure_ascii=True), name="Request body",
               attachment_type=AttachmentType.JSON, extension="json")

        cookies_string = '; '.join([f'{name}={value}' for name, value in resp.cookies.items()])
        attach(body=cookies_string, name='cookies', attachment_type=AttachmentType.TEXT)

        attach(body=json.dumps(resp.json(), indent=4, ensure_ascii=True), name="Response",
               attachment_type=AttachmentType.JSON, extension="json")

        logging.info(f'Response code {resp.status_code}')
        logging.info(f'Response text {resp.text}')
    return resp
