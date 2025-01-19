from django.urls import path
from accounts.views import CustomerRegistrationView
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from accounts.forms import LoginForm,MyPasswordChangeForm,MyPasswordResetForm,MySetPasswordForm
from accounts.views import CustomerRegistrationView, CustomPasswordChangeView,ProfileView,About,Faq,Reviews

urlpatterns = [
    
    # Authentication

    path('register/',CustomerRegistrationView.as_view(), name='register'),

    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html', authentication_form=LoginForm), name='login'),

    path('logout/', auth_views.LogoutView.as_view(next_page='Home'),
         name='logout'),

    path('password-change/',
          CustomPasswordChangeView.as_view(
             template_name='accounts/passwordchange.html',
             form_class=MyPasswordChangeForm,
             # Redirect to profile page after successful change
             success_url=reverse_lazy('login')
         ),
         name='password_change'
         ),


    path('password-reset/',
         auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html', form_class=MyPasswordResetForm), name="password_reset"),


    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name="password_reset_done"),



    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_confirm.html', form_class=MySetPasswordForm), name="password_reset_confirm"),


    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='accounts/password_reset_complete.html'
         ),
         name="password_reset_complete"),


     # profile

     path('profile/', ProfileView.as_view(), name='profile'),


     path('about-us/', About, name='aboutus'),
     path('FAQ/', Faq, name='FAQ'),
     path('reviews/', Reviews, name='review'),
]