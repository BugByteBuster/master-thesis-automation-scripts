import re
import xlsxwriter
import numpy as np
import statistics as s

workbook = xlsxwriter.Workbook('arrays.xlsx')
worksheet = workbook.add_worksheet()
bold = workbook.add_format({'bold': 1})
worksheet.write('A1', 'time taken to add subnet', bold)
worksheet.write('B1', 'time taken to handle the router port request in agent cloud', bold)
worksheet.write('C1', 'time taken to duplicate router and router port rc', bold)
worksheet.write('D1', 'time taken to duplicate router', bold)
worksheet.write('E1', 'time taken to duplicate router port', bold)
worksheet.write('F1', 'time taken to create ipsec, ike and vpnsservice', bold)
worksheet.write('G1', 'time taken to create ipse', bold)
worksheet.write('H1', 'time taken to create ike', bold)
worksheet.write('I1', 'time taken to establish s2s connectivity', bold)
worksheet.write('J1', 'No of threads spawned', bold)
worksheet.write('K1', 'time taken by threads', bold)
worksheet.write('L1', 'avg of tatal time taken to create extra router', bold)
worksheet.write('M1', 'average time taken to get external network id', bold)
worksheet.write('N1', 'avg time taken to create extra router', bold)
worksheet.write('O1', 'avg time taken to create port on the router', bold)
worksheet.write('P1', 'avg time taken to attach subnet to the router', bold)
worksheet.write('Q1', 'avg time taken to create vpn service on extra routers(only threads)', bold)
worksheet.write('R1', 'avg time taken for updating routes', bold)
worksheet.write('S1', 'time taken for creating s2s', bold)
worksheet.write('T1', 'avg time taken to create s2s', bold)

def formater(input, val, col):
    avglist=[]
    values=[]
    row = val
    col = col
    with open('results.txt') as file:
        for line in file:
            if str(input) in line:
                x = re.split(str(input), line)
                values.append(x[1])
        a = list(map(str.strip, values))
        a = np.array(a)
        print(a)
        list2 = []
        for i in (3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27):
            list2.append(a[0:i])
            a = a[i:]
            # print(a)
        list2 = np.array(list2)
        # print (list2)
        for item in list2:
            item = list(map(float, item))
            print(len(item))
            print((item))
            print(s.mean((item)))
            avglist.append(s.mean((item)))
        print (avglist)
        for item in (avglist):
            worksheet.write(row, col, item)
            row += 1
def extract(input, val,col):
    print(input)
    avglist = []
    values = []
    row=val
    col=col
    if input == "time taken to create extra routers":
        formater(input, val, col)
    elif input=="time taken to get external network_id:":
        formater(input, val, col)
    elif input=="time taken to create only router extra":
        formater(input, val, col)
    elif input=="time taken to create port only":
        formater(input, val,col)
    elif input=="time_taken to attach subnet to router":
        formater(input, val,col)
    elif input=="time taken to create VPN service on the router":
        with open('results.txt') as file:
            for line in file:
                if str(input) in line:
                    x = re.split(str(input), line)
                    values.append(x[1])
            a = list(map(str.strip, values))
            a = np.array(a)
            print(a)
            list2 = []
            for i in (2,4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28):
                list2.append(a[0:i])
                a = a[i:]
                # print(a)
            list2 = np.array(list2)
            # print (list2)
            for item in list2:
                item = list(map(float, item))
                print(len(item))
                print((item))
                print(s.mean((item[1:])))
                avglist.append(s.mean((item[1:])))
            print(avglist)
            for item in (avglist):
                worksheet.write(row, col, item)
                row += 1
    elif input=="time taken for updating routes":
        formater(input, val, col)
    elif input=="Time taken to create s2s connectivity":
        with open('results.txt') as file:
            for line in file:
                if str(input) in line:
                    x = re.split(str(input), line)
                    values.append(x[1])
            a = list(map(str.strip, values))
            a = np.array(a)
            print(a)
            list2 = []
            for i in (2,4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28):
                list2.append(a[0:i])
                a = a[i:]
                # print(a)
            list2 = np.array(list2)
            # print (list2)
            for item in list2:
                item = list(map(float, item))
                print(len(item))
                print((item))
                print(s.mean((item)))
                avglist.append(s.mean((item)))
            print(avglist)
            for item in (avglist):
                worksheet.write(row, col, item)
                row += 1
    else:
        with open('results.txt') as file:
            for line in file:
                if str(input) in line:
                    x=re.split(str(input), line)
                    values.append(x[1])
            a = list(map(str.strip, values))
            x = np.array(a)
            #print (x)
        for item in (x):
            worksheet.write(row, col, item)
            row += 1


extract("time taken to add subnet", 1, 0)
extract("time taken to handle the router port request in agent cloud", 1, 1)
extract("time_taken to duplicate router and router port", 1,2)
extract("time_taken_for_duplicate_router", 1,3)
extract("Time taken to duplicate router port",1, 4)
extract("time_taken to create ipsec, ike and vpn service", 2, 5)
extract("Time taken to create ipsec policy",2,6)
extract("Time taken to create ike policy", 2, 7)
extract("time_taken to establish s2s connectivity", 2, 8)
extract("No of threads spawned", 3, 9)
extract("time_taken_for_thread", 3, 10)
extract("time taken to create extra routers", 3, 11)
extract("time taken to get external network_id:", 3, 12)
extract("time taken to create only router extra", 3, 13)
extract("time taken to create port only", 3, 14)
extract("time_taken to attach subnet to router", 3, 15)
extract("time taken to create VPN service on the router", 2, 16)
extract("time taken for updating routes",3, 17)
extract("time taken for creating s2s", 3,18)
extract("Time taken to create s2s connectivity", 2, 19)

workbook.close()
