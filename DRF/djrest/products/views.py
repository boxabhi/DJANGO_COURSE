from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .documents import ProductsDocument
from django_elasticsearch_dsl.search import Search
from elasticsearch_dsl import Q


def index_product(request):
    return render(request, 'product_index.html')

class ProductElasticAPI(APIView):
    def get(self, request):
        search = request.GET.get('search')
        search = ProductsDocument.search().query(
            'multi_match', query=search, 
            fields=["product_name", "product_brand"],
             fuzziness="AUTO",
             operator="and",
             type="best_fields"
            ).extra(size =12)
        response = search.execute()
        
        products = []
        for hit in response:
            products.append({
                'product_name' : hit.product_name,
                'product_price' : hit.product_price,
                'product_brand' : hit.product_brand
            })

        return Response({
            'data' : products
        })