
	

-- st_within AllZonesExtent with vacant land
SELECT vacant.*
INTO vacant_land_keepers
FROM public."AllZonesExtent" as AllZones, public."vacant_land" as vacant
WHERE st_within(vacant.geom, AllZones.geom);