import re
import linecache
import xlsxwriter

def extract_lines(filename, output_filename, start_line, end_line):
    with open(filename) as f1, open(output_filename, 'a') as f2:
        for i, line in enumerate(f1):
            if start_line in str(line):
                for j in range(i+1, i+end_line+1):
                    f2.write(linecache.getline(filename, j))
        f2.close()
        f1.close()

def write_data_to_excel(input_file, output_file, search_line, column_name):
    workbook = xlsxwriter.Workbook(output_file)
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': 1})
    worksheet.write('A1', column_name, bold)
    
    with open(input_file) as f:
        row = 1
        col = 0
        array = []
        for line in f:
            if search_line in line:
                x = re.split(search_line, line)
                array.append(x[1])
                if len(array) == 27:
                    a = list(map(str.strip, array))
                    for item in a:
                        worksheet.write(row, col, item)
                        row += 1
                    row += 1
                    array = []
        f.close()

    workbook.close()

# Specify the input and output file names
input_filename = 'results.txt'
output_filename = 'results2.txt'
excel_filename = 'thread_results.xlsx'

# Extract the desired lines from the input file
extract_lines(input_filename, output_filename, "No of threads spawned 27", 194)

# Write the extracted data to an Excel file
write_data_to_excel(output_filename, excel_filename, "time taken to create extra routers", "time taken to create extra routers")
