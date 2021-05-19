from django.urls     import path
from products.views  import ProductListView, ProductLikeView

urlpatterns = [
    path("", ProductListView.as_view()),
    path("/like", ProductLikeView.as_view()),
    ]