import xlsxwriter
import random

# Create an new Excel file and add a worksheet.
workbook = xlsxwriter.Workbook('employee_ssn_data.xlsx')
worksheet = workbook.add_worksheet()

# Write some simple text.
worksheet.write('A1', 'Employee')
worksheet.write('B1', "SSN")

for i in range(2, 50):
    # Write employee name
    random_first = random.choice(open("first_name.txt").readlines())
    random_last = random.choice(open("last_name.txt").readlines())
    worksheet.write(f'A{i}', f'{random_first} {random_last}')

    #Generate SSN in form AAA-BB-CCCC
    worksheet.write(f'B{i}', f'{random.randint(0,9)}{random.randint(0,9)}{random.randint(0,9)}-{random.randint(0,9)}{random.randint(0,9)}-{random.randint(0,9)}{random.randint(0,9)}{random.randint(0,9)}{random.randint(0,9)}')

workbook.close()
