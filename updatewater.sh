#!/bin/bash

while read i
do echo $i
    psql -U canada -h 127.0.0.1 -c "update pd308_a_2011 p set the_geom_nowater = foo.nowater from (select p.pd_num, p.emrp_name, ST_Intersection(ST_Transform(p.the_geom, 4326), f.the_geom) nowater from pd308_a_2011 p left join fed308_a_nowater f on p.fed_num = cast(f.feduid as integer) where fed_num = $i) foo WHERE p.fed_num = '$i' AND p.pd_num = foo.pd_num AND p.emrp_name = foo.emrp_name "
done < kmlall.txt
