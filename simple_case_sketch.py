from crunching import DistributedLoad, PointLoad, calculate_diagrams, plot_and_save

# User input
beam_span = (0, 9)
fixed_support = 2
rolling_support = 7

loads = [PointLoad(-20, 3),
         DistributedLoad(-20, (0, 2)),
         DistributedLoad("-10", (3, 9))]


# Calculate reaction forces at supports
my_plots = calculate_diagrams(beam_span, fixed_support, rolling_support, loads)


# Plotting
plot_and_save(*my_plots)

