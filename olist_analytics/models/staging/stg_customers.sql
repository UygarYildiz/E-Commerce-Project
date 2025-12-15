{{config(materialized="view")}}

WITH source AS(
    SELECT
        customer_id,
        customer_unique_id,
        customer_zip_code_prefix,
        customer_city,
        customer_state
    FROM {{source("raw","olist_customers")}}

 
),
cleaned AS(
    SELECT
        customer_id,
        customer_unique_id,
        customer_zip_code_prefix,
        TRIM(upper(customer_city)) AS customer_city,
        TRIM(upper(customer_state)) AS customer_state
    FROM source
),
final AS(
    SELECT
        customer_id,
        customer_unique_id,
        customer_zip_code_prefix,
        customer_city,
        customer_state
    FROM cleaned
)
SELECT * FROM final



