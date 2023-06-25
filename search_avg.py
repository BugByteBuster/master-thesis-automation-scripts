import re
import statistics as s
import numpy as np

def extract_data(file_path, keyword):
    values = []
    with open(file_path) as file:
        for line in file:
            if keyword in line:
                x = re.split(keyword, line)
                values.append(x[1])
    return list(map(str.strip, values))

def calculate_mean(data):
    x = np.array(data)
    y = x.astype(np.float)
    return np.mean(y)

# Define the file path and keyword
file_path = 'results.txt'
keyword = "7. Time taken to create s2s connectivity"

# Extract the data and calculate the mean
data = extract_data(file_path, keyword)
mean = calculate_mean(data)

# Print the mean value
print(mean)
