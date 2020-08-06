import numpy
from project_variable import *
from rsl_cal import *


#Helper function to place user at random position in shopping centre
def get_distribution_inside_shopping_centre():
	global average_shopping_time
	global deviation_in_shopping_time
	angle = numpy.random.random() * 2 * numpy.pi
	radius = shopping_centre_radius * numpy.sqrt(numpy.random.random())
#Getting the value of x coordinate and adding circle centre's x coordinate
	x = radius * numpy.cos(angle) + x_coordinate_of_basestation
#Getting the value of y coordinate and adding circle centre's y coordinate
	y = radius * numpy.sin(angle) + y_coordinate_of_basestation
	time_left = numpy.random.normal(average_shopping_time,deviation_in_shopping_time)
	temp_dict = {}
	temp_dict['x'] = x
	temp_dict['y'] = y
	temp_dict['remaining_time'] = time_left
	temp_dict['angle'] = angle
	temp_dict['distance_from_basestation'] = radius
	temp_dict['came_from'] = 'S'
	temp_dict['is_on_call'] = 0
	temp_dict['call_time'] = 0
	temp_dict['connected_to'] = ''
	temp_dict['rsl_for_small_cell'] = 0
	temp_dict['rsl_for_macro_cell'] = 0
	return temp_dict

#Helper function to place user at random position on highway
def get_distribution_on_highway():
	global length_of_highway
	position = numpy.random.randint(low=0,high=length_of_highway)
	temp_dict = {}
	temp_dict['position_on_highway'] = position
	temp_dict['distance_from_basestation'] = numpy.hypot((midpoint_of_highway - position), distance_between_basestation_and_highway)
	if position<midpoint_of_highway:
		temp_dict['movement_direction'] = 'E'
	else:
		temp_dict['movement_direction'] = 'W'
	temp_dict['came_from'] = 'H'
	temp_dict['is_on_call'] = 0
	temp_dict['call_time'] = 0
	temp_dict['connected_to'] = ''
	temp_dict['rsl_for_macro_cell'] = 0
	temp_dict['rsl_for_small_cell'] = 0
	return temp_dict


#Function will create the mentioned number of users in shopping centre
def create_user_in_shopping_centre():
	global user_data_in_shopping_centre
	i = 0
	temp_dict = {}
#Loop to generate random user and distribute in shopping centre
	while i < number_of_user_in_shopping_centre:
		temp_dict = get_distribution_inside_shopping_centre()
		username = 'user' + str(i)
		user_data_in_shopping_centre[username] = temp_dict
		user_who_are_not_on_call.append(username)
		i = i + 1

#Function will return the dictionary of user data which are present in shopping centre
def get_user_present_in_shopping_centre():
	return user_data_in_shopping_centre

#Function will create the mentioned number of users on highway
def create_user_on_highway():
	global user_data_on_highway
	i = total_number_of_user - number_of_user_in_shopping_centre
	temp_dict = {}
#loop to generate random user and distribute on highway
	while i < total_number_of_user:
		temp_dict = get_distribution_on_highway()
		username = 'user' + str(i)
		user_data_on_highway[username] = temp_dict
		user_who_are_not_on_call.append(username)
		i = i + 1

#Function will return the dictionary of user data which are present on highway
def get_user_present_on_highway():
	return user_data_on_highway

#Function will update the user's shopping time and will remove a user from shopping centre and put it on highway if the shopping time 
#is less than 0
def update_user_data_in_shopping_centre():
	user_who_wants_to_move = [] 
#loop to decrease shopping time of user and move them to highway with equal probability of placement
	for user in user_data_in_shopping_centre.keys():
		if user_data_in_shopping_centre[user]['remaining_time'] <= 1:
#change users position on highway
			user_data_on_highway[user] = {}
#Placing the user on highway with equal probability
			placement_direction = numpy.random.choice([1,0],p=[probability_of_placing_new_user_on_highway,(1 - probability_of_placing_new_user_on_highway)])
			if placement_direction == 1:
				position = midpoint_of_highway + entrance_threshold
				user_data_on_highway[user]['position_on_highway'] = position
				user_data_on_highway[user]['movement_direction'] = 'E'
			else:
				position = midpoint_of_highway - entrance_threshold
				user_data_on_highway[user]['position_on_highway'] = position
				user_data_on_highway[user]['movement_direction'] = 'W'
			user_data_on_highway[user]['came_from'] = 'S'
			user_data_on_highway[user]['distance_from_basestation'] = numpy.hypot((position - midpoint_of_highway), distance_between_basestation_and_highway)
			user_data_on_highway[user]['is_on_call'] = user_data_in_shopping_centre[user]['is_on_call']
			user_data_on_highway[user]['call_time'] = user_data_in_shopping_centre[user]['call_time']
			user_data_on_highway[user]['connected_to'] = user_data_in_shopping_centre[user]['connected_to']
