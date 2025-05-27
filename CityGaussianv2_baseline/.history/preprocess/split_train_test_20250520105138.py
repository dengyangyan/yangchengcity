import numpy as np
def load_data(file):
    with open(file) as f:
        data = f.readlines()

    data = [data[2*i+5].strip() for i in range((len(data)-4)//2)]