from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Product, Feedback
import json


def product_list(request):
    products = Product.objects.all().values(
        'id', 'name', 'description', 'price', 'created_at')

    return JsonResponse(list(products), safe=False)


def get_product_details(request, product_id):
    """
    Fetches details of a specific product by its ID.
    """
    try:
        product = Product.objects.get(id=product_id)
        product_details = {
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': str(product.price),  # Convert Decimal to string for JSON serialization
            'created_at': product.created_at.isoformat(),  # Convert to ISO format for JSON serialization
        }
        return JsonResponse(product_details, safe=False)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)

@csrf_exempt  # Temporarily disable CSRF token for testing purposes (not recommended for production)
def submit_feedback(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            email = data.get('email')
            message = data.get('message')

            if not name or not email or not message:
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            # Save feedback in the database
            feedback = Feedback.objects.create(name=name, email=email, message=message)
            return JsonResponse({'message': 'Feedback submitted successfully!'}, status=201)
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    
    return JsonResponse({'error': 'Invalid HTTP method'}, status=405)