#Removing user from shopping centre
			user_who_wants_to_move.append(user)
#Updating user's shopping time
		else:
			user_data_in_shopping_centre[user]['remaining_time'] = user_data_in_shopping_centre[user]['remaining_time'] - 1

	for user in user_who_wants_to_move:
		user_data_in_shopping_centre.pop(user)

# Function will update the user's position on highway, take decision about moving the user to shopping centre and replace the user if
# it is moved out of the highway
def update_user_data_on_highway(probability_of_movement_towards_shopping_centre):
	global number_of_complete_call_for_small_cell
	global number_of_traffic_channel_in_small_cell
	global number_of_complete_call_for_macro_cell
	global number_of_traffic_channel_in_macro_cell
	user_who_wants_to_move = []
#loop to move user on highway towards shopping centre entrance and take decision whether to give entry to them or not and also
#removing the user from highway when they go beyond the highway and updating new details for that user 
	for user in user_data_on_highway.keys():
#Chekcing whether the user is present in enterance threshold range
		if user_data_on_highway[user]['came_from'] == 'H' and numpy.absolute(midpoint_of_highway - user_data_on_highway[user]['position_on_highway'] <= entrance_threshold):
			choice = numpy.random.choice([1,0],p=[probability_of_movement_towards_shopping_centre, (1 - probability_of_movement_towards_shopping_centre)])
#If the user is selected based on the probability then moving the user to shopping centre and removing it from highway
			if choice == 1:
				user_data_in_shopping_centre[user] = {}
				user_data_in_shopping_centre[user] = get_distribution_inside_shopping_centre()
				user_data_in_shopping_centre[user]['is_on_call'] = user_data_on_highway[user]['is_on_call']
				user_data_in_shopping_centre[user]['call_time'] = user_data_on_highway[user]['call_time']
				user_data_in_shopping_centre[user]['connected_to'] = user_data_on_highway[user]['connected_to']
#If user is on call then before placing it in shopping centre I am calculating rsl values
				if user_data_in_shopping_centre[user]['is_on_call'] == 1:
					user_data_in_shopping_centre[user]['rsl_for_small_cell'] = get_rsl_for_small_cell(user_data_in_shopping_centre[user]['distance_from_basestation'])
					user_data_in_shopping_centre[user]['rsl_for_macro_cell'] = get_rsl_for_macro_cell_when_user_is_in_shopping_centre(user_data_in_shopping_centre[user]['distance_from_basestation'])
				user_who_wants_to_move.append(user)
			else:
#Updating user position based on its direction of movement
				if user_data_on_highway[user]['movement_direction'] == 'W':
					user_data_on_highway[user]['position_on_highway'] = user_data_on_highway[user]['position_on_highway'] - distance_travelled_in_one_sec
				if user_data_on_highway[user]['movement_direction'] == 'E':
					user_data_on_highway[user]['position_on_highway'] = user_data_on_highway[user]['position_on_highway'] + distance_travelled_in_one_sec
				user_data_on_highway[user]['distance_from_basestation'] = numpy.hypot((user_data_on_highway[user]['position_on_highway'] - midpoint_of_highway), distance_between_basestation_and_highway)
#Removing the user from highway when it goes beyond the highway and creating a new user and placing it randomly on highway
		elif user_data_on_highway[user]['position_on_highway'] < 0 or user_data_on_highway[user]['position_on_highway'] > length_of_highway:
#If user is on call then incrementing the complete call coung for corresponding cell to which user is connected and freeing up the 
#channel as well
			if user_data_on_highway[user]['is_on_call'] == 1:
				if user_data_on_highway[user]['connected_to'] == 'M':
					number_of_complete_call_for_macro_cell = number_of_complete_call_for_macro_cell + 1
					number_of_traffic_channel_in_macro_cell = number_of_traffic_channel_in_macro_cell + 1
				else:
					number_of_complete_call_for_small_cell = number_of_complete_call_for_small_cell + 1
					number_of_traffic_channel_in_small_cell = number_of_traffic_channel_in_small_cell + 1
