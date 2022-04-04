from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [path('', views.IndexView.as_view(), name='main'),
               path('app_goods/index/',
                    views.IndexView.as_view(),
                    name='main'),

               path('app_goods/product_list/',
                    views.ProductListView.as_view(),
                    name='product-list'),

               path('app_goods/top_items/',
                    views.TopListView.as_view(),
                    name='top-items'),

               path('app_goods/list_carts/',
                    views.ListCart.as_view(),
                    name='list-cart'),

               path('app_goods/list_cartitems/',
                    views.ListCartItem.as_view(),
                    name='list-cartitem'),

               path('app_goods/top_balance/',
                    views.AppTopBalance.as_view(),
                    name='top-balance'),

               path('app_goods/login/',
                    views.AppLoginView.as_view(),
                    name='login'),

               path('app_goods/logout/>',
                    views.AppLogoutView.as_view(),
                    name='logout'),

               path('app_goods/register/',
                    views.AppRegisterView.as_view(),
                    name='register'),

               path('app_goods/profile/<int:pk>/',
                    views.AppProfileView.as_view(),
                    name='profile'),

               ] \
              + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
              + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
