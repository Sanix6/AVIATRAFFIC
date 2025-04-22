from rest_framework import serializers

#django
from django.contrib.auth.password_validation import validate_password
from django.core.mail import send_mail


#apps
from .models import User



class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True, min_length=8,
                                    error_messages={"min_length": "Не менее 8 символов."})

    class Meta:
        model = User
        fields = ('email', 'first_name', 'phone','password', 'confirm_password')

    def validate(self, attrs):
        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")

        validate_password(password)

        if password != confirm_password:
            raise serializers.ValidationError({"password": "Пароли не совпадают!"})

        return attrs

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        user = User(**validated_data)
        user.set_password(validated_data["password"])
        user.save()

        # send_mail(
        #     "Подтверждение email",
        #     f"Ваш код подтверждения: {user.code}",
        #     "smtp.yandex.ru",
        #     [user.email],
        #     fail_silently=False,
        # )

        return user


class ModifyPasswordSerializers(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True, required=True, min_length=8,
                                             error_messages={"min_length": "Не менее 8 символов."})
    class Meta:
        model = User
        fields = ['password', 'confirm_password']

    def validate(self, attrs):
        password = attrs.get("password")
        confirm_password = attrs.get('confirm_password')
        validate_password(password)
        if password != confirm_password:
            raise serializers.ValidationError({"password": "Пароли не совпадают!"})

        return attrs

class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True)
    password = serializers.CharField(
        write_only=True,
        min_length=4,
        required=True,
        error_messages={"min_length": "Не менее 4 символов."},
    )
    

class PersonalSerializers(serializers.ModelSerializer):
    first_name = serializers.CharField(write_only=True)
    email = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'email']


