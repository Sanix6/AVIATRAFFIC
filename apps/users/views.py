#restframework
from rest_framework import generics, status, viewsets, views
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token as DRFToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import AllowAny
from django.conf import settings
import uuid
from django.utils import timezone
from datetime import timedelta

#apps
from .models import User
from .serializers import RegisterSerializer, ModifyPasswordSerializers, PersonalSerializers, LoginSerializer,SetNewPasswordSerializer
from .utils import Util, generate_resend_link
from assets.templates import EMAIL_TEMPLATE, RESEND_FORM



class RegisterView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            email_body = EMAIL_TEMPLATE.format(first_name=user.first_name, code=user.code)

            email_data = {'email_subject': 'Подтверждение регистрации','email_body': email_body,'to_email': user.email}
            Util.send_email(email_data)

            return Response({"response": True,
                "message": "Пользователь зарегистрирован. Код подтверждения отправлен на вашу электронную почту."
            }, status=status.HTTP_201_CREATED)

        return Response({"response": False,"message": "Ошибка при регистрации пользователя.",
                        "error": serializer.errors,
                    }, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data['phone']
        password = serializer.validated_data['password']

        user = authenticate(request, phone=phone, password=password)

        if user is not None:
            token, created = DRFToken.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.id,
                'phone': user.phone,
            }, status=status.HTTP_200_OK)
        else:
            return Response(
                {"detail": "Неверный номер телефона или пароль."},
                status=status.HTTP_401_UNAUTHORIZED
            )


class ReSendView(views.APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Отправить новый код для сброса пароля.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email пользователя'),
            },
        )
    )

    def post(self, request):
        email = request.data.get('email')

        try:
            user = User.objects.get(email=email)
            token = str(uuid.uuid4())
            user.reset_token = None
            user.reset_token = token  
            user.token_expiration = timezone.now() + timedelta(minutes=15)
            user.save()

            reset_link = generate_resend_link(token)

            email_body = RESEND_FORM.format(first_name=user.first_name, code=user.code)
            email_data = {
                'email_subject': 'Сброс пароля',
                'email_body': email_body,
                'to_email': user.email
            }
            Util.send_email(email_data)
            return Response({"response": True, "message": "Код для сброса пароля отправлен на ваш email."},
                            status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"response": False, "message": "Пользователь с таким email не найден."},
                            status=status.HTTP_404_NOT_FOUND)



class ConfirmCodeView(views.APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Подтверждение кода, отправленного на email при регистрации.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'code'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email пользователя'),
                'code': openapi.Schema(type=openapi.TYPE_STRING, description='Код подтверждения'),
            },
        )
    )

    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('code')

        if not email or not code:
            return Response({"response": False, "message": "Email и код обязательны."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
            if str(user.code).strip() != str(code).strip():
                return Response({"response": False, "message": "Неверный код подтверждения."},
                                status=status.HTTP_400_BAD_REQUEST)

            user.is_active = True
            user.code = ''
            user.save()

            token, _ = DRFToken.objects.get_or_create(user=user)

            return Response({
                "response": True,
                "message": "Код подтверждён. Аккаунт активирован.",
                "token": token.key,
            }, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"response": False, "message": "Пользователь с таким email не найден."},
                        status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"response": False, "message": "Произошла ошибка.", "error": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class PersonalView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        method='post',
        request_body=ModifyPasswordSerializers,
        responses={200: openapi.Response('Success'), 400: 'Bad Request'}
    )

    @action(detail=False, methods=['post'], url_path='modify-password')
    def modify_password(self, request):
        serializer = ModifyPasswordSerializers(data=request.data, instance=request.user)
        if serializer.is_valid():
            request.user.set_password(serializer.validated_data['password'])
            request.user.save()
            return Response({"responce": True, "message": "Пароль успешно обновлён."}, status=status.HTTP_200_OK)
        return Response({"responce": False, "message": "При изменении пароля произошла ошибка"}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        method='post',
        request_body=PersonalSerializers,
        responses={200: openapi.Response('Success'), 400: 'Bad Request'}
    )

    @action(detail=False, methods=['post'], url_path='modify-personal')
    def modify_personal(self, request):
        serializer = PersonalSerializers(instance=request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"responce": True,"detail": "Профиль успешно обновлён."}, status=status.HTTP_200_OK)
        return Response({"responce": False, "message": "При изменении пароля произошла ошибка"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['delete'], url_path='delete-account')
    def delete_account(self, request):
        user = request.user
        user.delete()
        return Response({"detail": "Аккаунт успешно удалён."}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'], url_path='logout')
    def logout(self, request):
        try:
            request.user.auth_token.delete()
            return Response({'message':'Успешно'}, status=status.HTTP_200_OK)
        except AttributeError:
            return Response({'error': 'У пользователя нет активного токена'}, status=status.HTTP_400_BAD_REQUEST)

