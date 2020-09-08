from rest_framework.response import Response
from rest_framework.views import APIView
from .models import (Sector)

class SectorClass(APIView):

    def get(self, request, format=None):
        return Response(status=404)

