from django.shortcuts import render
from .models import Product
from django.contrib.postgres.search import (SearchVector, SearchQuery, SearchRank,
                                            TrigramSimilarity
                                            )
from django.db.models import Q


def index(request):

    if search := request.GET.get('search'):
        query = SearchQuery(search)
        vector =  SearchVector(
            "title",
            "description",
            "category",
            "brand"
        )
        rank = SearchRank(vector, query)
        results = Product.objects.annotate(
            rank = rank,
            similarity = TrigramSimilarity('title', search) 
            + TrigramSimilarity('description', search) + TrigramSimilarity('category', search)
            + TrigramSimilarity('brand', search)
        ).filter(Q(rank__gte =0.3)| Q(similarity__gte = 0.3)).distinct().order_by('-rank', '-similarity')
    else:
        results = Product.objects.all()


    if request.GET.get('min_price') and request.GET.get('max_price') :
        min_price = float(request.GET.get('min_price'))
        max_price = float(request.GET.get('max_price'))
        results = results.filter(
            price__gte=min_price, price__lte=max_price
        ).order_by('price')

    if request.GET.get('brand'):
        print("brand")

        results = results.filter(
            brand__icontains = request.GET.get('brand')
        ).order_by('price')

    if request.GET.get('category'):
        print("cateory")
        results = results.filter(
            category__icontains = request.GET.get('category')
        ).order_by('price')

    brands = Product.objects.all().distinct('brand').order_by('brand')
    categories = Product.objects.all().distinct('category').order_by('category')


    return render(request, 'index.html', {'results': results ,
                                          'brands' : brands,
                                          'categories' : categories,
                                           'search' :request.GET.get('search') })