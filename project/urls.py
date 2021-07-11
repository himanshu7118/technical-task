from django.urls import path, include
from project import views

from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    # path('home', views.home, name="home"),
    # path('signup', views.signup, name='sign-up'),
    path('registeruser', views.RegisterUserView.as_view(), name='register_user'),
    path('userinfo/', views.UserInfoView.as_view(), name='doctor_info'),
    # path('login', views.login, name='login'),
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('password_reset/confirm/', include('django_rest_passwordreset.urls', namespace='password_reset_confirm')),
    path('product/',views.ProductView.as_view(),name='Product'),
    path('product/<int:pk>',views.ProductView.as_view(),name='Product'),
    path('product_category/',views.ProductCategoryView.as_view(),name='Product-Category'),
    path('product_category/<int:pk>',views.ProductCategoryView.as_view(),name='Product-Category'),
    path('order/',views.OrderView.as_view(),name='Order'),
    path('order_list/<int:pk>',views.OrderList.as_view(),name='Order-List'),
    path('order_update/',views.OrederUpdateView.as_view(),name='Order-update'),
    path('order_delete/',views.OrderDeleteView.as_view(),name='Order-delete'),
    path('offer_list/',views.OfferListView.as_view(),name='Offer-List'),
    path('offer/',views.OfferView.as_view(),name='Offer'),
    path('offer/<int:pk>',views.OfferView.as_view(),name='Offer-update-delete'),
    path('order_product_list/',views.OrderProductListview.as_view(),name='Order-Product-List'),
    path('addtocart/',views.AddToCart.as_view(),name='Addtocart'),


]
