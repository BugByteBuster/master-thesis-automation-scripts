"""
import re
import numpy as np
import xlsxwriter


workbook = xlsxwriter.Workbook('thread_results.xlsx')
worksheet = workbook.add_worksheet()
bold = workbook.add_format({'bold': 1})
worksheet.write('A1', 'time taken to create extra routers', bold)

def input(string, row, col):
    with open("results.txt") as f:
        array=[]
        for line in f:
            if str(string) in line:
                x = re.split(string, line)
                array.append((x[1]))
        a = list(map(str.strip, array))
        # print (a)
        #a = sorted(a, key=lambda x: float(x))
        for item in a:
            worksheet.write(row, col, item)
            row +=1
input("time taken to create extra routers", 1, 0)
workbook.close()
"""
from openpyxl import *
import xlsxwriter
import re
import linecache
line1="No of threads spawned 27"
line2="time taken to create extra routers"


workbook = xlsxwriter.Workbook('thread_results.xlsx')
worksheet = workbook.add_worksheet()
bold = workbook.add_format({'bold': 1})
worksheet.write('A1', 'time taken to create extra routers', bold)

with open('results.txt') as f1, open('results2.txt', 'a') as f2:
    for i, line in enumerate(f1):
        if line1 in str(line):
            for j in range(i+1, i+195):
                f2.write(linecache.getline('results.txt', j))
    f2.close()
    f1.close()

with open('results2.txt') as f3:
        row=1
        col=0
        array = []
        for f3_line in f3:
            if line2 in f3_line:
                x = re.split(line2, f3_line)
                array.append(x[1])
                if len(array) == 27:
                    a = list(map(str.strip, array))
                    for item in a:
                        worksheet.write(row, col, item)
                        row += 1
                    row = row + 1

                    array = []
        f3.close()

workbook.close()



