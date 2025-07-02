SELECT 
    c_custkey as customer_key,
    c_name  as customer_name,
    c_address as address,
    c_nationkey as nation_key,
    c_phone as phone,
    c_acctbal as acctual_bal,
    c_mktsegment as mkt_segment,
    c_comment as comment,
FROM 
    {{ source('tpch', 'customer')}}