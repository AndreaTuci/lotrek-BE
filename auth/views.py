from .serializers import CustomTokenObtainPairSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, status
from django.contrib.auth.models import User
from .serializers import RegisterSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


# Nel documento è richiesto un Token semplice ma ho predisposto per JWT
class ObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = CustomTokenObtainPairSerializer

    # Override di post per restituire nel formato richiesto
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)

        # Eccezione generica, così restituisco la risposta nel formato richiesto
        except Exception:
            return Response({"result": "Cannot login with provided credentials"}, status=status.HTTP_400_BAD_REQUEST)

        # La TokenObtainPairView mi restituirebbe 'refresh' e 'access' come chiavi
        # copio 'access' in 'token' e poi rimuovo dal dizionario la vecchia chiave.
        # Rispetto alla richiesta ho in più 'refresh'.
        serializer.validated_data['token'] = serializer.validated_data['access']
        serializer.validated_data.pop('access')
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    # Override di create per restituire gli errori e il messaggio di successo nel formato richiesto
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=False):
            errors = []
            for key, values in serializer.errors.items():
                errors = [value[:] for value in values]
            return Response({"result": "Error creating the user,", "errors": errors},
                            status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"result": "User successfully created."}, status=status.HTTP_201_CREATED, headers=headers)


# Questa non la uso, è un'altra vista per ottenere il token
# Scritta prima di usare JWT
class SignInView(APIView):

    def get(self, request):
        content = {
            'token': str(request.auth),
        }
        return Response(content)
