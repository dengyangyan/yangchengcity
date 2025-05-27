import numpy as np
def load_data(train_file, total_file):
    with open(total_file) as f:
        totaldata = f.readlines()
    totaldata = [totaldata[2*i+5].strip().split(' ')[-1] for i in range((len(totaldata)-4)//2)]
    with open(train_file) as f:
        traindata = f.readlines()
    traindata = [traindata[2*i+5].strip().split(' ')[-1] for i in range((len(traindata)-4)//2)]
    # testdata
    testdata = totaldata.copy()
    for i in range(len(traindata)):
        testdata.remove(traindata[i])
    return traindata, testdata
def split_data(data, images_folder):
    # data: list
    # ratio: list
    # return: list
    images_folder 
    