from rest_framework.decorators import action
from rest_framework.response import Response
from main import service
from .serializer import FanSerializer


class LikedMixin:
    @action(detail=True, methods=['POST'])
    def like(self, request, pk=None):
        obj = self.get_object()
        service.add_like(obj, request.user)
        return Response("You have liked the article.")

    @action(detail=True, methods=['POST'])
    def unlike(self, request, pk=None):
        obj = self.get_object()
        service.remove_like(obj, request.user)
        return Response("You have unliked the article.")

    @action(detail=True, methods=['GET'])
    def fans(self, request, pk=None):
        obj = self.get_object()
        fans = service.get_fans(obj)
        serializer = FanSerializer(fans, many=True)
        return Response(serializer.data)
