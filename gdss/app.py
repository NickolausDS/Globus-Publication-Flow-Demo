from django.apps import AppConfig
from gdss import checks
from gdss import fields


class Gdss(AppConfig):
    name = "gdss"


SEARCH_INDEXES = {
    "gdss": {
        "uuid": "",
        "name": "gdss",
        "fields": [
            ("title", fields.title),
            ("content", fields.content),
            ("publication_status", fields.publication_status),
        ],
        "template_override_dir": "gdss",
    }
}
