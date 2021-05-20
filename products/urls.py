from django.urls     import path
from products.views  import ProductListView, ProductDetailView, ProductLikeView

urlpatterns = [
    path("", ProductListView.as_view()),
    path('/<int:product_id>', ProductDetailView.as_view()),
    path("/like", ProductLikeView.as_view()),
    ]