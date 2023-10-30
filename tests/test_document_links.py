import json

from pydantic_core import to_json

from jsonapi.models.links import Links, Link
from jsonapi.models.meta import Meta

def test_document_links():
    """
    https://jsonapi.org/format/#document-links
    """
    jsonapi_links = Links(
        self="http://example.com/articles/1/relationships/comments",
        related=Link(
            href="http://example.com/articles/1/comments",
            title="Comments",
            describedby="http://example.com/schemas/article-comments",
            meta=Meta({
                "count": 10
            })
        )
    )

    example = {
        "self": "http://example.com/articles/1/relationships/comments",
        "related": {
            "href": "http://example.com/articles/1/comments",
            "title": "Comments",
            "describedby": "http://example.com/schemas/article-comments",
            "meta": {
                "count": 10
            }
        }
    }

    assert example == json.loads(to_json(jsonapi_links, exclude_none=True))