#Setting other call parameters to default value
				user_data_on_highway[user]['is_on_call'] = 0
				user_data_on_highway[user]['call_time'] = 0
				user_data_on_highway[user]['connected_to'] = ''
				user_data_on_highway[user]['rsl_for_small_cell'] = 0
				user_data_on_highway[user]['rsl_for_macro_cell'] = 0
#Removing the user from list of active call users and adding it to inactive users list
				if user not in user_who_are_not_on_call:
					user_who_are_not_on_call.append(user)
				if user in user_who_are_on_call:
					user_who_are_on_call.remove(user)
#Getting new random position of user on higway
			user_data_on_highway[user] = get_distribution_on_highway()
#Updating user position based on its direction of movement
		elif user_data_on_highway[user]['movement_direction'] == 'W':
			user_data_on_highway[user]['position_on_highway'] = user_data_on_highway[user]['position_on_highway'] - distance_travelled_in_one_sec		
			user_data_on_highway[user]['distance_from_basestation'] = numpy.hypot((user_data_on_highway[user]['position_on_highway'] - midpoint_of_highway), distance_between_basestation_and_highway)
		elif user_data_on_highway[user]['movement_direction'] == 'E':
			user_data_on_highway[user]['position_on_highway'] = user_data_on_highway[user]['position_on_highway'] + distance_travelled_in_one_sec
			user_data_on_highway[user]['distance_from_basestation'] = numpy.hypot((user_data_on_highway[user]['position_on_highway'] - midpoint_of_highway), distance_between_basestation_and_highway)
		user_data_on_highway[user]['came_from'] = 'H'
#Removing the user from highway who are moved to shopping centre
	for user in user_who_wants_to_move:
		user_data_on_highway.pop(user)


#Function to connect new call 
def connect_new_call(user_who_want_to_make_new_call):
	global number_of_call_attempt_for_small_cell
	global number_of_dropped_call_for_macro_cell
	global call_block_counter_for_power
	global call_block_counter_for_capacity_in_macro_cell
	global fading
	global number_of_call_attempt_for_macro_cell
	global number_of_dropped_call_for_small_cell
	global call_block_counter_for_capacity_in_small_cell
	global user_who_are_on_call
	global user_who_are_not_on_call
	global number_of_traffic_channel_in_small_cell
	global number_of_traffic_channel_in_macro_cell
	global number_of_successful_call_connection_to_small_cell
	global number_of_successful_call_connection_to_macro_cell
#For every user in the user's list of who wants to make new call
	for user in user_who_want_to_make_new_call:
#Finding rsl value and setting the value in dictionary
		if user in user_data_in_shopping_centre:
			rsl_for_macro_cell = get_rsl_for_macro_cell_when_user_is_in_shopping_centre(user_data_in_shopping_centre[user]['distance_from_basestation'])
			rsl_for_small_cell = get_rsl_for_small_cell(user_data_in_shopping_centre[user]['distance_from_basestation'])
			user_data_in_shopping_centre[user]['rsl_for_small_cell'] = rsl_for_small_cell
			user_data_in_shopping_centre[user]['rsl_for_macro_cell'] = rsl_for_macro_cell
		else:
			rsl_for_macro_cell = get_rsl_for_macro_cell(user_data_on_highway[user]['distance_from_basestation'], user_data_on_highway[user]['position_on_highway'])
			rsl_for_small_cell = get_rsl_for_small_cell(user_data_on_highway[user]['distance_from_basestation'])
			user_data_on_highway[user]['rsl_for_small_cell'] = rsl_for_small_cell
			user_data_on_highway[user]['rsl_for_macro_cell'] = rsl_for_macro_cell
#If rsl for small cell is greater than preference threshold 
		if rsl_for_small_cell >= preference_threshold:
#Increment the number of call attempt for small cell
			number_of_call_attempt_for_small_cell = number_of_call_attempt_for_small_cell + 1
#If channel is available in small cell then connecting users call to small cell and decrementing available channel count and incrementing
#successful call connection count for small cell
			if number_of_traffic_channel_in_small_cell > 0:
				number_of_traffic_channel_in_small_cell = number_of_traffic_channel_in_small_cell - 1
				number_of_successful_call_connection_to_small_cell = number_of_successful_call_connection_to_small_cell + 1
