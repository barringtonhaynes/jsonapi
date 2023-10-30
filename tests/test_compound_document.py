import json

from jsonapi.models import DTOBaseModel, JsonApiResponse, TopLevelLinks
from jsonapi.models.links import Links
from jsonapi.models.relationships import Relationship, Relationships, ResourceIdentifierObject
from jsonapi.models.resource import Resource

class ArticleAttributes(DTOBaseModel):
    title: str

class Article(Resource[str, ArticleAttributes]):
    type: str = 'articles'

def test_compound_documents():
    """
    https://jsonapi.org/format/#document-compound-documents
    """
    jsonapi_response = JsonApiResponse(
        links=TopLevelLinks(
            self="http://example.com/articles",
            next="http://example.com/articles?page[offset]=2",
            last="http://example.com/articles?page[offset]=10"
        ),
        data=[Article(
            id="1",
            attributes=ArticleAttributes(
                title="JSON:API paints my bikeshed!"
            ),
            relationships=Relationships(
                author=Relationship(
                    links=Links(
                        self="http://example.com/articles/1/relationships/author",
                        related="http://example.com/articles/1/author"
                    ),
                    data=ResourceIdentifierObject(
                        type="people",
                        id="9"
                    )
                ),
                comments=Relationship(
                    links=Links(
                        self="http://example.com/articles/1/relationships/comments",
                        related="http://example.com/articles/1/comments"
                    ),
                    data=[
                        ResourceIdentifierObject(
                            type="comments",
                            id="5"
                        ),
                        ResourceIdentifierObject(
                            type="comments",
                            id="12"
                        )
                    ]
                )
            ),
            links=Links(
                self="http://example.com/articles/1"
            )
        )],
        included=[
            Resource(
                type="people",
                id="9",
                attributes={
                    "firstName": "Dan",
                    "lastName": "Gebhardt",
                    "twitter": "dgeb"
                },
                links=Links(
                    self="http://example.com/people/9"
                )
            ),
            Resource(
                type="comments",
                id="5",
                attributes={
                    "body": "First!"
                },
                relationships=Relationships(
                    author=Relationship(
                        data=ResourceIdentifierObject(
                            type="people",
                            id="2"
                        )
                    )
                ),
                links=Links(
                    self="http://example.com/comments/5"
                )
            ),
            Resource(
                type="comments",
                id="12",
                attributes={
                    "body": "I like XML better"
                },
                relationships=Relationships(
                    author=Relationship(
                        data=ResourceIdentifierObject(
                            type="people",
                            id="9"
                        )
                    )
                ),
                links=Links(
                    self="http://example.com/comments/12"
                )
            )
        ]
    )

    example = {
        "links": {
            "self": "http://example.com/articles",
            "next": "http://example.com/articles?page[offset]=2",
            "last": "http://example.com/articles?page[offset]=10"
        },
        "data": [
            {
                "type": "articles",
                "id": "1",
                "attributes": {
                    "title": "JSON:API paints my bikeshed!"
                },
                "relationships": {
                    "author": {
                        "links": {
                            "self": "http://example.com/articles/1/relationships/author",
                            "related": "http://example.com/articles/1/author"
                        },
                        "data": { "type": "people", "id": "9" }
                    },
                    "comments": {
                        "links": {
                            "self": "http://example.com/articles/1/relationships/comments",
                            "related": "http://example.com/articles/1/comments"
                        },
                        "data": [
                            { "type": "comments", "id": "5" },
                            { "type": "comments", "id": "12" }
                        ]
                    }
                },
                "links": {
                    "self": "http://example.com/articles/1"
                }
            }
        ],
        "included": [
            {
                "type": "people",
                "id": "9",
                "attributes": {
                    "firstName": "Dan",
                    "lastName": "Gebhardt",
                    "twitter": "dgeb"
                },
                "links": {
                    "self": "http://example.com/people/9"
                }
            }, {
                "type": "comments",
                "id": "5",
                "attributes": {
                    "body": "First!"
                },
                "relationships": {
                    "author": {
                    "data": { "type": "people", "id": "2" }
                    }
                },
                "links": {
                    "self": "http://example.com/comments/5"
                }
            }, {
                "type": "comments",
                "id": "12",
                "attributes": {
                    "body": "I like XML better"
                },
                "relationships": {
                    "author": {
                    "data": { "type": "people", "id": "9" }
                    }
                },
                "links": {
                    "self": "http://example.com/comments/12"
                }
            }
        ]
    }

    assert example == json.loads(
        jsonapi_response.model_dump_json(exclude_none=True))
