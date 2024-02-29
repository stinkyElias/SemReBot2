(define (domain warehouse)

(:requirements :strips :typing :adl :fluents :durative-actions)

(:types
    robot
    zone
)

(:predicates
    (battery_full ?r - robot)
    (robot_available ?r - robot)
    
    (robot_at ?r - robot ?z - zone)

    (is_reol_zone ?z - zone)
    (is_charging_zone ?z - zone)
    (is_unload_zone ?z - zone)
)

(:durative-action navigate
    :parameters (?r - robot ?zone_1 ?zone_2 - zone)
    :duration (= ?duration 5)
    :condition (and 
        (at start (robot_at ?r ?zone_1))
        (at start (robot_available ?r))
        (at start (battery_full ?r))
        )
    :effect (and 
        (at start (not(robot_at ?r ?zone_1)))
        (at end (robot_at ?r ?zone_2))
        (at start (not(robot_available ?r)))
        (at end (robot_available ?r))
    )
)

)