#Based on user's position updating the call parameters
				if user in user_data_on_highway:
					user_data_on_highway[user]['is_on_call'] = 1
					user_data_on_highway[user]['call_time'] = numpy.random.normal(average_call_duration)
					user_data_on_highway[user]['connected_to'] = 'S'
				else:
					user_data_in_shopping_centre[user]['is_on_call'] = 1
					user_data_in_shopping_centre[user]['call_time'] = numpy.random.normal(average_call_duration)
					user_data_in_shopping_centre[user]['connected_to'] = 'S'
#added user to list of users who are on call
				user_who_are_on_call.append(user)
#removed user from list of users who are not on call
				user_who_are_not_on_call.remove(user)				
#If no channel is available then following code will execute
			else:
#incrementing call block counter for small cell
				call_block_counter_for_capacity_in_small_cell = call_block_counter_for_capacity_in_small_cell + 1			
#If rsl for macro cell is greater then rsl threshold
				if rsl_for_macro_cell >= rsl_threshold:
#Incrementing call attempt for macro cell
					number_of_call_attempt_for_macro_cell = number_of_call_attempt_for_macro_cell + 1
#If channel is free in macro cell then connecting user to macro cell
					if number_of_traffic_channel_in_macro_cell > 0:
						number_of_traffic_channel_in_macro_cell = number_of_traffic_channel_in_macro_cell - 1
						number_of_successful_call_connection_to_macro_cell = number_of_successful_call_connection_to_macro_cell + 1
#Updating call parameters based on user's position
						if user in user_data_on_highway:
							user_data_on_highway[user]['is_on_call'] = 1
							user_data_on_highway[user]['call_time'] = numpy.random.normal(average_call_duration)
							user_data_on_highway[user]['connected_to'] = 'M'
						else:
							user_data_in_shopping_centre[user]['is_on_call'] = 1
							user_data_in_shopping_centre[user]['call_time'] = numpy.random.normal(average_call_duration)
							user_data_in_shopping_centre[user]['connected_to'] = 'M'						
#added user to list of users who are on call
						user_who_are_on_call.append(user)
#removed user from list of users who are not on call
						user_who_are_not_on_call.remove(user)
#If macro cell does not have channel available then incrementing a drop call count for small cell
					else:
						number_of_dropped_call_for_small_cell = number_of_dropped_call_for_small_cell + 1
#If macro cell does not have sufficient power then incrementing a drop call count for small cell
				else:
					number_of_dropped_call_for_small_cell = number_of_dropped_call_for_small_cell + 1


#If the above conditions failed then this will be checked
		elif rsl_for_small_cell >= rsl_for_macro_cell and rsl_for_small_cell >= rsl_threshold:
#Incrementing call attempt for small cell
			number_of_call_attempt_for_small_cell = number_of_call_attempt_for_small_cell + 1
#If channel is available in small cell then connecting users call to small cell and decrementing available channel count and incrementing
#successful call connection count for small cell
			if number_of_traffic_channel_in_small_cell > 0:
				number_of_traffic_channel_in_small_cell = number_of_traffic_channel_in_small_cell - 1
				number_of_successful_call_connection_to_small_cell = number_of_successful_call_connection_to_small_cell + 1
#Based on user's position updating the call parameters
				if user in user_data_on_highway:
					user_data_on_highway[user]['is_on_call'] = 1
					user_data_on_highway[user]['call_time'] = numpy.random.normal(average_call_duration)
					user_data_on_highway[user]['connected_to'] = 'S'
				else:
					user_data_in_shopping_centre[user]['is_on_call'] = 1
					user_data_in_shopping_centre[user]['call_time'] = numpy.random.normal(average_call_duration)
					user_data_in_shopping_centre[user]['connected_to'] = 'S'
#added user to list of users who are on call
				user_who_are_on_call.append(user)
#removed user from list of users who are not on call
				user_who_are_not_on_call.remove(user)
#If no channel is available in small cell then following code will execute
			else:
#incrementing call block counter for small cell
				call_block_counter_for_capacity_in_small_cell = call_block_counter_for_capacity_in_small_cell + 1			
#If rsl for macro cell is greater then rsl threshold
				if rsl_for_macro_cell >= rsl_threshold:
#Incrementing call attempt for macro cell
					number_of_call_attempt_for_macro_cell = number_of_call_attempt_for_macro_cell + 1
#If channel is free in macro cell then connecting user to macro cell
					if number_of_traffic_channel_in_macro_cell > 0:
						number_of_traffic_channel_in_macro_cell = number_of_traffic_channel_in_macro_cell - 1
						number_of_successful_call_connection_to_macro_cell = number_of_successful_call_connection_to_macro_cell + 1
