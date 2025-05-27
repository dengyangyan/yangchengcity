import numpy as np
import shutil
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
def copyimage(data, images_folder, outputfolder):
    # data: list
    # ratio: list
    # return: list
    outputtest = images_folder + 'test/'
    outputtrain = images_folder + 'train/'
    for i in range(len(data)):
        shutil.copyfile(images_folder + data[i], outputfolder + data[i])
if __name__ == '__main__':
    traindata, testdata = load_data('/mnt/data/yangchengcity/slgy_s5_baitian/triangulated/images.txt', '/mnt/data/yangchengcity/slgy_s5_baitian/sparse/0/images.txt')
    copyimage(traindata, '/mnt/data/yangchengcity/slgy_s5_baitian/images', '/mnt/data/yangchengcity/slgy_s5_baitian/train/')
    copyimage(testdata, '/mnt/data/yangchengcity/slgy_s5_baitian/images', '/mnt/data/yangchengcity/slgy_s5_baitian/test/')
    