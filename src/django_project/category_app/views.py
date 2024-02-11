from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.request import Request


class CategoryViewSet(viewsets.ViewSet):
    def list(self, request: Request) -> Response:
        return Response(
            status=200,
            data=[
                {
                    "id": "1",
                    "name": "Movie",
                    "description": "Movie description",
                    "is_active": True,
                },
                {
                    "id": "2",
                    "name": "Serie",
                    "description": "Serie description",
                    "is_active": False,
                },
            ],
        )
