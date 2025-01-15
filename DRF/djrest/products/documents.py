from django_elasticsearch_dsl.registries import registry
from django_elasticsearch_dsl import Document, fields
from .models import *

@registry.register_document
class ProductsDocument(Document):
    class Index:
        name = "products"
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }
    class Django:
        model = Product
        fields = [
            "product_name",
            "product_brand",
            "product_price",
        ]