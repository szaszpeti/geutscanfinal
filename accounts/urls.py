from django.urls import path

from django.contrib.auth import views as auth_views

from . import views



urlpatterns = [
	path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),  
	path('logout/', views.logoutUser, name="logout"),

    path('', views.home, name="home"),
    #path('user/', views.userPage, name="user-page"),

    path('account/', views.accountSettings, name="account"),

    path('inspections/', views.inspections, name='inspections'),
    path('inspection_detail/<str:pk>', views.detailInspection, name='inspection_detail'),
    path('pandas_detail/<str:pk>', views.detailPandas, name='pandas_detail'),
    path('technician/<str:pk_test>/', views.technician, name="technician"),

    path('create_inspection/', views.createInspection, name="create_inspection"),
    path('update_inspection/<str:pk>/', views.updateInspection, name="update_inspection"),
    path('delete_inspection/<str:pk>/', views.deleteInspection, name="delete_inspection"),

    path('reset_password/',
     auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),
     name="reset_password"),

    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"), 
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"), 
     name="password_reset_confirm"),

    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"), 
        name="password_reset_complete"),



]