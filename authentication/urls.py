from django.urls import path
from authentication import views as auth
from django.contrib.auth import views as reset
from mainpage import views as mainpage
from .forms import CustomPasswordResetForm

urlpatterns = [
	
	path('login', auth.loginView, name='login'),
	path('register', auth.registerView, name='register'),
	path('logout', auth.logoutUser, name='logout'),
	path('products', mainpage.recommendedProducts, name='products'),
	path('reset_password/', reset.PasswordResetView.as_view(template_name="resetPassword.html",form_class=CustomPasswordResetForm), name="reset_password"),
	path('new_password_send/', reset.PasswordResetDoneView.as_view(template_name="resetPasswordDone.html",), name="reset_password_done"),
	path('reset/<uidb64>/<token>/', reset.PasswordResetConfirmView.as_view(template_name=""), name="reset_password_confirm"),
	path('reset_password_complete/', reset.PasswordResetCompleteView.as_view(template_name="resetPasswordComplete.html"), name="reset_password_complete"),
]