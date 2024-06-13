from adrf.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from .models import PointOfInterest
from .serializers import PointOfInterestSerializer
from django.db import models
from asgiref.sync import sync_to_async


class PointOfInterestListCreateView(APIView):
    """
    API view to list and create points of interest.
    """
    permission_classes = [permissions.IsAuthenticated]

    async def get(self, request):
        pois = await sync_to_async(list)(PointOfInterest.objects.filter(user=request.user))
        serializer = PointOfInterestSerializer(pois, many=True)
        return Response(serializer.data)

    async def post(self, request):
        serializer = PointOfInterestSerializer(data=request.data)
        if await sync_to_async(serializer.is_valid)():
            await sync_to_async(serializer.save)(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PointOfInterestDetailView(APIView):
    """
    API view to retrieve, update, and delete points of interest.
    """
    permission_classes = [permissions.IsAuthenticated]

    async def get_object(self, pk):
        try:
            return await sync_to_async(PointOfInterest.objects.get)(pk=pk, user=self.request.user)
        except PointOfInterest.DoesNotExist:
            return None

    async def get(self, request, pk):
        poi = await self.get_object(pk)
        if poi is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PointOfInterestSerializer(poi)
        return Response(serializer.data)

    async def put(self, request, pk):
        poi = await self.get_object(pk)
        if poi is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PointOfInterestSerializer(poi, data=request.data)
        if await sync_to_async(serializer.is_valid)():
            await sync_to_async(serializer.save)()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    async def patch(self, request, pk):
        poi = await self.get_object(pk)
        if poi is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PointOfInterestSerializer(poi, data=request.data, partial=True)
        if await sync_to_async(serializer.is_valid)():
            await sync_to_async(serializer.save)()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    async def delete(self, request, pk):
        poi = await self.get_object(pk)
        if poi is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        await sync_to_async(poi.delete)()
        return Response(status=status.HTTP_204_NO_CONTENT)
