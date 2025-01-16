
search = ProductsDocument.search().query(
            'match',
            product_name = search
            ).extra(size =12)


search = ProductsDocument.search().query(
    'multi_match', query=search, 
    fields=["product_name", "product_brand"]
    ).extra(size =12)
response = search.execute()


 search = ProductsDocument.search().query(
            'multi_match', query=search, 
            fields=["product_name", "product_brand"],
             fuzziness="AUTO",
             operator="and",
             type="best_fields"
            ).extra(size =12)
        response = search.execute()