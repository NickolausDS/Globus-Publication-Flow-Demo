"""
Make sure you are part of the Globus Flows Users group so that you can deploy this flow,
or delete any prior flows before running this example.
"""
from gladier import GladierBaseClient, GladierBaseTool, generate_flow_definition
from pprint import pprint


class StartPublication(GladierBaseTool):
    """Ingest the initial search record with two entries, one to track the status of publication and the other as the main content. Both
    are private."""

    flow_definition = {
        "StartAt": "StartPublicationIngestStatus",
        "States": {
            "StartPublicationIngestStatus": {
                "Comment": "Ingest a record into Globus Search",
                "Type": "Action",
                "ActionUrl": "https://actions.globus.org/search/ingest",
                "Parameters": {
                    "id": "StatusMetadata",
                    "search_index.$": "$.input.search.index",
                    "subject.$": "$.input.search.subject",
                    "visible_to.=": "[input.search.pre_publish_visible_to]",
                    "content": {
                        "type": "StatusMetadata",
                        "status_type": "transfer",
                        "status": "INCOMPLETE",
                    },
                },
                "ResultPath": "$.StartPublicationIngestStatus",
                "WaitTime": 600,
                "Next": "StartPublicationIngestContent",
            },
            "StartPublicationIngestContent": {
                "Comment": "Ingest a record into Globus Search",
                "Type": "Action",
                "ActionUrl": "https://actions.globus.org/search/ingest",
                "Parameters": {
                    "id": "ContentMetadata",
                    "search_index.$": "$.input.search.index",
                    "subject.$": "$.input.search.subject",
                    "visible_to.=": "[input.search.pre_publish_visible_to]",
                    "content.$": "$.input.search.content",
                },
                "ResultPath": "$.CompletePublicationIngestContent",
                "WaitTime": 600,
                "End": True,
            },
        },
    }


class TransferData(GladierBaseTool):
    """Transfer the data associated with a record."""

    flow_definition = {
        "StartAt": "TransferData",
        "States": {
            "TransferData": {
                "Comment": "Ingest a record into Globus Search",
                "Type": "Action",
                "ActionUrl": "https://actions.globus.org/search/ingest",
                "Parameters": {
                    "id": "Metadata",
                    "search_index.$": "$.input.search.index",
                    "subject": "http://example.com/foo",
                    "visible_to": ["public"],
                    "content": {
                        "type": "Metadata",
                        "testing": {
                            "hello": "world",
                        },
                    },
                },
                "ResultPath": "$.TransferData",
                "WaitTime": 600,
                "End": True,
            },
        },
    }


class CompletePublication(GladierBaseTool):
    """
    Complete publication by marking the transfer as complete and the content entry public
    """

    flow_definition = {
        "StartAt": "CompletePublicationIngestStatus",
        "States": {
            "CompletePublicationIngestStatus": {
                "Comment": "Ingest a record into Globus Search",
                "Type": "Action",
                "ActionUrl": "https://actions.globus.org/search/ingest",
                "Parameters": {
                    "id": "StatusMetadata",
                    "search_index.$": "$.input.search.index",
                    "subject.$": "$.input.search.subject",
                    "visible_to.=": "[input.search.pre_publish_visible_to]",
                    "content": {
                        "type": "StatusMetadata",
                        "status_type": "transfer",
                        "status": "COMPLETE",
                    },
                },
                "ResultPath": "$.CompletePublicationIngestStatus",
                "WaitTime": 600,
                "Next": "CompletePublicationIngestContent",
            },
            "CompletePublicationIngestContent": {
                "Comment": "Ingest a record into Globus Search",
                "Type": "Action",
                "ActionUrl": "https://actions.globus.org/search/ingest",
                "Parameters": {
                    "id": "ContentMetadata",
                    "search_index.$": "$.input.search.index",
                    "subject.$": "$.input.search.subject",
                    "visible_to.=": "[input.search.post_publish_visible_to]",
                    "content.$": "$.input.search.content",
                },
                "ResultPath": "$.CompletePublicationIngestContent",
                "WaitTime": 600,
                "End": True,
            },
        },
    }


