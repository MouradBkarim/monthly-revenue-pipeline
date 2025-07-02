SELECT
  c.customer_key,
  n.name as nation,
  r.name as region
FROM 
    {{ ref('stg_tpch_customer') }} c
JOIN 
    {{ ref('stg_tpch_nation') }} n
  ON c.nation_key = n.nation_key
JOIN 
    {{ ref('stg_tpch_region') }} r
  ON n.region_key = r.region_key