#Updating call parameters based on user's position
						if user in user_data_on_highway:
							user_data_on_highway[user]['is_on_call'] = 1
							user_data_on_highway[user]['call_time'] = numpy.random.normal(average_call_duration)
							user_data_on_highway[user]['connected_to'] = 'M'
						else:
							user_data_in_shopping_centre[user]['is_on_call'] = 1
							user_data_in_shopping_centre[user]['call_time'] = numpy.random.normal(average_call_duration)
							user_data_in_shopping_centre[user]['connected_to'] = 'M'
#added user to list of users who are on call
						user_who_are_on_call.append(user)
#removed user from list of users who are not on call
						user_who_are_not_on_call.remove(user)
#If macro cell does not have channel available then incrementing a drop call count for small cell
					else:
						number_of_dropped_call_for_small_cell = number_of_dropped_call_for_small_cell + 1
#If macro cell does not have sufficient power available then incrementing a drop call count for small cell
				else:
					number_of_dropped_call_for_small_cell = number_of_dropped_call_for_small_cell + 1



#If above conditions fail then this will execute
		elif rsl_for_small_cell < preference_threshold and rsl_for_macro_cell >= rsl_for_small_cell and rsl_for_macro_cell >= rsl_threshold:
#Not mention in question but unable to verify the output without incrementing it
#Incrementing call attempt for macro cell
			number_of_call_attempt_for_macro_cell = number_of_call_attempt_for_macro_cell + 1 
#If channel is free in macro cell then connecting user to macro cell
			if number_of_traffic_channel_in_macro_cell > 0:
				number_of_traffic_channel_in_macro_cell = number_of_traffic_channel_in_macro_cell - 1
				number_of_successful_call_connection_to_macro_cell = number_of_successful_call_connection_to_macro_cell + 1
#Updating call parameters based on user's position
				if user in user_data_on_highway:
					user_data_on_highway[user]['is_on_call'] = 1
					user_data_on_highway[user]['call_time'] = numpy.random.normal(average_call_duration)
					user_data_on_highway[user]['connected_to'] = 'M'
				else:
					user_data_in_shopping_centre[user]['is_on_call'] = 1
					user_data_in_shopping_centre[user]['call_time'] = numpy.random.normal(average_call_duration)
					user_data_in_shopping_centre[user]['connected_to'] = 'M'
#added user to list of users who are on call
				user_who_are_on_call.append(user)
#removed user from list of users who are not on call
				user_who_are_not_on_call.remove(user)
#If channel is not available in macro cell 
			else:
#Increment call block counter for macro cell
				call_block_counter_for_capacity_in_macro_cell = call_block_counter_for_capacity_in_macro_cell + 1
#If rsl small cell is greater than rsl threshold
				if rsl_for_small_cell >= rsl_threshold:
#Incrementing call attempt for small cell 
					number_of_call_attempt_for_small_cell = number_of_call_attempt_for_small_cell + 1
#If small has channel avaialble then connecting to small cell
					if number_of_traffic_channel_in_small_cell > 0:
#Decrementing the free channel count and incrementing successful call connection count for small cell
						number_of_traffic_channel_in_small_cell = number_of_traffic_channel_in_small_cell - 1
						number_of_successful_call_connection_to_small_cell = number_of_successful_call_connection_to_small_cell + 1
#Updating user call parameter based on its position
						if user in user_data_on_highway:
							user_data_on_highway[user]['is_on_call'] = 1
							user_data_on_highway[user]['call_time'] = numpy.random.normal(average_call_duration)
							user_data_on_highway[user]['connected_to'] = 'S'
						else:
							user_data_in_shopping_centre[user]['is_on_call'] = 1
							user_data_in_shopping_centre[user]['call_time'] = numpy.random.normal(average_call_duration)
							user_data_in_shopping_centre[user]['connected_to'] = 'S'
#Adding user to active user's call list
						user_who_are_on_call.append(user)
#Removing user from inactive users call list
						user_who_are_not_on_call.remove(user)
#If no channel available in small cell then incrementing drop call count for macro cell
					else:
						number_of_dropped_call_for_macro_cell = number_of_dropped_call_for_macro_cell + 1
#If small cell rsl is less than rsl threshold then incrementing call drop count for macro cell
				else:
					number_of_dropped_call_for_macro_cell = number_of_dropped_call_for_macro_cell + 1
#If above all conditions fail then this will execute
		else:
