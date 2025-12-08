-- TEKİL PRIMARY KEYLERİN EKLENMESİ

ALTER TABLE olist_customers ADD PRIMARY KEY (customer_id);
ALTER TABLE olist_orders ADD PRIMARY KEY (order_id);
ALTER TABLE olist_sellers ADD PRIMARY KEY (seller_id);
ALTER TABLE olist_products ADD PRIMARY KEY (product_id);

ALTER TABLE olist_order_reviews ADD PRIMARY KEY (review_id,order_id); -- Duplicate vardı o yüzden Composite yapıldı
ALTER TABLE product_category_name_translation ADD PRIMARY KEY (product_category_name);

-- Kompozit Primary Key'ler
ALTER TABLE olist_order_items ADD PRIMARY KEY (order_id,order_item_id);
ALTER TABLE olist_order_payments ADD PRIMARY key (order_id,payment_sequential);