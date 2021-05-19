import json

from django.shortcuts       import get_object_or_404
from django.http            import JsonResponse
from django.views           import View
from django.db.models       import Q

from products.models        import Category, Product, ProductImage, SubCategory, ProductTag, Tag, Like, User

from util.utils             import login_required

class ProductListView(View):
    def get(self, request):
        category_id       = request.GET.get('category_id')
        sub_category_id   = request.GET.get('sub_category_id')
        keyword           = request.GET.get('keyword')
        pagination        = int(request.GET.get('pagination', 0))
        limit             = int(request.GET.get('limit', 4))
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
        
        return JsonResponse({'product_info' : product_list}, status = 200)

class ProductLikeView(View):
    @login_required
    def get(self, request):     #전체 찜상품 조회기능
        like_list   = request.user.product_set.all()
        
        like_items = [{
            'name'        : product.name, 
            'hashtag'     : product.hashtag,
            'price'       : product.productoption_set.first().price,
            'image_url'   : product.productimage_set.first().image_url,
        }for product in like_list]
        
        return JsonResponse({'like_items' : like_items}, status = 200)
    
    @login_required
    def post(self,request):     #찜 추가 및 삭제 기능
        data           = json.loads(request.body)
        product_id     = data.get('product_id')
        product        = Product.objects.get(id=product_id)
        products       = Product.objects.all()
        like_list      = request.user.product_set.all()

        if Like.objects.filter(product_id=product_id).exists():
            user.product_set.remove(product_id)

        else:    
            user.product_set.add(product_id)

        like_items = [{
            'name'        : product.name, 
            'hashtag'     : product.hashtag,
            'price'       : product.productoption_set.first().price,
            'image_url'   : product.productimage_set.first().image_url,
        }for product in like_list]

        return JsonResponse({'like_items' : like_items}, status = 200)