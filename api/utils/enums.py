from enum import Enum


class FingerprintType(str, Enum):

    COOKIES = 'cookie'
    JS_OBJECTS = 'js object'
    META = 'meta'
    ASSET_DOMAIN = 'asset_domain'
    ENDPOINT = 'endpoint'
    PATH = 'path'
    BODY_CLASS = 'body class'
    QUERY_PARAM = 'query param'
    CHECKOUT_URL = 'checkout url'
    HTML_ATTRIBUTE = 'html_attribute'
    SCRIPT = 'script'
    IFRAME = 'iframe'
    HTML_COMMENT = 'html comment'
