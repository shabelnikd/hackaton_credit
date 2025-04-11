from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .tasks import send_activation_mail
from .models import UserModel

AbstractUser = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbstractUser
        fields = ('email', 'full_name', 'password', 'phone_number')

    def create(self, validated_data):
        print(validated_data)
        user = AbstractUser.objects.create_user(**validated_data)
        user.create_activation_code()
        send_activation_mail(user.email, user.activation_code)
        return user


class LoginSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=6, required=True)

    def validate_email(self, email):
        if not AbstractUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('Пользователь не зарегистрирован')
        return email

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.pop('password')
        user = AbstractUser.objects.get(email=email)
        user.set_password(password)

        if not user.check_password(password):
            raise serializers.ValidationError('Неверный пароль')
        if not user.is_active:
            raise serializers.ValidationError('Активируйте свою учетную запись через email')
        if not user:
            raise serializers.ValidationError('Пользователь не найден (Непредвиденная ошибка)')

        refresh = self.get_token(user)

        attrs['user_id'] = user.id
        attrs['full_name'] = user.full_name

        attrs['phone_number'] = user.phone_number
        attrs['tokens'] = {'access': str(refresh.token), 'refresh': str(refresh)}

        return attrs


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, email):
        if not AbstractUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('Такого пользователя не существует')
        return email


class CreateNewPasswordSerializer(serializers.Serializer):
    activation_code = serializers.CharField(required=True)
    password = serializers.CharField(min_length=6, required=True)

    def validate_activation_code(self, code):
        if not AbstractUser.objects.filter(activation_code=code).exists():
            raise serializers.ValidationError('Активационный код введен неверно')
        return code

    def create_pass(self):
        code = self.validated_data.get('activation_code')
        password = self.validated_data.get('password')
        user = AbstractUser.objects.get(activation_code=code)
        user.set_password(password)
        user.activation_code = ''
        user.save()


class ChangePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbstractUser
        fields = 'password'

    def set_new_password(self):
        user = self.instance
        user.set_password(self.validated_data['password'])
        user.save()



class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbstractUser
        fields = "__all__"



class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbstractUser
        fields = "__all__"


