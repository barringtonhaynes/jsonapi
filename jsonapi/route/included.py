from abc import abstractmethod
import json
from typing import Callable, List, Optional
from fastapi import Request, Response
from fastapi.routing import APIRoute
from pydantic import BaseModel, parse_obj_as

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


def getRelatedResources(resource: Resource) -> list[ResourceIdentifierObject]:
    related_resources = []
    related_errors = []
    traverse(
        resource, ResourceIdentifierObject,
        lambda x: related_resources.append(x)
    )
    return related_resources


def hasResolvedResources(resource_identifier: ResourceIdentifierObject, resources: list[Resource]) -> bool:
    for resource in resources: #[0]:
        if resource.type == resource_identifier.type and resource.id == resource_identifier.id:
            return True
    return False


# def get_included_types(include: str) -> list[str]:
#     if include:
#         return include.split(',')
    
def parse_included_paths(include: str) -> list[list[str]]:
    if include:
        return [path.split('.') for path in include.split(',')]
    return []


class IncludeRelatedRouteBase(APIRoute):
    # @abstractmethod
    # def get_related_resources(self, request: Request, related_resource_ids=List[ResourceIdentifierObject]) -> List[Resource]:
    #     raise NotImplementedError
    
    @abstractmethod
    async def get_related_resources(
        self,
        request: Request,
        related_resource_ids=List[ResourceIdentifierObject]
    ) -> tuple[list[Resource], list[Error]]:
        raise NotImplementedError

    async def fetch_all_related_resources(self, request: Request, paths: list[list[str]], existing_resources=None):
        if not paths:
            return []

        if existing_resources is None:
            existing_resources = []

        first_relations = [path[0] for path in paths]
        related_resource_ids = getRelatedResources(existing_resources)

        # Filter out the ones you've already got or aren't in the first step of our paths
        related_resource_ids = [
            res for res in related_resource_ids if res.type in first_relations and not hasResolvedResources(res, existing_resources)
        ]

        new_resources, errors = await self.get_related_resources(request, related_resource_ids)
        existing_resources.extend(new_resources)

        # Drop the first relation from each path and filter out any paths that are now empty
        next_paths = [path[1:] for path in paths if len(path) > 1]

        await self.fetch_all_related_resources(request, next_paths, existing_resources)

        return existing_resources

    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def include_related_handler(request: Request) -> Response:
            response: Response = await original_route_handler(request)

            # included_types = get_included_types(
            #     request.query_params.get('include'))

            # if included_types is None:
            #     return response

            body = json.loads(response.body.decode())
            model = parse_obj_as(self.response_model, body)

            if model.data is None:
                return response

            if model.included is None:
                model.included = []

            included_paths = parse_included_paths(
                request.query_params.get('include')
            )

            if not included_paths:
                return response

            # if model.data is a list return that, otherswise wrap it in a list
            existing_resources = model.data if isinstance(
                model.data, list) else [model.data]

            resources_to_include = await self.fetch_all_related_resources(request, included_paths, existing_resources)
            model.included.extend(resources_to_include)

            related_resource_ids = getRelatedResources(model.data)
            related_resource_ids.extend(getRelatedResources(model.included))

            # filter out related_resources that are already included
            related_resource_ids = [
                resource_id for resource_id in related_resource_ids if not hasResolvedResources(resource_id, model.included)]

            # filter out related_resources that are not in included_types
            related_resource_ids = [
                resource_id for resource_id in related_resource_ids if resource_id.type in included_paths] # included_types]
            
            r, e = await self.get_related_resources(request, related_resource_ids)

            model.included.extend(r)

            # model.included.extend(self.get_related_resources(
            #     request, related_resource_ids))

            return Response(
                content=model.json(
                    exclude_none=self.response_model_exclude_none),
                media_type="application/vnd.api+json",
                status_code=response.status_code
            )

        return include_related_handler
