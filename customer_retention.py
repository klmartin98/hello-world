from vsm_lib.customer_mods import customer_selector as cs
from vsm_lib import date_tools as dtls
from vsm_lib.class_lib.cohort_class import Cohort
import datetime as dt
import statistics as stats


def get_customer_retention(start_date, per_interval, num_periods, cohort=None):
	
	date1 = start_date
	date2 = dtls.month_end(date1)
	interval = per_interval
	num_iterations = num_periods

	iteration = 1
	
	temp = []	

	if cohort == None:

		while iteration <= num_iterations:
			prev_per_customers = cs.get_customers_with_spending(date1, date2)
			date1 = dtls.datetime_incrementer(date1,interval,1)

			date2 = dtls.month_end(date1)
			#print(date1, date2)
			
			next_per_customers = set(cs.get_customers_with_spending(date1, date2))
			new_customers = set(cs.get_users_by_fm(date1, date2))
			overlap = len(new_customers & next_per_customers)

			num_prev = len(prev_per_customers)
			num_new = len(next_per_customers)
			
			#print(num_prev,num_new, new_cust)
			
			retention = (num_new-overlap)/num_prev
			
			temp.append(retention)
			iteration+= 1
			#print(date1, date2)
	else:
		if cohort.type == 'avg_spending':
			temp_array = []
			prev_per_customers = cohort.get_customers(date1, date2)
			
			while iteration <= num_iterations:
				
				date1 = dtls.datetime_incrementer(date1,interval,1)
				date2 = dtls.month_end(date1)
				#print(date1, date2)
					
				next_per_customers = set(cohort.get_customers(date1, date2))
				new_customers = set(cs.get_users_by_fm(date1, date2))
				overlap = len(new_customers & next_per_customers)

				num_prev = len(prev_per_customers)
				num_new = len(next_per_customers)
				temp_array.append(num_prev)
				#print(num_prev,num_new, new_cust)
				
				retention = (num_new-overlap)/num_prev
				
				temp.append(retention)
				iteration+= 1
				prev_per_customers = next_per_customers
			temp_array.append(num_new)
		elif cohort.type == 'channel':
			pass
			

	mini_dict = {}
	mini_dict['retention_rate'] = round(stats.mean(temp),4)
	mini_dict['standard_deviation'] = round(stats.stdev(temp),4)
	mini_dict['avg_num_customers'] = round(stats.mean(temp_array),4)
	return mini_dict


cohort_array = []

cohort_A = Cohort('avg_spending', 1, 10)
cohort_array.append(cohort_A)

cohort_B = Cohort('avg_spending', 10.01, 25)
cohort_array.append(cohort_B)

cohort_C = Cohort('avg_spending', 25.01, 49)
cohort_array.append(cohort_C)

cohort_D = Cohort('avg_spending', 50, 99)
cohort_array.append(cohort_D)

cohort_E = Cohort('avg_spending', 100, 249)
cohort_array.append(cohort_E)

cohort_F = Cohort('avg_spending', 250, 499)
cohort_array.append(cohort_F)

cohort_G = Cohort('avg_spending', 500)
cohort_array.append(cohort_G)


for cohort in cohort_array:
	cohort.print_details()
	date1 = dt.datetime(2016,7,1,0,0,0)
	retention_rate = get_customer_retention(date1, 'month', 12, cohort)
	print(retention_rate)
	print('\n')
