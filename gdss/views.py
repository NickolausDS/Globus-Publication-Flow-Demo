import logging
from django.shortcuts import render, redirect

# from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django import forms

import globus_sdk
from globus_portal_framework.gclients import load_globus_access_token
from globus_portal_framework.gsearch import get_index

from gdss.forms import PublishDataForm

log = logging.getLogger(__name__)


# @login_required
def publish_data_flow(request, index):
    """
    This view is the heart of this project. It behaves a few different ways.
    First, it renders the form above in normal GET requests, and allows the user to
    populate it with values.

    When a user POSTs a valid form, it loads a _user_ access token and starts the flow
    as the user with the values they provide. The JSON response is given directly to
    the template, and used to build a link to the webapp to track progress.
    """
    context = {}
    if request.method == "POST":
        form = PublishDataForm(request.POST)
        if form.is_valid():
            log.debug(f"Loading flow token for user {request.user.username}")
            token = load_globus_access_token(request.user, settings.FLOW_ID)
            authorizer = globus_sdk.AccessTokenAuthorizer(token)
            sfc = globus_sdk.SpecificFlowClient(settings.FLOW_ID, authorizer=authorizer)
            run = sfc.run_flow(
                body={
                    "input": {
                        "search": {
                            "index": get_index(index)["uuid"],
                            "subject": "http://example.com/foo",
                            "pre_publish_visible_to": "public",
                            "post_publish_visible_to": "public",
                            "content": {
                                "type": "ContentMetadata",
                                "title": form.cleaned_data["title"],
                            },
                        },
                        "source": {
                            "id": "ddb59aef-6d04-11e5-ba46-22000b92c6ec",
                            "path": "/share/godata",
                        },
                        "destination": {
                            "id": "ddb59aef-6d04-11e5-ba46-22000b92c6ec",
                            "path": "/~/",
                        },
                        "recursive": True,
                    },
                },
                label=form.cleaned_data["label"],
                tags=form.cleaned_data["tags"].split(","),
            )
            log.info(
                f"Flow started with run {run.data['run_id']} for user {request.user.username}"
            )
            messages.info(request, "Your flow has been started!")
            return redirect("search", index=index)
        log.debug(
            f"User {request.user.username} failed to start flow due to {len(form.errors)} form errors."
        )
    else:
        log.debug(f"Loading new form for user {request.user.username}")
        form = PublishDataForm()
    context["form"] = form
    return render(request, "publish-data-flow.html", context)
