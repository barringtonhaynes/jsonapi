import json

from pydantic_core import to_json

from jsonapi.models import JsonApi


def test_jsonapi_object():
    """
    https://jsonapi.org/format/#document-jsonapi-object
    """
    jsonapi_object = JsonApi(
        ext=[
            "https://jsonapi.org/ext/atomic"
        ],
        profile=[
            "http://example.com/profiles/flexible-pagination",
            "http://example.com/profiles/resource-versioning"
        ]
    )

    example =  {
        "version": "1.1",
        "ext": [
            "https://jsonapi.org/ext/atomic"
        ],
        "profile": [
            "http://example.com/profiles/flexible-pagination",
            "http://example.com/profiles/resource-versioning"
        ]
    }

    assert example == json.loads(to_json(jsonapi_object, exclude_none=True))
