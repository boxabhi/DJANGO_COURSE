from django.shortcuts import render
from products.models import Category, VendorProducts,ProductVariant,Products


def home(request):
    categories = Category.objects.all()
    products = VendorProducts.objects.filter(
        product__product_images__isnull =False, product__parent_product__isnull = True)[:30]
    context = {
        "categories" : categories,
        "products" : products,
    }
    return render(request, 'home/home.html', context)



def product_detail(request, id):
    product = VendorProducts.objects.get(id = id)
    if request.GET.get('product_sku'):
        product = VendorProducts.objects.get(product__product_sku = request.GET.get('product_sku'))
    product_variants = []
    if product.product.product_variants.exists():
        parent_variants = product.product.product_variants.prefetch_related('variant_option')
        for variant in parent_variants:
            product_variants.extend(
                {
                    "product_sku": product.product.product_sku,
                    "option_name": option.option_name,
                    "variant_name": option.variant_name,
                }
                for option in variant.variant_option.all()
            )

    variant_products = []
    if product.product.parent_product:
        variant_products = [product.product.parent_product]
    else:
        variant_products = product.product.variant_products.all()


    for vp in variant_products:
        product_variant = ProductVariant.objects.filter(product = vp).first()
        product_variants.extend(
            {
                "product_sku": vp.product_sku,
                "option_name": option.option_name,
                "variant_name": option.variant_name,
            }
            for option in product_variant.variant_option.all()
        )
    result = {}
    sorted_variants = sorted(product_variants, key=lambda x:x['product_sku'])
    for variant in sorted_variants:
        product_sku = variant['product_sku']
        variant_string = f"{variant['variant_name']}: {variant['option_name']}"
        
        if product_sku in result:
            result[product_sku].add(variant_string)  
        else:

            result[product_sku] = {variant_string}

    for product_sku in result:
        result[product_sku] = " ".join(result[product_sku])

    context = {
        'product': product,
        'product_variants': result,
    }

    print(result)

    return render(request, 'home/product_details.html', context)