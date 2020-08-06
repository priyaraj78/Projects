from project import *

create_user_in_shopping_centre()
create_user_on_highway()

simulation_time = int(input("Enter simulation time : ")) * 3600
probability_of_movement_towards_shopping_centre = float(input("Enter probability of moving user into shopping centre : "))
start_simulation(simulation_time, probability_of_movement_towards_shopping_centre)
