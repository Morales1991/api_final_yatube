from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import PostViewSet, CommentViewSet, GroupList, FollowList

router = DefaultRouter()
router.register('posts', PostViewSet)
router.register(r'posts/(?P<post_id>\d+)/comments', CommentViewSet)


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='Get_token'),
    path('token/refresh/', TokenRefreshView.as_view, name='Refresh_token'),
    path('group/', GroupList.as_view(), name='Group' ),
    path('follow/', FollowList.as_view(), name='Follow' ),
    path('',include(router.urls)),
]
