from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.conf import settings

import globus_sdk
from fair_research_login.client import NativeClient


class Command(BaseCommand):
    help = "Make a user a super user"
    GROUPS_SCOPE = "urn:globus:auth:scope:groups.api.globus.org:all"

    def add_arguments(self, parser):
        parser.add_argument("--approve", action="store_true")

    def handle(self, *args, **options):
        if options["approve"] is not True:
            print(
                f"Will add this portal's identity to flow group settings.FLOW_GROUP {settings.FLOW_GROUP}"
            )
            print(
                "The person calling this script MUST have admin access to the group above."
            )
            print('Call again with "--approve" to make this happen')
            return

        # Login. Replace your client_id below with the one generated from https://developers.globus.org
        cli = NativeClient(
            client_id="7414f0b4-7d05-4bb6-bb00-076fa3f17cf5",
            app_name="Make Portal A Manager",
            token_storage=None,
        )
        tokens = cli.login(requested_scopes=[self.GROUPS_SCOPE])
        authorizer = globus_sdk.AccessTokenAuthorizer(
            tokens["groups.api.globus.org"]["access_token"]
        )

        gc = globus_sdk.GroupsClient(authorizer=authorizer)

        batch = globus_sdk.BatchMembershipActions()
        batch.add_members(settings.SOCIAL_AUTH_GLOBUS_KEY, role="manager")
        gc.batch_membership_action(settings.FLOW_GROUP, batch)

        print(
            f"Added portal identity {settings.SOCIAL_AUTH_GLOBUS_KEY} to group {settings.FLOW_GROUP}"
        )
