import re
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(CustomTokenObtainPairSerializer, cls).get_token(user)

        token['username'] = user.username
        return token


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', )

    # Validazione della password - Un'alternativa era scrivere delle classi di validazione vere e proprie
    def validate(self, attrs):

        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords didn't match."})

        if len(attrs['password']) < 6:
            raise serializers.ValidationError({"password": "Password is too short (min 6 chars)."})

        # Per controllare i caratteri uso regex
        criteria = re.compile("^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[-+_!@#$%^&*., ?]).+$")
        if not re.search(criteria, attrs['password']):
            raise serializers.ValidationError({"password": "Password must contain at least 1 lower case, 1 upper "
                                                           "case, 1 special character and 1 digit"})
        return attrs

    # Creo l'utente usando create. Volendo c'era anche create_user
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

