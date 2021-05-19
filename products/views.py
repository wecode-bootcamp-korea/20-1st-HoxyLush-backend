import json

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
        
        return JsonResponse({'Product_Info' : product_list}, status = 200)

class ProductLikeView(View):
    @login_required
    def get(self, request):
        like_list      = request.user.product_set.all()
        
        like_items = [{
            'product_id'  : product.id,
            'name'        : product.name, 
            'hashtag'     : product.hashtag,
            'price'       : product.productoption_set.first().price,
            'image_url'   : product.productimage_set.first().image_url,
        }for product in like_list]
        
        return JsonResponse({'Like_Items' : like_items}, status = 200)
    
    @login_required
    def post(self,request):
        try:
            data           = json.loads(request.body)
            product_id     = data.get('product_id')
            like_list      = request.user.product_set.all()

            if Like.objects.filter(product_id=product_id, user=request.user).exists():
                request.user.product_set.remove(product_id)

            else:    
                request.user.product_set.add(product_id)

        except KeyError:
            return JsonResponse({'Message' : 'KEY_ERROR'}, status = 400)

        return JsonResponse({'Message' : 'SUCCESS'}, status = 200)