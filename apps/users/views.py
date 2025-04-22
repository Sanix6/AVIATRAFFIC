#restframework
from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token as DRFToken

#apps
from .models import User
from .serializers import RegisterSerializer, ModifyPasswordSerializers, PersonalSerializers, LoginSerializer
from .utils import Util
from assets.helpers import EMAIL_TEMPLATE

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



class PersonalView(viewsets.ViewSet):

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


