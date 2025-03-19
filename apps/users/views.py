#restframework
from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

#django
import random
from django.utils.html import format_html


#apps
from .models import User
from .serializers import RegisterSerializer, ModifyPasswordSerializers, PersonalSerializers
from .utils import Util

class RegisterView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            email_body = format_html(f"""
                <div style="font-family: Arial, sans-serif; padding: 20px;">
                    <h2 style="color: #333;">Добро пожаловать, {user.first_name}!</h2>
                    <p>Ваш код подтверждения: <strong style="font-size: 20px;">{user.code}</strong></p>
                    <p>Введите этот код в приложении, чтобы завершить регистрацию.</p>
                    <br>
                    <p>С уважением,<br>Ваша команда</p>
                </div>
            """)
            email_data = {
                'email_subject': 'Подтверждение регистрации','email_body': email_body,'to_email': user.email}
            Util.send_email(email_data)

            return Response({"response": True,"message":
                "Пользователь зарегистрирован. Код подтверждения отправлен на вашу электронную почту."
            }, status=status.HTTP_201_CREATED)

        return Response({"response": False,
            "message": "Ошибка при регистрации пользователя."
        }, status=status.HTTP_400_BAD_REQUEST)


class PersonalView(viewsets.ViewSet):
    @action(detail=False, methods=['post'], url_path='modify-password')
    def modify_password(self, request):
        serializer = ModifyPasswordSerializers(data=request.data, instance=request.user)
        if serializer.is_valid():
            request.user.set_password(serializer.validated_data['password'])
            request.user.save()
            return Response({"responce": True, "message": "Пароль успешно обновлён."}, status=status.HTTP_200_OK)
        return Response({"responce": False, "message": "При изменении пароля произошла ошибка"}, status=status.HTTP_400_BAD_REQUEST)

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


