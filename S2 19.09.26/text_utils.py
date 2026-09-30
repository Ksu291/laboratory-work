
def load_data():
    data = [3, 17, 8, 25, 6, 12, 25, 9, 14]
    return data

def filter_above(values,threshold):
    return [value for value in values if value>threshold]

def mean(values):
    return sum(values)/len(values)
