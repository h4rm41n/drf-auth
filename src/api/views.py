from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status, serializers

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

#serializer untuk form login
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255, required=True,)
    password = serializers.CharField(max_length=255, required=True,)

#class untuk generated token
class TokenRequestTask:
    @staticmethod
    def newToken(user):
        if TokenRequestTask.checkToken(user):
            reset_token = TokenRequestTask.resetToken(user)
            create_token = TokenRequestTask.createToken(user)
            new_token = Token.objects.get(user=user)
            return new_token.key
        else:
            create_token = TokenRequestTask.createToken(user)
            new_token = Token.objects.get(user=user)
            return new_token.key

    @staticmethod
    def checkToken(user):
        try:
            Token.objects.get(user=user)
            return True
        except Token.DoesNotExist:
            return False

    @staticmethod
    def resetToken(user):
        try:
            token = Token.objects.filter(user=user)
            token.delete()
            return True
        except:
            return False

    @staticmethod
    def createToken(user):
        try:
            Token.objects.create(user=user)
            return True
        except:
            return False

    @staticmethod
    def tokenExists(key, user):
        check_token = Token.objects.filter(key=key, user=user)
        if check_token.exists():
            return True
        else:
            return False

#view login
class LoginAPIView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            check_user = User.objects.filter(
                                username=serializer.validated_data['username']
                            )

            if check_user.exists():
                get_obj_user = User.objects.get(
                                    username=serializer.validated_data['username']
                                )
                if not get_obj_user.check_password(serializer.validated_data['password']):
                    return Response({
                            "detail":"Maaf kombinasi username dan password kurang tepat",
                            "":None,
                        }, status=status.HTTP_400_BAD_REQUEST)

                return Response({
                        "detail":{
                            "token":TokenRequestTask.newToken(get_obj_user),
                            "message":"Selamat login sukses",
                        }
                    }, status=status.HTTP_202_ACCEPTED)

            return Response({
                        "detail":{
                            "message":"Maaf data login anda tidak valid",
                        }
                    }, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TestRequiredToken(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if TokenRequestTask.tokenExists(request.auth.key, request.user):
            user = User.objects.filter(user=request.user)
            if not user.exists():
                return Response({
                    "detail":"Maaf akses anda ilegal",
                }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "detail":{
                "username":user.username,
                "first_name":user.first_name,
                "last_name":user.last_name,
                "email":user.email,
                "is_staff":user.is_staff,
                "date_joined":user.date_joined
            }
        }, status=status.HTTP_400_BAD_REQUEST)