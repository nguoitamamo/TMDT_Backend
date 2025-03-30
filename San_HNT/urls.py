

from django.urls import path, include
from . import views
from rest_framework import routers




r = routers.DefaultRouter()
r.register('products', views.ProductViewSet )
r.register('users', views.UserViewSet)
r.register('permissions' , views.PermissionViewSet)
r.register('categorys', views.CategoryViewSet)
r.register('suppliers', views.SupplierViewSet)
r.register('comments', views.CommentViewSet)
r.register('customers', views.CustomerViewSet)
r.register('ordes', views.OrderViewSet)




urlpatterns = [
    path('', include(r.urls)),

]
