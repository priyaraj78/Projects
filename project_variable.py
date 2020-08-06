length_of_highway = 7000
midpoint_of_highway = length_of_highway/2
entrance_threshold = 20
shopping_centre_radius = 900
average_shopping_time = 1800
deviation_in_shopping_time = 200
# simulation_time = 60 * 60
# probability_of_movement_towards_shopping_centre = 0.25
simulation_time_step = 1
distance_between_basestation_and_highway = 1000
x_coordinate_of_basestation = 3500
y_coordinate_of_basestation = 1000


height_of_base_station = 45
EIRP_power_of_macro_cell = 57
EIRP_power_of_small_cell = 54
number_of_traffic_channel_in_macro_cell = 35
number_of_traffic_channel_in_small_cell = 35
frequency_of_macro_cell = 800
frequency_of_small_cell = 1900

total_number_of_user = 1000
number_of_user_in_shopping_centre = 500
number_of_user_on_highway = 500

probability_of_placing_new_user_on_highway = 0.5

mobile_height = 1.7
rsl_threshold = -102
preference_threshold = -80
handoff_margin = 3
call_rate = 1/3600
probability_of_making_call = call_rate * simulation_time_step
average_call_duration = 180
speed_of_user = 33
distance_travelled_in_one_sec = speed_of_user/simulation_time_step


user_data_in_shopping_centre = {}
user_data_on_highway = {}
user_who_are_on_call = []
user_who_are_not_on_call = []
shadowing_list = []
fading = 0
number_of_call_attempt_for_small_cell = 0
number_of_call_attempt_for_macro_cell = 0
number_of_complete_call_for_small_cell = 0
number_of_complete_call_for_macro_cell = 0
number_of_dropped_call_for_small_cell = 0
number_of_dropped_call_for_macro_cell = 0
call_block_counter_for_capacity_in_small_cell = 0
call_block_counter_for_capacity_in_macro_cell = 0
number_of_successful_call_connection_to_small_cell = 0
number_of_successful_call_connection_to_macro_cell = 0
call_block_counter_for_power = 0
handoff_attempt_from_small_to_macro = 0
handoff_attempt_from_macro_to_small = 0
failed_handoff_from_small_to_macro = 0
failed_handoff_from_macro_to_small = 0
successful_handoff_from_small_to_macro = 0
successful_handoff_from_macro_to_small = 0
