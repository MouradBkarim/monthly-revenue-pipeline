SELECT
  o.order_date,
  l.extended_price * (1 - l.discount) as revenue,
  {{ net_revenue('l.extended_price', 'l.discount') }} AS net_revenue,
  o.customer_key
FROM 
    {{ ref('stg_tpch_orders') }} o
JOIN 
    {{ ref('stg_tpch_line_item') }} l
  ON o.order_key = l.order_key