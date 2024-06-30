from django.shortcuts import render
from django.http import JsonResponse
from products.documents import ProductDocument


def search_product(request):
    data = {}
    data = {
        "status" : 200,
        "message" : "Products",
        "products" : []
    }
    if request.GET.get('search'):
        search = request.GET.get('search').split(',')
        result = ProductDocument.search().query(
            'terms', brand_name__brand_name = search
        ).extra(from_= 1 , size = 3)
        result = result.execute()
        products = [
            {
                "title": hit.title,
                "description": hit.description,
                "category": hit.category,
                "price": hit.price,
                "brand": hit.brand,
                "sku": hit.sku,
                "thumbnail": hit.thumbnail,
                "score" : hit.meta.score,
            }
            for hit in result
        ]
        print(len(products))
        data['products'] = products
    return JsonResponse(data)