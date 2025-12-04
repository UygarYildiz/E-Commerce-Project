ALTER TABLE olist_orders 
    ADD CONSTRAINT fk_orders_customers 
    FOREIGN KEY (customer_id) REFERENCES olist_customers(customer_id);


ALTER TABLE olist_products
    ADD CONSTRAINT fk_products_category_name_translation
    FOREIGN KEY (product_category_name) REFERENCES product_category_name_translation(product_category_name);

ALTER TABLE olist_order_payments
    ADD CONSTRAINT fk_order_payments_orders
    FOREIGN KEY (order_id) REFERENCES olist_orders(order_id);


ALTER TABLE olist_order_reviews
    ADD CONSTRAINT fk_order_reviews_orders
    FOREIGN KEY (order_id) REFERENCES olist_orders(order_id);


ALTER TABLE olist_order_items
    ADD CONSTRAINT fk_order_items_orders
    FOREIGN KEY (order_id) REFERENCES olist_orders(order_id),
    ADD CONSTRAINT fk_order_items_products
    FOREIGN KEY (product_id) REFERENCES olist_products(product_id),
    ADD CONSTRAINT fk_order_items_sellers 
    FOREIGN KEY (seller_id) REFERENCES olist_sellers(seller_id);
   


 