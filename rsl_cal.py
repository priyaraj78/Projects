from project_variable import *
import numpy

#Calculating propagation loss for macro cell using okamura hata
def get_propagation_loss_using_okamura_hata(distance_from_basestation):
	propagation_loss = 69.55 + 26.16 * numpy.log10(frequency_of_macro_cell) - 13.82 * numpy.log10(height_of_base_station) + (44.9 - 6.55 * numpy.log10(height_of_base_station)) * numpy.log10(distance_from_basestation/1000) - (1.1 * numpy.log10(frequency_of_macro_cell) - 0.7) * mobile_height + (1.56 * numpy.log10(frequency_of_macro_cell) - 0.8)
	return propagation_loss

#Calculating propagation loss for small cell using cost231 model
def get_propagation_loss_using_cost231_model(distance_from_basestation):
	propagation_loss = 46.3+33.9*numpy.log10(frequency_of_small_cell)-13.82*numpy.log10(height_of_base_station) + (44.9 - 6.55 *numpy.log10(height_of_base_station))*numpy.log10(distance_from_basestation/1000) - (1.1 * numpy.log10(frequency_of_small_cell) - 0.7) * mobile_height + (1.56 * numpy.log10(frequency_of_small_cell) - 0.8)
	return propagation_loss

#Calculating shadowing value at an interval of 5 metre on highway
def calculate_shadowing_value_at_every_5_meter():
	global shadowing_list
	shadowing_list = numpy.random.normal(0,2,1400)	

#Calculatning shadowing in small cell and returning a constant value as per problem statement
def get_shadowing_value_for_small_cell():
	shadowing = 2
	return shadowing

#Calculating fading value and return second deepest value
def get_fading():
	i = 0
	fading_list = []
	while i < 10:
		temp = numpy.random.rayleigh()
		fading_list.append(20*numpy.log10(temp))
		i = i + 1
	fading_list.sort()
	return fading_list[1]

#Calculating rsl for macro cell
def get_rsl_for_macro_cell(distance_from_basestation, position_on_highway):
	fading = get_fading()
	remainder = (position_on_highway % 5)
	if position_on_highway == 7000:
		quotient = shadowing_list[len(shadowing_list) - 1]
	else:
		if remainder <=2:
			quotient = int(position_on_highway/5)		
		else:
			quotient = int(position_on_highway/5) + 1
	propagation_loss = get_propagation_loss_using_okamura_hata(distance_from_basestation)
	rsl = EIRP_power_of_macro_cell - propagation_loss + shadowing_list[quotient] + fading
	return rsl

#Calculating rsl for small cell
def get_rsl_for_small_cell(distance_from_basestation):
	fading = get_fading()
	shadowing = get_shadowing_value_for_small_cell()
	propagation_loss = get_propagation_loss_using_cost231_model(distance_from_basestation)
	rsl = EIRP_power_of_small_cell - propagation_loss + shadowing + fading
	return rsl

def get_rsl_for_macro_cell_when_user_is_in_shopping_centre(distance_from_basestation):
	fading = get_fading()
	shadowing = get_shadowing_value_for_small_cell()
	propagation_loss = get_propagation_loss_using_okamura_hata(distance_from_basestation)
	rsl = EIRP_power_of_small_cell - propagation_loss + shadowing + fading
	return rsl