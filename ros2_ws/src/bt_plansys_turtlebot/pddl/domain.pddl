(define (domain warehouse)

(:requirements :strips :typing :adl :fluents :durative-actions)

(:types
    robot
    zone
    pallet
)

(:predicates
    (battery_full ?r - robot)
    (robot_available ?r - robot) ; if robot is NOT holding a pallet
    
    (robot_at ?r - robot ?z - zone)
    (pallet_at ?p - pallet ?z - zone)

    (is_reol_zone ?z - zone)
    (is_charging_zone ?z - zone)
    (is_unload_zone ?z - zone)

    (is_pallet ?p - pallet)
    
    (pallet_not_moved ?p - pallet)
)

(:durative-action navigate
    :parameters (?robot - robot ?from_zone ?to_zone - zone)
    :duration (= ?duration 5)
    :condition (and 
        (at start (and
            (robot_at ?robot ?from_zone)
            (robot_available ?robot)
        ))
    )
    :effect (and 
        (at start (not(robot_at ?robot ?from_zone)))
        (at end (robot_at ?robot ?to_zone))

        (at start (not(robot_available ?robot)))
        (at end (robot_available ?robot))
    )
)

(:durative-action transport
    :parameters (?robot - robot ?pallet - pallet ?from_zone ?to_zone - zone)
    :duration (= ?duration 5)
    :condition (and 
        (at start (and
            (robot_at ?robot ?from_zone)
            (pallet_at ?pallet ?from_zone)
            (pallet_not_moved ?pallet)
            (robot_available ?robot)
        ))
        
        (over all (and
            ; (battery_full ?robot)
            (is_unload_zone ?from_zone)
            (is_reol_zone ?to_zone)
            (is_pallet ?pallet)
        )) 
    )
    :effect (and 
        (at start (and
            (not(robot_at ?robot ?from_zone))
            (not(pallet_at ?pallet ?from_zone))
            (pallet_not_moved ?pallet)
            (not(robot_available ?robot))
        ))
        (at end (and 
            (robot_at ?robot ?to_zone)
            (pallet_at ?pallet ?to_zone)
            (not(pallet_not_moved ?pallet))
            (robot_available ?robot)

            ; (not(battery_full ?robot))
        ))
    )
)

(:durative-action recharge
    :parameters (?robot - robot ?zone - zone)
    :duration (= ?duration 5)
    :condition (and 
        (at start (is_charging_zone ?zone))
        (over all (robot_at ?robot ?zone)) 
        (at start (robot_available ?robot))
    )
    :effect (and 
        (at end (battery_full ?robot)) 
        (at end (robot_available ?robot))
    )
)

)