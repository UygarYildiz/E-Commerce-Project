{{ config(materialized="view")}}

WITH source AS (
    SELECT
        order_id,
        customer_id,
        order_status,
        order_purchase_timestamp,
        order_approved_at,
        order_delivered_carrier_date,
        order_delivered_customer_date,
        order_estimated_delivery_date
    FROM {{source ("raw","olist_orders")}}
),

cleaned AS(
    SELECT
        order_id,
        customer_id,
        TRIM(UPPER(order_status)) AS order_status,
        order_purchase_timestamp,
        order_approved_at,
        order_delivered_carrier_date,
        order_delivered_customer_date,
        order_estimated_delivery_date
    FROM source
)
,
final AS(
    SELECT * FROM cleaned
        
)

SELECT * FROM final
