#!/usr/bin/python3

# Author: Jose Garcia
# Date: 10/20/2019

""" Coding challenge using Instacart dataset.
    
    This program takes the csv files from /input and performs basic statistics about
    the contents. It uses lists and dictionaries for fast indexing.

"""

import sys

def csv_to_list(filename):
  """Open a csv file. Return its content as a list of integers or strings"""
  with open(filename, 'r') as f:
    # skip first line (header)
    first_line = f.readline()

    # put data from csv into a list. use "," to separate elements
    num_list = [[int(value) if value.rstrip().isdigit() else value for value in row.split(',')] for row in f.readlines()]
  f.close
  return num_list


def output_file(filename):
  """Create the output file. Add header"""
  f = open(filename, 'w')

  # write header
  f.write('department_id,number_of_orders,number_of_first_orders,percentage\n')
  f.close()

  return

  
def add_to_output(filename, row):
  """Open output file in Append mode to write each row"""
  f = open(filename, 'a')

  # format and join text with a comma
  format_row = ['{}'.format(i) for i in row]
  write_row = ','.join(format_row) + '\n'
  f.write(write_row)
  f.close()
  
  return
 

# main function
def main():
  if len(sys.argv) != 4:
    print('usage: ./run.py input-file-1 input-file-2 output-file')
    sys.exit(1)

  # convert input files into lists
  product_list = csv_to_list(sys.argv[2]) 
  order_list = csv_to_list(sys.argv[1])

  # create a dictionary from the previous list. product_dict only uses
  # first and last elements of each row (product_id, department_id)
  product_dict = {}
  
  for row in product_list:
    prod_id, *useless, dept_id = row
    
    # product_id as key for the dictionary
    if prod_id not in product_dict:
      product_dict[prod_id] = dept_id 

  # create two dictionaries to count products per department
  # each iteration adds 1 per product found on the order
  departments = {}
  depts_reorder = {}
  
  for row in order_list:
    order_id, prod_id, *useless, reordered = row
    dept_id = product_dict[prod_id]
    
    # department_id as key for the dictionary
    if dept_id not in departments:
      departments[dept_id] = []
    
    # add 1 (assuming each row in order_product.csv contains only one product)
    departments[dept_id].append(1)
    
    # inverse logic. we're interested in products which haven't been ordered before
    if reordered == 0:
      if dept_id not in depts_reorder:
        depts_reorder[dept_id] = []
      
      # add 1 according to the inverse logic
      depts_reorder[dept_id].append(1)

  # get a sorted version of departments
  sorted_depts = sorted(departments.keys())

  # create csv
  output_file(sys.argv[3])

  # add rows to output file in order
  for dept in sorted_depts:
    # first element: department_id
    row = []
    row.append(dept)

    # second: orders per department
    total_orders = sum(departments[dept])
    row.append(total_orders)
    
    # third: first ordered products per department
    if dept in depts_reorder:
      total_first_ord = sum(depts_reorder[dept])
    else:
      total_first_ord = 0
    row.append(total_first_ord)
   
    # fourth: calculate percentage
    percent = total_first_ord / total_orders
    format_percent = '{0:.2f}'.format(percent)
    row.append(format_percent)
 
    # write full row in output file
    add_to_output(sys.argv[3], row)

if __name__ == '__main__':
  main()
