(define (domain warehouse)

(:requirements :strips :typing :adl :fluents :durative-actions)

(:types
    robot
    zone
    pallet
)

(:predicates
    (battery_full ?r - robot)
    (robot_available ?r - robot)
    
    (robot_at ?r - robot ?z - zone)
    (pallet_at ?p - pallet ?z - zone)

    (is_reol_zone ?z - zone)
    (is_charging_zone ?z - zone)
    (is_unload_zone ?z - zone)

    (pallet_not_moved ?p - pallet)

)


(:durative-action navigate
    :parameters (?r - robot ?zone_1 ?zone_2 - zone)
    :duration (= ?duration 5)
    :condition (and 
        (at start (robot_at ?r ?zone_1))
        (at start (robot_available ?r))
        )
    :effect (and 
        (at start (not(robot_at ?r ?zone_1)))
        (at end (robot_at ?r ?zone_2))
        (at start (not(robot_available ?r)))
        (at end (robot_available ?r))
    )
)

(:durative-action transport
    :parameters (?r - robot ?p - pallet ?zone_1 ?zone_2 - zone)
    :duration (= ?duration 5)
    :condition (and 
        (over all (battery_full ?r))
        (at start (robot_at ?r ?zone_1))
        (at start (pallet_at ?p ?zone_1))
        (at start (robot_available ?r))
        (at start (pallet_not_moved ?p))
        (at start (is_unload_zone ?zone_1))
        (at start (is_reol_zone ?zone_2))
    )
    :effect (and 
        (at start (not (robot_at ?r ?zone_1)))
        (at end (robot_at ?r ?zone_2))

        (at start (not (pallet_at ?p ?zone_1)))
        (at end (pallet_at ?p ?zone_2))

        (at start (not (robot_available ?r)))
        (at end (robot_available ?r))
        
        (at end (not (pallet_not_moved ?p)))
    )
)

(:durative-action recharge
    :parameters (?r - robot ?z - zone)
    :duration (= ?duration 5)
    :condition (and 
        (at start (is_charging_zone ?z))
        (over all (robot_at ?r ?z))
        (at start (robot_available ?r))
    )
    :effect (and 
        (at end(battery_full ?r))
        (at start (not (robot_available ?r)))
        (at end (robot_available ?r))
    )
)

)