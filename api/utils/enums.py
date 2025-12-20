from enum import Enum


class FingerprintType(str, Enum):

    COOKIES = 'cookie'
    JS_OBJECTS = 'js_object'
    META = 'meta'
    ASSET_DOMAIN = 'asset_domain'
    ENDPOINT = 'endpoint'
    PATH = 'path'
    BODY_CLASS = 'body_class'
    QUERY_PARAM = 'query_param'
    CHECKOUT_URL = 'checkout_url'
    HTML_ATTRIBUTE = 'html_attribute'
    SCRIPT = 'script'
    IFRAME = 'iframe'
    HTML_COMMENT = 'html_comment'
