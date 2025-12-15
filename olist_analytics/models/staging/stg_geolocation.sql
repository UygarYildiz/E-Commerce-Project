
{{config(materialized="view")}}
with quartiles as(
	select 
		PERCENTILE_CONT(0.25) within group (order by geolocation_lat  ) as Q1_lat,
		PERCENTILE_CONT(0.75) within group (order by geolocation_lat) as Q3_lat,
		PERCENTILE_CONT(0.25) within group (order by geolocation_lng )as Q1_lng,
		PERCENTILE_CONT(0.75) within group (order by geolocation_lng) as Q3_lng
	from {{source("raw","olist_geolocation")}} 
),
bounds As(
	select
		Q1_lat-1.5*(q3_lat - q1_lat) as lower_lat,
		q3_lat +1.5*(q3_lat -q1_lat ) as upper_lat,
		q1_lng -1.5*(q3_lng -q1_lng  ) as lower_lng,
		q3_lng +1.5*(q3_lng - q1_lng) as upper_lng
	from quartiles 
),
filtered AS(
	select 
	og.*
	from {{source("raw","olist_geolocation")}} as og
	cross join bounds  as b
	where 
	-- Öncelikle brezilya verisiyle çalıştığımız için brezilyayı kapsayacak kordinatları
	-- SOnrsında ise IQR ile aykırı değerleri filtreliyoruz çünü deduplicate yapacağız.
		og.geolocation_lat between -34 and 5
		and og.geolocation_lng between -74 and -34
		and og.geolocation_lat between b.lower_lat and b.upper_lat
		and og.geolocation_lng between  b.lower_lng and b.upper_lng
),
deduplicated AS(
	select 
		geolocation_zip_code_prefix,
		geolocation_city,
		geolocation_state,
		-- İki kere aykırı değerleri filtreledğimizden performans kaybı olmaması için AVG tercih edil
		AVG(geolocation_lat) as geolocation_lat ,
		AVG(geolocation_lng ) as geolocation_lng	
	from filtered
	group by
		geolocation_zip_code_prefix,
		geolocation_city,
		geolocation_state	
	),
	final AS(
		select 
			geolocation_zip_code_prefix ,
			TRIM(upper(geolocation_city)) as geolocation_city ,
			TRIM(upper(geolocation_state)) as geolocation_state,
			geolocation_lat ,
			geolocation_lng 
		from deduplicated 
	)

SELECT * FROM final
	



