from beambending.beam import graphics_output, PointLoad, DistributedLoad

with graphics_output() as (beam, x):
    beam.length(9)           # Beam length
    beam.fixed_support(2)    # x-coordinate of the fixed support
    beam.rolling_support(7)  # x-coordinate of the rolling support

    loads = [PointLoad(-20, 3),  # Point load (20kN downwards, at x=3m)
             DistributedLoad(-20, (0, 2)),  # 20kN/m downwards, for 0m <= x <= 2m
             DistributedLoad(-10, (3, 9))]  # 10kN/m downwards, for 3m <= x <= 9m
    
    beam.add_loads(loads)

