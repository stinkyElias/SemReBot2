(define (domain warehouse)

<<<<<<< HEAD
    (:requirements :strips :typing :adl :fluents :durative-actions)

    (:types
        robot
        zone
        pallet
    )

    (:predicates
        (robot_available ?robot - robot)
        
        (robot_at ?robot - robot ?zone - zone)
        (pallet_at ?pallet - pallet ?zone - zone)
        
        (pallet_not_moved ?pallet - pallet)

        (is_unload_zone ?zone - zone)
        (is_shelf_zone ?zone - zone)
        (is_recharge_zone ?zone - zone)
    )

    (:functions
        (distance ?from - zone ?to - zone)
        (speed ?robot - robot)
        (battery_level ?robot - robot) ; % of battery
    )

    (:durative-action navigate
        :parameters (?robot - robot ?from_zone - zone ?to_zone - zone)
        :duration (= ?duration (/ (distance ?from_zone ?to_zone) (speed ?robot)))
        :condition (and 
            (at start (and
                (robot_at ?robot ?from_zone)
                (robot_available ?robot)

                (> (battery_level ?robot) 20)
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

                (decrease (battery_level ?robot) 10)
            ))
        )
    )

    (:durative-action transport
        :parameters (?robot - robot ?pallet - pallet ?from_zone - zone ?to_zone - zone)
        :duration (= ?duration (/ (distance ?from_zone ?to_zone) (speed ?robot)))
        :condition (and 
            (at start (and
                (robot_at ?robot ?from_zone)
                (robot_available ?robot)

                (pallet_at ?pallet ?from_zone)
                (pallet_not_moved ?pallet)

                (> (battery_level ?robot) 30)
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

                (decrease (battery_level ?robot) 20)
            ))
            (at end (and 
                (robot_at ?robot ?to_zone)
                (pallet_at ?pallet ?to_zone)
                (robot_available ?robot)
            ))
        )
    )

    (:durative-action recharge
        :parameters (?robot - robot ?zone - zone)
        :duration (= ?duration 10)
        :condition (and 
            (at start (and
                (is_recharge_zone ?zone)
                (robot_available ?robot)
                (robot_at ?robot ?zone)
            )))
            
        :effect (and 
            (at start (and 
                (not(robot_available ?robot))
                (assign (battery_level ?robot) 100)
            ))
            (at end (robot_available ?robot))
        )
    )
=======
(:requirements :strips :typing :adl :fluents :durative-actions)

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
)

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

>>>>>>> main
)