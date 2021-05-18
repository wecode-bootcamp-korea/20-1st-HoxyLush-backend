from django.urls     import path
from products.views  import ProductListView, LikeView

urlpatterns = [
    path("", ProductListView.as_view()),
    path("/like", LikeView.as_view()),
    path('/like/<int:post_id>/', views.like_items, name="like_items"),
    ]