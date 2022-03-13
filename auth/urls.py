from django.urls import path
from auth.views import ObtainTokenPairView, RegisterView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('signin/', ObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('pair/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', RegisterView.as_view(), name='auth_register'),
]
