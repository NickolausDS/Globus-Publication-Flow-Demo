import os
from urllib.parse import urlsplit, urlunsplit, urlencode
import logging

log = logging.getLogger(__name__)


def title(result):
    return get_record_type(result, "ContentMetadata")["title"]


def content(result):
    return get_record_type(result, "ContentMetadata")


def publication_status(result):
    return get_record_type(result, "StatusMetadata")


def get_record_type(result, entry_type):
    for entry in result:
        if entry.get("type") == entry_type:
            return entry
