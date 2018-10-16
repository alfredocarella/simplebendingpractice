from beambending.beam import graphics_output

with graphics_output() as (beam, x):
    beam.length(9)           # Beam length
    beam.fixed_support(2)    # x-coordinate of the fixed support
    beam.rolling_support(7)  # x-coordinate of the rolling support

    # SYNTAX A:
    # Add a point load (20kN pointing downward, at x=3m)
    beam.point_load(-20, 3)
    # Distributed load (20kN/m pointing downward, between x=0m and x=2m)
    beam.distributed_load(-20, (0, 2))
    # Distributed load (10kN/m pointing downward, between x=3m and x=9m)
    beam.distributed_load(-10, (3, 9))

    # SYNTAX B:
    # loads = [PointLoad(-20, 3),
    #          DistributedLoad(-20, (0, 2)),
    #          DistributedLoad(-10, (3, 9))]
    #
    # beam.add_loads(loads)

