SELECT
  date_trunc('month', o.order_date) as month,
  c.nation,
  c.region,
  o.customer_key as customer_id,
  sum(o.net_revenue) as monthly_revenue_with_discount,
  sum(o.revenue) as monthly_revenue_without_discount
FROM 
  {{ ref('int_orders_lineitem') }} o
JOIN 
  {{ ref('int_customer_region') }} c
  on o.customer_key = c.customer_key
GROUP BY 1, 2, 3, 4
