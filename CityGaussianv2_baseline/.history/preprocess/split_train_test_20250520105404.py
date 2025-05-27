import numpy as np
def load_data(train_file, total_file):
    with open(total_file) as f:
        totaldata = f.readlines()
    with open(train_file) as f:
        traindata = f.readlines()
    traindata = [traindata[2*i+5].strip().split(' ')[-1] for i in range((len(traindata)-4)//2)]
    # testdata
    with open(total_file) as f:
        totaldata = f.readlines()
    