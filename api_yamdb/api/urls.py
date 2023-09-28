from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (CategoryViewSet,
                       GenreViewSet,
                       TitleViewSet,
                       user_created_view,
                       token_created_view,
                       UserViewSet,
                       ReviewViewSet,
                       CommentViewSet)

from api.views import CategoryViewSet, GenreViewSet, TitleViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')
router.register('users', UserViewSet, basename='users')
router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns_auth = [
    path('signup/', user_created_view),
    path('token/', token_created_view),
]

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/', include(urlpatterns_auth)),
]
