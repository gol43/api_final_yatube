from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import GroupView, PostView, CommentView, FollowView

router = DefaultRouter()
router.register(r'groups', GroupView,
                basename='group')
router.register(r'posts', PostView,
                basename='posts')
router.register(
    r'posts/(?P<post_id>\d+)/comments', CommentView,
    basename='comments')
router.register(r'follow', FollowView,
                basename='follow')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]
# можно было бы наверное сделать и через
# 'v1/api-token-auth/', views.obtain_auth_token,
# но решил применить второй способ
