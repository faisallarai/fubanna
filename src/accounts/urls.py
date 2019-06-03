from django.urls import path, re_path

from .views import (LogoutPageView, AgentUserListView, AgentUserDetailView,
                    RegisterView, LoginPageView, send_login_email, activate_login_email,
                    UserActivationSentView)

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginPageView.as_view(), name='login'),
    path('send_email/', send_login_email, name='send_login_email'),
    path('activate_email/<uuid:uid>/', activate_login_email, name='activate'),
    path('logout/', LogoutPageView.as_view(), name='logout'),
    path('accounts/', AgentUserListView.as_view(), name='accounts-list'),
    path('accounts/<int:pk>/', AgentUserDetailView.as_view(),
         name='accounts-detail'),
    path('user_activation_sent/', UserActivationSentView.as_view(),
         name='user_activation_sent'),
    # re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #        agent_activation_view, name='activate'),
]
