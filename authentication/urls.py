from re import template
from django.urls import path
from. import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    # path('register/',views.registerFunction,name="register"),

   path('reg/', views.SignUp_function, name='reg'),
   path('login/', views.Login_function, name='login'),  
   path('verify/',views.verifyUser,name="verify"),
   path("logout/", auth_views.LogoutView.as_view(next_page='/'), name="logout"),
   path('reset_password/', auth_views.PasswordResetView.as_view(template_name="forget-password.html"),name="reset_password"),
   path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="resetpassword_check.html"),name="password_reset_done"),
   path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="change-password.html"),name="password_reset_confirm"),
   path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="reset_password_done.html"),name ='password_reset_complete'),
   path('changePassword/',views.changePassword,name="changepassword"),
]
