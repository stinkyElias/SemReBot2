(define (domain warehouse)

(:requirements :strips :typing :adl :fluents :durative-actions);

(:types
    robot
    zone
    pallet
)

(:predicates
    (robot_available ?robot - robot)
    
    (robot_at ?robot - robot ?zone - zone)
    (pallet_at ?pallet - pallet ?zone - zone)

    (is_pallet ?pallet - pallet)
    
    (pallet_not_moved ?pallet - pallet)

    (is_unload_zone ?zone - zone)
    (is_shelf_zone ?zone - zone)
);

(:durative-action navigate
    :parameters (?robot - robot ?from_zone - zone ?to_zone - zone)
    :duration (= ?duration 3)
    :condition (and 
        (at start (and
            (robot_at ?robot ?from_zone)
            (robot_available ?robot)
        ))
    )
    :effect (and 
        (at start (and
            (not(robot_at ?robot ?from_zone))
            (not(robot_available ?robot))
        ))
        (at end (and 
            (robot_at ?robot ?to_zone)
            (robot_available ?robot)
        ))
    )
)

(:durative-action transport
    :parameters (?robot - robot ?pallet - pallet ?from_zone - zone ?to_zone - zone)
    :duration (= ?duration 5)
    :condition (and 
        (at start (and
            (robot_at ?robot ?from_zone)
            (robot_available ?robot)

            (pallet_at ?pallet ?from_zone)
            (pallet_not_moved ?pallet)
        ))
        (over all (and
            (is_unload_zone ?from_zone)
            (is_shelf_zone ?to_zone)
        ))
    )
    :effect (and 
        (at start (and
            (not(robot_at ?robot ?from_zone))
            (not(pallet_at ?pallet ?from_zone))
            (not(robot_available ?robot))
            (not(pallet_not_moved ?pallet))
        ))
        (at end (and 
            (robot_at ?robot ?to_zone)
            (pallet_at ?pallet ?to_zone)
            (robot_available ?robot)
        ))
    )
)

)