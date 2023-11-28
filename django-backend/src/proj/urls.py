"""
URL configuration for proj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from rest_framework.routers import SimpleRouter


from product.views import ProductViewSet
from category.views import CategoryViewSet
from waiter.views import WaiterViewSet

router = SimpleRouter()
router.register(r'product', ProductViewSet, basename='product')
router.register(r'category', CategoryViewSet, basename="category")
router.register(r'waiter', WaiterViewSet, basename="waiter")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('user_auth.urls')),
    path('api-my_auth/', include('rest_framework.urls')),
    path('api/v1/', include(router.urls)),
    path('', include('category.urls')),
    path('panel/', include('admin_p.urls')),
    path('tables/', include('tables.urls')),
    path('waiters/', include('waiter.urls')),

]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




