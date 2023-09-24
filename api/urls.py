from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken import views

from api.views import PostViewSet, GroupViewSet, CommentViewSet

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet)
router.register('posts/(?P<post_id>\\d+)/comments', CommentViewSet, basename='comments')
router.register(r'groups', GroupViewSet)

urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token),
    path('', include(router.urls)),
#    path('', include(router.urls)),
]