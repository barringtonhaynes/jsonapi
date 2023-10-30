from abc import abstractmethod
import json
from typing import Callable, List
from fastapi import Request, Response
from fastapi.routing import APIRoute
from pydantic import BaseModel, TypeAdapter

from jsonapi.models.errors import Error
from jsonapi.models.relationships import ResourceIdentifierObject
from jsonapi.models.resource import Resource


def traverse(obj, target_type, action):
    if isinstance(obj, target_type):
        action(obj)
    elif isinstance(obj, BaseModel):
        for attr in obj.__dict__.values():
            traverse(attr, target_type, action)
    elif isinstance(obj, dict):
        for key in obj:
            traverse(obj[key], target_type, action)
    elif isinstance(obj, (list, tuple)):
        for item in obj:
            traverse(item, target_type, action)


def get_related_resource_ids(resource: Resource) -> list[ResourceIdentifierObject]:
    related_resources = []
    traverse(resource, ResourceIdentifierObject, lambda x: related_resources.append(x))
    return related_resources


# def get_included_types(include: str) -> list[str]:
#     if include:
#         return include.split(',')


def parse_included_paths(include: str) -> list[list[str]]:
    if include:
        return [path.split(".") for path in include.split(",")]
    return None


def get_resource_ids(resources: list[Resource]) -> list[ResourceIdentifierObject]:
    # TODO: Check whether we need to filter out None values
    return [resource.to_resource_identifier_object() for resource in resources]


def filter_resources(
    resources: list[Resource],
    resource_ids: list[ResourceIdentifierObject],
    include: bool = True,
) -> list[Resource]:
    return [
        resource
        for resource in resources
        if (resource.to_resource_identifier_object() in resource_ids) == include
    ]


def filter_resource_ids(
    resources: list[ResourceIdentifierObject],
    resource_ids: list[ResourceIdentifierObject],
    include: bool = True,
) -> list[Resource]:
    return [
        resource_id
        for resource_id in resources
        if (resource_id in resource_ids) == include
    ]


class IncludeRelatedRouteBase(APIRoute):
    @abstractmethod
    async def get_related_resources(
        self, request: Request, related_resource_ids=List[ResourceIdentifierObject]
    ) -> tuple[list[Resource], list[Error]]:
        raise NotImplementedError

    async def fetch_all_related_resources(
        self,
        request: Request,
        paths: list[list[str]],
        existing_resources=None,
        existing_errors=None,
    ) -> tuple[list[Resource], list[Error]]:
        if not paths:
            return []

        first_relations = [path[0] for path in paths]

        if existing_resources is None:
            existing_resources = []

        existing_resource_ids = get_resource_ids(existing_resources)
        related_resource_ids = get_related_resource_ids(existing_resources)

        if existing_errors is None:
            existing_errors = []

        # Filter out the ones we already have or aren't in the first step of our paths
        related_resource_ids = [
            resource_id
            for resource_id in related_resource_ids
            if resource_id.type in first_relations
            and not resource_id in existing_resource_ids
        ]

        new_resources, new_errors = await self.get_related_resources(
            request, related_resource_ids
        )

        existing_resources.extend(new_resources)
        existing_errors.extend(new_errors)

        # Drop the first relation from each path and filter out any paths that are now empty
        next_paths = [path[1:] for path in paths if len(path) > 1]

        await self.fetch_all_related_resources(
            request, next_paths, existing_resources, existing_errors
        )

        return existing_resources, existing_errors

    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def include_related_handler(request: Request) -> Response:
            response: Response = await original_route_handler(request)

            # included_types = get_included_types(
            #     request.query_params.get('include'))

            # if included_types is None:
            #     return response

            included_paths = parse_included_paths(request.query_params.get("include"))

            if not included_paths:
                return response

            body = json.loads(response.body.decode())
            model = TypeAdapter(self.response_model).validate_python(body)

            if model.data is None:
                return response

            data_resources = (
                model.data if isinstance(model.data, list) else [model.data]
            )
            data_resource_ids = get_resource_ids(data_resources)

            print("\nDATA RESOURCES\n", data_resources, "=====================\n")
            print("\nDATA RESOURCE IDS\n", data_resource_ids, "=====================\n")

            model.included = [] if model.included is None else model.included
            # included_ids = get_resource_ids(model.included)

            fetched_resources, fetched_errors = await self.fetch_all_related_resources(
                request, included_paths, data_resources
            )
            model.included.extend(fetched_resources)

            if fetched_errors:
                model.errors = [] if model.errors is None else model.errors
                model.errors.extend(fetched_errors)

            # related_resource_ids = getRelatedResources(model.data)
            # related_resource_ids.extend(getRelatedResources(model.included))

            # # filter out related_resources that are already included
            # related_resource_ids = filter_resource_ids(
            #     related_resource_ids, included_ids, False
            # )

            # # filter out related_resources that are not in included_types
            # related_resource_ids = filter_resource_ids(
            #     related_resource_ids, data_resource_ids
            # )

            # resources, errors = await self.get_related_resources(
            #     request, related_resource_ids
            # )

            # model.included.extend(resources)

            # model.included.extend(self.get_related_resources(
            #     request, related_resource_ids))

            # filter out data resources from the included resources
            model.included = filter_resources(model.included, data_resource_ids, False)

            # if errors:
            #     model.errors = [] if model.errors is None else model.errors
            #     model.errors.extend(errors)

            return Response(
                content=model.model_dump_json(
                    exclude_none=self.response_model_exclude_none
                ),
                media_type="application/vnd.api+json",
                status_code=response.status_code,
            )

        return include_related_handler
