SELECT 
    n_nationkey as nation_key,
    n_name as name,
    n_regionkey as region_key,
    n_comment as comment,
FROM 
    {{source('tpch', 'nation')}}