@generate_flow_definition
class PublicationTestClient(GladierBaseClient):
    gladier_tools = [
        # First, ingest two search entries under a private group The two entries will:
        #     a. StatusMetadata Entry: Track the status of the transfer
        #     b. ContentMetadata Entry: Contain the content of the search record metadata
        StartPublication,
        # Second, transfer the data tracked by the search records above
        TransferData,
        # Third, Re-ingest the same entries, but this time make the content public
        #     a. StatusMetadata Entry: Now tracks the transfer as COMPLETE
        #     b. ContentMetadata Entry: Will now be shown to as PUBLIC
        CompletePublication,
    ]
    # The Globus Group Configured Here: https://app.globus.org/groups/6fea0a5d-53e2-11ee-b198-0bb9c052ae37/about
    globus_group = "6fea0a5d-53e2-11ee-b198-0bb9c052ae37"

    flow_schema = {
        "type": "object",
        "required": [
            "input",
        ],
        "additionalProperties": False,
        "properties": {
            "input": {
                "type": "object",
                "required": ["search", "source", "destination", "recursive"],
                "propertyOrder": ["search", "source", "destination", "recursive"],
                "additionalProperties": False,
                "properties": {
                    "source": {
                        "type": "object",
                        "title": "Source",
                        "format": "globus-collection",
                        "required": ["id", "path"],
                        "properties": {
                            "id": {
                                "type": "string",
                                "title": "Source Collection ID",
                                "format": "uuid",
                                "pattern": "[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}",
                                "maxLength": 36,
                                "minLength": 36,
                                "description": "The UUID for the collection which serves as the source of the Move",
                            },
                            "path": {
                                "type": "string",
                                "title": "Source Collection Path",
                                "description": "The path on the source collection for the data",
                            },
                        },
                        "description": "Globus-provided flows require that at least one collection is managed under a subscription.",
                        "propertyOrder": ["id", "path"],
                        "additionalProperties": False,
                    },
                    "destination": {
                        "type": "object",
                        "title": "Destination",
                        "format": "globus-collection",
                        "required": ["id", "path"],
                        "properties": {
                            "id": {
                                "type": "string",
                                "title": "Destination Collection ID",
                                "format": "uuid",
                                "pattern": "[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}",
                                "maxLength": 36,
                                "minLength": 36,
                                "description": "The UUID for the collection which serves as the destination for the Move",
                            },
                            "path": {
                                "type": "string",
                                "title": "Destination Collection Path",
                                "description": "The path on the destination collection where the data will be stored",
                            },
                        },
                        "description": "Globus-provided flows require that at least one collection is managed under a subscription.",
                        "propertyOrder": ["id", "path"],
                        "additionalProperties": False,
                    },
                    "search": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "index": {
                                "type": "string"
                            },
                            "subject": {
                                "type": "string"
                            },
                            "pre_publish_visible_to": {
                                "type": "string"
                            },
                            "post_publish_visible_to": {
                                "type": "string"
                            },
                            "content": {
                                "type": "object",
                                "additionalProperties": True,
                                "properties": {
                                    "title": {
                                        "type": "string",
                                        "title": "Search Record Title"
                                    }
                                }
                            }

                        }
                    },
                    "recursive": {
                        "type": "boolean",
                        "title": "Recursive Transfer",
                    }
                },
            }
        },
    }


if __name__ == "__main__":
    flow_input = {
        "input": {
            "search": {
                "index": "3e2525cc-e8c1-49cd-bef5-a9566770d74c",
                "subject": "http://example.com/foo",
                "pre_publish_visible_to": "public",
                "post_publish_visible_to": "public",
                "content": {
                    "type": "ContentMetadata",
                    "title": "Test Metadata Search Record",
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
        }
    }
    # Instantiate the client
    pub_test_client = PublicationTestClient()

    # Optionally, print the flow definition
    pprint(pub_test_client.flow_definition)

    # Run the flow
    flow = pub_test_client.run_flow(flow_input=flow_input, label="Publication Test")

    # Track the progress
    run_id = flow["run_id"]
    pub_test_client.progress(run_id)
    pprint(pub_test_client.get_status(run_id))