#Incrementing drop call count based on users position and call block counter for power
			call_block_counter_for_power
			if user in user_data_on_highway:
				number_of_dropped_call_for_macro_cell = number_of_dropped_call_for_macro_cell + 1
			else:
				number_of_dropped_call_for_small_cell = number_of_dropped_call_for_small_cell + 1

def check_active_call():
	global number_of_complete_call_for_macro_cell
	global number_of_traffic_channel_in_macro_cell
	global number_of_complete_call_for_small_cell
	global number_of_traffic_channel_in_small_cell
	global handoff_attempt_from_small_to_macro
	global successful_handoff_from_small_to_macro
	global failed_handoff_from_small_to_macro
	global call_block_counter_for_capacity_in_macro_cell
	global handoff_attempt_from_macro_to_small
	global successful_handoff_from_macro_to_small
	global failed_handoff_from_macro_to_small
	global call_block_counter_for_capacity_in_small_cell
	global number_of_dropped_call_for_small_cell
	global number_of_dropped_call_for_macro_cell
	global user_who_are_on_call
	global user_who_are_not_on_call
	global call_block_counter_for_power_for_small_cell
	global call_block_counter_for_power_for_macro_cell
	cell_type = ''
#For every user who is on call loop will execute
	for user in user_who_are_on_call:
#If user is in shopping centre
		if user in user_data_in_shopping_centre:
#Getting its cell type to which it is connected
			cell_type = user_data_in_shopping_centre[user]['connected_to']
#If the users call time is ended
			if user_data_in_shopping_centre[user]['call_time'] <= 0:
#Incrementing free channel count and call completion count
				if user_data_in_shopping_centre[user]['connected_to'] == 'M':
					number_of_complete_call_for_macro_cell = number_of_complete_call_for_macro_cell + 1
					number_of_traffic_channel_in_macro_cell = number_of_traffic_channel_in_macro_cell + 1
				else:
					number_of_complete_call_for_small_cell = number_of_complete_call_for_small_cell + 1
					number_of_traffic_channel_in_small_cell = number_of_traffic_channel_in_small_cell + 1
#removing from active user call list
				user_who_are_on_call.remove(user)
#adding user to inactive user call list
				user_who_are_not_on_call.append(user)
#Updating call parameters
				user_data_in_shopping_centre[user]['is_on_call'] = 0
				user_data_in_shopping_centre[user]['call_time'] = 0
				user_data_in_shopping_centre[user]['connected_to'] = ''
				user_data_in_shopping_centre[user]['rsl_for_small_cell'] = 0
				user_data_in_shopping_centre[user]['rsl_for_macro_cell'] = 0
				continue
#otherwise decreasing call time for the user
			else:
				user_data_in_shopping_centre[user]['call_time'] = user_data_in_shopping_centre[user]['call_time'] - 1
#If user is in highway
		else:
#Getting cell type to which user is connected
			cell_type = user_data_on_highway[user]['connected_to']
#If the call time is over 
			if user_data_on_highway[user]['call_time'] <= 0:
#Incrementing free channel count and call completion count
				if user_data_on_highway[user]['connected_to'] == 'M':
					number_of_complete_call_for_macro_cell = number_of_complete_call_for_macro_cell + 1
					number_of_traffic_channel_in_macro_cell = number_of_traffic_channel_in_macro_cell + 1
				else:
					number_of_complete_call_for_small_cell = number_of_complete_call_for_small_cell + 1
					number_of_traffic_channel_in_small_cell = number_of_traffic_channel_in_small_cell + 1
#removing user form active call list
				user_who_are_on_call.remove(user)
#add user to inactive call list
				user_who_are_not_on_call.append(user)
#Updating user call parameter
				user_data_on_highway[user]['is_on_call'] = 0
				user_data_on_highway[user]['call_time'] = 0
				user_data_on_highway[user]['connected_to'] = ''
				user_data_on_highway[user]['rsl_for_small_cell'] = 0
				user_data_on_highway[user]['rsl_for_macro_cell'] = 0
				continue
#Otherwise decrementing user call time
			else:
				user_data_on_highway[user]['call_time'] = user_data_on_highway[user]['call_time'] - 1
