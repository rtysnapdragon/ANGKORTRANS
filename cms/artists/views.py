from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Artist

@api_view(['POST'])
def artist_list(request):
    try:
        data=request.data
        Artists=Artist.objects.all()
        
        return Response({"success": True}, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=500)