from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Organisation
from .serializers import UserSerializer, LoginSerializer, OrganisationSerializer
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
import logging

logger = logging.getLogger(__name__)


class RegisterView(APIView):
    def get(self, request):
        
        return Response({"message": "Please use POST method to register"}, status=status.HTTP_200_OK)


    def post(self, request):
        logger.info(f"Received data: {request.data}")
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            org_name = f"{user.first_name}'s Organisation"
            org = Organisation.objects.create(name=org_name)
            org.users.add(user)
            refresh = RefreshToken.for_user(user)
            return Response({
                "status": "success",
                "message": "Registration successful",
                "data": {
                    "accessToken": str(refresh.access_token),
                    "user": UserSerializer(user).data
                }
            }, status=status.HTTP_201_CREATED)
        return Response({"errors": serializer.errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(email=serializer.validated_data['email'], password=serializer.validated_data['password'])
            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    "status": "success",
                    "message": "Login successful",
                    "data": {
                        "accessToken": str(refresh.access_token),
                        "user": UserSerializer(user).data
                    }
                })
            return Response({"status": "Bad request", "message": "Authentication failed", "statusCode": 401}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'user_id'

class UsersView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class OrganisationListView(generics.ListAPIView):
    serializer_class = OrganisationSerializer
    permission_classes = [IsAuthenticated]

    
    def get_queryset(self):
         return Organisation.objects.filter(users=self.request.user)

class OrganisationDetailView(generics.RetrieveAPIView):
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'org_id'
    def get_queryset(self):
        return Organisation.objects.filter(users=self.request.user)

class OrganisationCreateView(generics.CreateAPIView):
    serializer_class = OrganisationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        org = serializer.save()
        org.users.add(self.request.user)

# class AddUserToOrganisationView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, org_id):
#         org = Organisation.objects.get(org_id=org_id)
#         user_id = request.data.get('user_id')
#         user = User.objects.get(user_id=user_id)
#         org.users.add(user)
#         return Response({"status": "success", "message": "User added to organisation successfully"})


class AddUserToOrganisationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, org_id):
        try:
            org = get_object_or_404(Organisation, org_id=org_id)
            user_id = request.data.get('userId')
            
            if not user_id:
                return Response({"status": "error", "message": "userId is required"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                user = User.objects.get(user_id=user_id)
            except User.DoesNotExist:
                return Response({"status": "error", "message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            if user in org.users.all():
                return Response({"status": "success", "message": "User is already in the organisation"}, status=status.HTTP_200_OK)

            org.users.add(user)
            return Response({"status": "success", "message": "User added to organisation successfully"}, status=status.HTTP_200_OK)

        except Organisation.DoesNotExist:
            return Response({"status": "error", "message": "Organisation not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)