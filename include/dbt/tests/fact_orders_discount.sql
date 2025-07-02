-- Check if the monthly_revenue is never less than 0
SELECT
    *
FROM 
    {{ ref('fct_monthly_customers_revenue')}}
WHERE
    monthly_revenue_with_discount < 0
    AND 
    monthly_revenue_without_discount < 0