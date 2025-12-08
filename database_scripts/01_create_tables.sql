
-- Müşteri tablosu
create table if not exists olist_customers (
	customer_id VARCHAR(50),
	customer_unique_id VARCHAR(50) ,
	customer_zip_code_prefix VARCHAR(50),
	customer_city VARCHAR(50),
	customer_state VARCHAR(50)
);

-- Sipariş tablosu 
create table if not exists olist_orders(
	order_id VARCHAR(50),
	customer_id VARCHAR(50),
	order_status VARCHAR(20),
	order_purchase_timestamp TIMESTAMP ,
	order_approved_at TIMESTAMP,
    order_delivered_carrier_date TIMESTAMP,
    order_delivered_customer_date TIMESTAMP,
    order_estimated_delivery_date TIMESTAMP

);

-- Konum tablosu
create table if not exists olist_geolocation(
	geolocation_zipcode_prefix VARCHAR,
	geolocation_lat float,
	geolocation_lng float,
	geolocation_city VARCHAR(50),
	geolocation_state VARCHAR(10)
);

-- Sipariş ürün tablosu
create table if not exists olist_order_items(
	order_id VARCHAR(50),
	order_item_id int,
	product_id VARCHAR(50),
	seller_id VARCHAR(50),
	shipping_limit_date TIMESTAMP,
	price DECIMAL,
  	freight_value DECIMAL
			
);

-- Ürün tablosu
create table if not exists olist_products( 
	product_id VARCHAR(50),
	product_category_name VARCHAR(50),
	product_name_lenght int,
	product_description_lenght int,
	product_photos_qty int,
	product_weight_g int,
	product_length_cm int,
	product_height_cm int,
	product_width_cm int
	
);

-- Satıcı tablosu
create table if not exists olist_sellers(
	seller_id VARCHAR(50),
	seller_zip_code_prefix VARCHAR(50),
	seller_city VARCHAR(50),
	seller_state VARCHAR(50)
);

-- Sipariş inceleme tablosu
create table if not exists olist_order_reviews(
	review_id VARCHAR(50),
    order_id VARCHAR(50),
	review_score INT,
	review_comment_title VARCHAR(50),
	review_comment_message TEXT,
	review_creation_date TIMESTAMP,
	review_answer_timestamp TIMESTAMP
);


-- Ödeme  tablosu

create table if not exists olist_order_payments(
	order_id VARCHAR(50),
    payment_sequential int,
    payment_type varchar(50),
    payment_installments int,
    payment_value decimal 

);

-- Ürün kategori ismi tablosu
create table if not exists product_category_name_translation(
	product_category_name VARCHAR(50),
	product_category_name_english VARCHAR(50)
);












































