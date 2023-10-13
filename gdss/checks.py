from django.core.checks import Info, register
from django.conf import settings


@register()
def settings_checks(app_configs, **kwargs):
    errors = []
    if not settings.SOCIAL_AUTH_GLOBUS_KEY or not settings.SOCIAL_AUTH_GLOBUS_SECRET:
        errors.append(
            Info(
                "Globus App credentials have not been configured, login will not work.",
                hint="Please go to the following link and add your credentials in local_settings.py:\n\t"
                "https://app.globus.org/settings/developers/registration/confidential_client/select-project",
                obj=settings,
                id="gdss.W001",
            )
        )

    if not any(p["uuid"] for p in settings.SEARCH_INDEXES.values()):
        errors.append(
            Info(
                "Your project does not have a search UUID!",
                hint="You can create one with:\n\t"
                'globus search index create gdss "A search index for gdss" '
                "And set the UUID inside gdss.apps.SEARCH_INDEXES[].uuid",
                obj=settings,
                id="gdss.W002",
            )
        )
    return errors
