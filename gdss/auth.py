import logging
import globus_sdk
from django.conf import settings
from django.contrib.auth.models import User
from globus_portal_framework.gclients import get_user_groups, load_auth_client

log = logging.getLogger(__name__)


def get_group_from_user_groups(group_id: str, user_groups: list):
    for group in user_groups:
        if group["id"] == group_id:
            return group


def get_user_org_id(user: User):
    ac = load_auth_client(user)
    identities = ac.oauth2_userinfo()
    for identity in identities["identity_set"]:
        if identity["identity_provider"] == settings.REQUIRED_IDENTITY_PROVIDER:
            return identity["sub"]
    raise ValueError(
        f"User does not have an identity that corresponds to configured settings.REQUIRED_IDENTITY_SET: {settings.REQUIRED_IDENTITY_PROVIDER}"
    )


def add_user_to_group(user_uuid: str, group_uuid: str):
    app = globus_sdk.ConfidentialAppAuthClient(
        settings.SOCIAL_AUTH_GLOBUS_KEY, settings.SOCIAL_AUTH_GLOBUS_SECRET
    )
    response = app.oauth2_client_credentials_tokens(
        requested_scopes="urn:globus:auth:scope:groups.api.globus.org:all"
    )
    tokens = response.by_resource_server
    authorizer = globus_sdk.AccessTokenAuthorizer(
        tokens["groups.api.globus.org"]["access_token"]
    )
    gc = globus_sdk.GroupsClient(authorizer=authorizer)

    batch = globus_sdk.BatchMembershipActions()
    batch.add_members(user_uuid)
    try:
        gc.batch_membership_action(group_uuid, batch)
        log.info(f"Added user identity {user_uuid} to group {group_uuid}")
    except globus_sdk.GroupsAPIError as gapie:
        if gapie.code == "FORBIDDEN":
            raise ValueError("Need to run 'python manage.py setup_flow_group'")
        raise


def ensure_user_in_group(user: User):
    group = settings.FLOW_GROUP
    user_uuid = get_user_org_id(user)
    log.debug(f"Checking user {user} within authorized group list...")
    user_groups = get_user_groups(user)
    group = get_group_from_user_groups(settings.FLOW_GROUP, user_groups)
    if group:
        for membership in group["my_memberships"]:
            if (
                membership["identity_id"] == user_uuid
                and membership["status"] == "active"
            ):
                log.debug(
                    f"User {user} already has active membership and does not need to be added to the group"
                )
                return

    add_user_to_group(user_uuid, settings.FLOW_GROUP)
