     @app.route('/api/products', methods=['POST'])
     def create_product():
         data = request.json
         
         #To validate if sku is unique
         if Product.query.filter_by(sku=data['sku']).first():
             return {"error": "SKU must be unique"}, 400
         
         #To check if price is decimal, int or not
         if not isinstance(data['price'], (int, float)):
             return {"error": "Price must be a decimal value"}, 400
         
         # To create a new product
         product = Product(
             name=data['name'],
             sku=data['sku'],
             price=data['price'],
         )
         db.session.add(product)
         db.session.commit()
         
         # To update the inventory
         inventory = Inventory(
             product_id=product.id,
             warehouse_id=data['warehouse_id'],
             quantity=data.get('initial_quantity', 0)  # Need to initialize the quantity with 0 to make sure it's not null or something else.
         )
         db.session.add(inventory)
         db.session.commit()
         
         return {"message": "Product created", "product_id": product.id}
     
