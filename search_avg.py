import re
import statistics as s
values=[]
import numpy as np
#numbers=[]
with open('results.txt') as file:
    for line in file:
            if "7. Time taken to create s2s connectivity" in line:
                x=re.split("7. Time taken to create s2s connectivity", line)
                values.append(x[1])
    a=list(map(str.strip, values))
    #numbers = [int(float(x)) for x in a]
    x = np.array(a)
    y = x.astype(np.float)
    print (y)
    print (np.mean(y))