#Getting rsl value for both the cell and setting in dictionary
		if user in user_data_in_shopping_centre:
			rsl_for_macro_cell = user_data_in_shopping_centre[user]['rsl_for_macro_cell']
			rsl_for_small_cell = user_data_in_shopping_centre[user]['rsl_for_small_cell']
		else:
			rsl_for_macro_cell = get_rsl_for_macro_cell(user_data_on_highway[user]['distance_from_basestation'], user_data_on_highway[user]['position_on_highway'])
			rsl_for_small_cell = get_rsl_for_small_cell(user_data_on_highway[user]['distance_from_basestation'])
			user_data_on_highway[user]['rsl_for_small_cell'] = rsl_for_small_cell
			user_data_on_highway[user]['rsl_for_macro_cell'] = rsl_for_macro_cell
#If the user is connected to small cell and checking for handoff
		if cell_type == 'S' and rsl_for_small_cell < preference_threshold and rsl_for_macro_cell >= rsl_for_small_cell + handoff_margin:
#Incrementing handoff attempt for small to macro
			handoff_attempt_from_small_to_macro = handoff_attempt_from_small_to_macro + 1
#If macro cell has free channel
			if number_of_traffic_channel_in_macro_cell > 0:
#Freeing up small cell channel and occupying macro cell channel
				number_of_traffic_channel_in_small_cell = number_of_traffic_channel_in_small_cell + 1
				number_of_traffic_channel_in_macro_cell = number_of_traffic_channel_in_macro_cell - 1
#Changing users call parameter
				if user in user_data_in_shopping_centre:
					user_data_in_shopping_centre[user]['connected_to'] = 'M'
				else:
					user_data_on_highway[user]['connected_to'] = 'M'
#incrementing successful handoff from small to macro
				successful_handoff_from_small_to_macro = successful_handoff_from_small_to_macro + 1
#otherwise incrementing failed handoff from small to macro and call block counter from macro cell
			else:
				failed_handoff_from_small_to_macro = failed_handoff_from_small_to_macro + 1
				call_block_counter_for_capacity_in_macro_cell = call_block_counter_for_capacity_in_macro_cell + 1
#If user is connected to macro and checking handoff condition
		elif cell_type == 'M' and (rsl_for_small_cell > preference_threshold or rsl_for_small_cell >= rsl_for_macro_cell + handoff_margin):
#incrementing handoff attempt from macro to small
			handoff_attempt_from_macro_to_small = handoff_attempt_from_macro_to_small + 1
#If small cell has free channel
			if number_of_traffic_channel_in_small_cell > 0:
#freeing up macro cell channel and occupying macro cell channel
				number_of_traffic_channel_in_small_cell = number_of_traffic_channel_in_small_cell - 1
				number_of_traffic_channel_in_macro_cell = number_of_traffic_channel_in_macro_cell + 1
#Changing users call parameter
				if user in user_data_in_shopping_centre:
					user_data_in_shopping_centre[user]['connected_to'] = 'S'
				else:
					user_data_on_highway[user]['connected_to'] = 'S'
#incrementing successful handoff count from macro to small
				successful_handoff_from_macro_to_small = successful_handoff_from_macro_to_small + 1
#otherwise incrementing failed handoff from macro to small and call block counter from small cell
			else:
				failed_handoff_from_macro_to_small = failed_handoff_from_macro_to_small + 1
				call_block_counter_for_capacity_in_small_cell = call_block_counter_for_capacity_in_small_cell + 1
#Checking if user is connected with small cell or macro cell
		elif cell_type == 'S':
#If rsl of small cell is less than preference threshold
			if rsl_for_small_cell < rsl_threshold:
#incrementing the drop call count for small cell and freeing up the channel for smal cell
				number_of_dropped_call_for_small_cell = number_of_dropped_call_for_small_cell + 1
				number_of_traffic_channel_in_small_cell = number_of_traffic_channel_in_small_cell + 1
#Updating user call parameter based on its position
				if user in user_data_in_shopping_centre:
					user_data_in_shopping_centre[user]['is_on_call'] = 0
					user_data_in_shopping_centre[user]['call_time'] = 0
					user_data_in_shopping_centre[user]['connected_to'] = ''
					user_data_in_shopping_centre[user]['rsl_for_small_cell'] = 0
					user_data_in_shopping_centre[user]['rsl_for_macro_cell'] = 0
				else:
					user_data_on_highway[user]['is_on_call'] = 0
					user_data_on_highway[user]['call_time'] = 0
					user_data_on_highway[user]['connected_to'] = ''
					user_data_on_highway[user]['rsl_for_small_cell'] = 0
					user_data_on_highway[user]['rsl_for_macro_cell'] = 0
#removing user from active users call list
				user_who_are_on_call.remove(user)
#adding user to inactive users call list
				user_who_are_not_on_call.append(user)
