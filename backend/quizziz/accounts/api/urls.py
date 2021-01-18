from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from accounts.api.views import SignupView, AccountAPI, AccountQuizzesAPI, CurrentAccountAPI


urlpatterns = [
    path('login/', include([
        path('', TokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    ])),
    path('signup/', SignupView.as_view(), name='signup'),
    path('account/<slug:account_slug>/', include([
        path('', AccountAPI.as_view(), name='account'),
        path('quizzes/', AccountQuizzesAPI.as_view(), name='account-quizzes'),
    ])),
    path('current/', include([
        path('', CurrentAccountAPI.as_view(), name='account-profile'),
    ])),
]
