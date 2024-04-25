from rest_framework import viewsets
from rest_framework.views import APIView
from .models import Career,Application
from .serializers import CareerSerializer,ApplicationSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

class CareerViewSet(viewsets.ModelViewSet):
    queryset = Career.objects.all()
    serializer_class = CareerSerializer

class ApplicationAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self,request):
        data = request.data
        data["user"] = request.user.id
        
        serializer = ApplicationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Application successfully applied'})      
        return Response({'msg':'An Error Occured'},status=status.HTTP_400_BAD_REQUEST)