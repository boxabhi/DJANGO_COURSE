from django.shortcuts import render
from .models import Product
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector, TrigramSimilarity
from django.db.models import Q
def index(request):

    if search := request.GET.get('search'):
        query = request.GET.get('search', '')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        
        vector = SearchVector('title', 'description', 'category', 'brand', )
        search_query = SearchQuery(query)
    
        results = Product.objects.annotate(
            rank=SearchRank(vector, search_query),
            similarity=TrigramSimilarity('title', query) + TrigramSimilarity('description', query)
        ).filter(
            Q(rank__gte=0.3) | Q(similarity__gte=0.3)
        ).distinct().order_by('-rank', '-similarity')
        
        if min_price:
            results = results.filter(price__gte=min_price)
        if max_price:
            results = results.filter(price__lte=max_price)
    
    else:
        results = Product.objects.all()



    return render(request, 'index.html', {'results': results , 'search' :request.GET.get('search') })