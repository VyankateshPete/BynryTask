   @app.route('/api/companies/<int:company_id>/alerts/low-stock', methods=['GET'])
   def low_stock_alerts(company_id):
       alerts = []
       # TO get porducts with low stocks
       products = Product.query.join(Inventory).filter(Inventory.quantity < Inventory.threshold).all()
       
       for product in products:
           # Check for recent sales activity
           if has_recent_sales(product.id):
               alerts.append({
                   "product_id": product.id,
                   "product_name": product.name,
                   "sku": product.sku,
                   "warehouse_id": product.warehouse_id,
                   "warehouse_name": get_warehouse_name(product.warehouse_id),
                   "current_stock": get_current_stock(product.id),
                   "threshold": get_threshold(product.id),
                   "days_until_stockout": calculate_days_until_stockout(product.id),
                   "supplier": get_supplier_info(product.id)
               })
       
       return {"alerts": alerts, "total_alerts": len(alerts)}
   
