import json

from django.shortcuts       import get_object_or_404
from django.http            import JsonResponse
from django.views           import View
from django.db.models       import Q

from products.models        import Category, Product, ProductImage, SubCategory, ProductTag, Tag

from util.utils             import login_required

class ProductListView(View):
    def get(self, request):
        category_id       = request.GET.get('category_id')
        sub_category_id   = request.GET.get('sub_category_id')
        keyword           = request.GET.get('keyword')
        pagination        = int(request.GET.get('pagination', 0))
        limit             = int(request.GET.get('limit', 4)) #프론트에서 limit값 올리면 tag 필터링 가능함.
        offset            = pagination * 4
        
        if category_id or sub_category_id:
            products = Product.objects.filter(
                Q(category_id = category_id) |
                Q(sub_category_id = sub_category_id))[offset:offset+limit]

        elif keyword:
            products= Product.objects.filter(name__contains = keyword)
            
        else:
            products = Product.objects.all()[offset:offset+limit]

        product_list = [{
            'id'            : product.id,
            'name'          : product.name,
            'hashtag'       : product.hashtag,
            'option' : [{ 
                'option_id'     : option.id,
                'price'         : option.price,
                'quantity'      : option.quantity,
                'weight'        : option.weight,
                } for option in product.productoption_set.all()],
            'image_url'     : product.productimage_set.first().image_url,
            'tag'    : [{'id' : tag.id, 'tag': tag.name} for tag in product.tag_set.all()]
            } for product in products]
            # Tag 클릭하면 해당 제품으로 가는 기능 추가해야됨.
        
        return JsonResponse({'product_info' : product_list}, status = 200)

class LikeView(View):
    @login_required
    def post(self, request):
        post = get_object_or_404(Post, id=post_id)

        if request.user in post.like_users.all():
            post.like_users.remove(request.user)
        else:
            post.like_users.add(request.user)