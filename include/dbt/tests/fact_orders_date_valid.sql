-- Make sure that the order_date is between today and 1990-01-01
SELECT
    *
FROM
    {{ ref('fct_monthly_customers_revenue') }}
WHERE
    month IS NULL
    OR month > CURRENT_DATE()
    OR month < DATE('1990-01-01')    