#otherwise this will execute
		elif cell_type == 'M':
#If rsl for macro cell is less than rsl threshold
			if rsl_for_macro_cell < rsl_threshold:
#incrementing drop call count for macro cell
				number_of_dropped_call_for_macro_cell = number_of_dropped_call_for_macro_cell + 1
#incrementing channel available count for macro cell
				number_of_traffic_channel_in_macro_cell = number_of_traffic_channel_in_macro_cell + 1
#Updating users call parameter based on its position
				if user in user_data_in_shopping_centre:
					user_data_in_shopping_centre[user]['is_on_call'] = 0
					user_data_in_shopping_centre[user]['call_time'] = 0
					user_data_in_shopping_centre[user]['connected_to'] = ''
					user_data_in_shopping_centre[user]['rsl_for_small_cell'] = 0
					user_data_in_shopping_centre[user]['rsl_for_macro_cell'] = 0
				else:
					user_data_on_highway[user]['is_on_call'] = 0
					user_data_on_highway[user]['call_time'] = 0
					user_data_on_highway[user]['connected_to'] = ''
					user_data_on_highway[user]['rsl_for_small_cell'] = 0
					user_data_on_highway[user]['rsl_for_macro_cell'] = 0
#removing user from active users call list
				user_who_are_on_call.remove(user)
#adding user to inactive users call list
				user_who_are_not_on_call.append(user)

#Function will start the simulation
def start_simulation(simulation_time, probability_of_movement_towards_shopping_centre):
	global user_who_are_on_call
	global user_who_are_not_on_call
	p = 0
#calculating shadowing value at every 5 meter
	calculate_shadowing_value_at_every_5_meter()
#starting simulation
	while p < simulation_time:
#Getting user's list who want to make new call based on probability
		user_who_want_to_make_new_call = []
		for user in user_who_are_not_on_call:
			choice = numpy.random.choice([1,0],p=[probability_of_making_call,(1-probability_of_making_call)])
			if choice == 1:
				user_who_want_to_make_new_call.append(user)
#Updating users paramter in shopping centre
		update_user_data_in_shopping_centre()
#Updating users parameter on highway
		update_user_data_on_highway(probability_of_movement_towards_shopping_centre)
#Checking active call for decrementing call time or handoff
		check_active_call()
#Connecting new call
		connect_new_call(user_who_want_to_make_new_call)
		p = p + 1
	print("number_of_call_attempt_for_small_cell %s"%number_of_call_attempt_for_small_cell)
	print("number_of_call_attempt_for_macro_cell %s"%number_of_call_attempt_for_macro_cell)
	print("number_of_complete_call_for_small_cell %s"%number_of_complete_call_for_small_cell)
	print("number_of_complete_call_for_macro_cell %s"%number_of_complete_call_for_macro_cell)
	print("number_of_dropped_call_for_small_cell %s"%number_of_dropped_call_for_small_cell)
	print("number_of_dropped_call_for_macro_cell %s"%number_of_dropped_call_for_macro_cell)
	print("call_block_counter_for_capacity_in_small_cell %s"%call_block_counter_for_capacity_in_small_cell)
	print("call_block_counter_for_capacity_in_macro_cell %s"%call_block_counter_for_capacity_in_macro_cell)
	print("number_of_successful_call_connection_to_small_cell %s"%number_of_successful_call_connection_to_small_cell)
	print("number_of_successful_call_connection_to_macro_cell %s"%number_of_successful_call_connection_to_macro_cell)
	print("call_block_counter_for_power %s"%call_block_counter_for_power)
	print("handoff_attempt_from_small_to_macro %s"%handoff_attempt_from_small_to_macro)
	print("handoff_attempt_from_macro_to_small %s"%handoff_attempt_from_macro_to_small)
	print("failed_handoff_from_small_to_macro %s"%failed_handoff_from_small_to_macro)
	print("failed_handoff_from_macro_to_small %s"%failed_handoff_from_macro_to_small)
	print("successful_handoff_from_small_to_macro %s"%successful_handoff_from_small_to_macro)
	print("successful_handoff_from_macro_to_small %s"%successful_handoff_from_macro_to_small)
	print("Number of available channel in small cell %s"%number_of_traffic_channel_in_small_cell)
	print("Number of available channel in macro cell %s"%number_of_traffic_channel_in_macro_cell)
	print("Number of user in shopping centre %s"%len(user_data_in_shopping_centre))
	print("Number of user on highway %s"%len(user_data_on_highway))

