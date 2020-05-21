from django.conf.urls.static import static
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.urls import path
from django.conf import settings
from django.views.generic import TemplateView
from django.conf.urls import url
from . import views
from .views import  user_details, HomeView, UserListView, RegistrationView, ProfileView, EditProfileView
from allauth.account.views import LoginView, LogoutView, PasswordResetView
urlpatterns = [
    path('home', HomeView.as_view(), name='home'),
    path('details/<str:pk>', user_details, name='user_detail'),
    path('users_list', UserListView.as_view(), name='list'),
    path('signup', RegistrationView.as_view(), name='registration'),
    path('profile/<str:pk>', ProfileView.as_view(), name='profile'),
    path('accounts/profile/edit', EditProfileView.as_view(), name='edit_profile'),
    path('contacts', views.contactform, name='contacts'),
    path('thanks', views.thanks, name='thanks'),
    path('login', LoginView.as_view(), name='custom_login'),
    path('logout', LogoutView.as_view(), name='custom_logout'),
    path('password_reset', PasswordResetView.as_view(), name='custom_reset_password'),
    path('dialogs', login_required(views.DialogsView.as_view()), name='dialogs'),
    path('dialogs/create/<str:user_id>', login_required(views.CreateDialogView.as_view()), name='create_dialog'),
    path('dialogs/<str:chat_id>', login_required(views.MessagesView.as_view()), name='messages'),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





