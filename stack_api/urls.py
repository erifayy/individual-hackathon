"""stack_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from rest_framework.routers import DefaultRouter

from main.views import ArticleViewSet, CommentViewSet, ChangePasswordView, RatingViewSet, ImageView

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


router = DefaultRouter()
router.register('articles', ArticleViewSet)
router.register('comments', CommentViewSet)
router.register('rating', RatingViewSet)


schema_view = get_schema_view(
   openapi.Info(
      title="The latest psychology news",
      default_version='v1',
      description="The best source of brain-storm information.",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="admin@gmail.com"),
      license=openapi.License(name="The Best License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', schema_view.with_ui()),
    path('api/v1/', include(router.urls)),
    path('api/v1/add-image/', ImageView.as_view()),
    path('api/v1/account/', include('account.urls')),
    path('api/v1/change-password/', ChangePasswordView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
