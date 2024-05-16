"""
URL configuration for Ecommerece project.

The urlpatterns list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from user_store import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/',views.home_page,name='home'),
    path('signup/',views.signup_form,name='signup'),
    path('login/',views.login_form,name='login'),
    path('logout/',views.logout_form,name='logout'),
    path('weblogin/',views.Website_Login_Form,name='weblogin'),
    path('profile/',views.home_page,name='profile'),
    path('userweb/',views.user_product,name='userweb'),
    path('yourproduct/',views.show_product,name='yourproduct'),
    path('delete/<int:pk>',views.DeleteUser_product.as_view(),name='delete'),
    path('update/<int:pk>',views.UpdateUser_product.as_view(),name='update'),
    path('bootproduct/<str:name>',views.boot_product.as_view(),name='bootproduct'),
    path('updatecomment/<int:pk>',views.YourCommentUpdate.as_view(),name='updatecomment'),
    path('deletecomment/<int:pk>',views.YourCommentDelete.as_view(),name='deletecomment'),
    path('comment/<int:id>',views.User_comments,name='comment'),
    path('addcart/<int:id>',views.add_cart,name='addcart'),
    path('viewcart/',views.view_cart,name='viewcart'),
    path('deletecartitem/<int:id>',views.delete_cart_items,name='deletecartitem'),


]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)