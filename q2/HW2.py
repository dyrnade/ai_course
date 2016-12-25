import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math as mt
from operator import itemgetter

# Part 1: Load the data
data = np.loadtxt('iris.data')
# Part 2: Plot 1st, 3rd and 4th features in 3D
fig_size = (30,20)
marker_size = 60
fig = plt.figure(figsize=fig_size)
data0 = data[data[:,4]==0]
data1 = data[data[:,4]==1]
data2 = data[data[:,4]==2]
ax = fig.add_subplot(111, projection='3d')
s = ax.scatter(data0[:,0],data0[:,2],data0[:,3], marker='o', c='r', s=marker_size)
s.set_edgecolors = s.set_facecolors = lambda *args:None
s = ax.scatter(data1[:,0],data1[:,2],data1[:,3], marker='o', c='g', s=marker_size)
s.set_edgecolors = s.set_facecolors = lambda *args:None
s = ax.scatter(data2[:,0],data2[:,2],data2[:,3], marker='o', c='b', s=marker_size)
s.set_edgecolors = s.set_facecolors = lambda *args:None

# Part 3: k-NN sub-functions implementation

# Part 3-1: Random seperation for training and test data.

# prepeare the test - train data for randomize seperation. We compute the necessary number of
# training & test sample dinamicly for choosing two third of the data (from each class) for train data
# and the remaining one third for test data

# (****don't use python library defined functions like "cross_validation" for randomized separation*****).

def rand_Train_Test(data):
    RandTrainData=[]
    RandTestData=[]

    # YOUR CODE HERE
    len_data = len(data)
    random_data = np.random.rand(len_data) < (2.0 / 3.0)
    RandTrainData = data[random_data]
    RandTestData = data[~random_data]
    return RandTrainData,RandTestData

# Part 3-2: Calculate the distance between any two points by using the Euclidean distance metric.
def find_Dist(sample1,sample2):
    euclid_Dist=0

    # YOUR CODE HERE
    euclid_Dist = np.sqrt(np.power(sample1[0] - sample2[0], 2.0) + np.power(sample1[2] - sample2[2], 2.0) + np.power(sample1[3] - sample2[3], 2.0))
    return euclid_Dist

# Part 3-3: Find the k nearest(most similar) neighbors of a test sample based on these pairwise distances(among the training dataset).
# Each test sample should be compared with all training data samples.

def find_Neighbours(training_data, test_data, k):
    all_Test_neighbours=[]
    # YOUR CODE HERE
    i = 0
    neighbors = []
    for i in np.arange(len(training_data)):
        distance = find_Dist(training_data[i], test_data)
        neighbors.append((training_data[i], distance))
    neighbors.sort(key=lambda distance_based: distance_based[1])
    for i in np.arange(k):
        all_Test_neighbours.append(neighbors[i])
    return all_Test_neighbours

# Part 3-4: Assign the class label of the test sample based on k nearest neighbors' majority.
#  (which class comes up the most often among the nearest neighbours).
#  ***** If the labels of k nearest neighbours are equally distributed for a test sample, you reject this test sample and use remaining test samples for computing the average error***.

def assign_Class(all_Test_neighbours):
    Test_Class_ids=[]

    # YOUR CODE HERE
    id_0 = id_1 = id_2 = 0
    for i in np.arange(len(all_Test_neighbours)):
        if int(all_Test_neighbours[i][0][4]) == 0:
            id_0 += 1
        elif int(all_Test_neighbours[i][0][4]) == 1:
            id_1 += 1
        else:
            id_2 += 1

    Test_Class_ids.append((0, id_0))
    Test_Class_ids.append((1, id_1))
    Test_Class_ids.append((2, id_2))

    return Test_Class_ids



# Part 4: Implement the function that runs k-NN with given different k values (1,2,3,4,5,6,7,8,9,10,11,12,13). For each k value, apply your k-NN on randomly seperated train-test data with 50 times.
#For all trials(times), calculate and record error rate then find the average error rate for each k values.

k=[1,2,3,4,5,6,7,8,9,10,11,12,13]
iterNum=50
average_err_for_ks=[]
# YOUR CODE HERE
def knn():
    errors = []
    for i in np.arange(len(k)):
        error = 0
        rejected = 0
        for iterN in np.arange(iterNum):
            training, test = rand_Train_Test(data)
            for t in np.arange(len(test)):
                neighbors = find_Neighbours(training, test[t], i+1)
                ids = assign_Class(neighbors)
                if ids[0][1] == ids[1][1] == ids[2][1]:
                    rejected += 1
                elif int(test[t][4]) is not max(ids, key=lambda maximum: maximum[1])[0]:
                   error += 1
        rate = error / ((float(len(test)) * iterNum) - rejected)
        errors.append(rate)
    return errors
average_err_for_ks = knn()

# Print Average error rate for corresponding k value on command window like below.
for i in range(len(average_err_for_ks)):
    print 'Average error rate for k=' + repr(k[i]) + '--> '+ repr(average_err_for_ks[i])

# Part 5: Plot the average error rate as a function of k. Then choose your optimal k value/values.
# Shortly explain your reason and how k value characteristic should be according to class number? (write your respond as a comment)

# YOUR CODE HERE
plt.figure()
plt.plot(k,average_err_for_ks)
plt.show()

'''
#################  Your Respond  ############################################

Optimal k is the lowest value of k.

Average error rate for k=1--> 0.047058823529411764
Average error rate for k=2--> 0.058260869565217394
Average error rate for k=3--> 0.034444444444444444
Average error rate for k=4--> 0.038507462686567163
Average error rate for k=5--> 0.0376
Average error rate for k=6--> 0.055
Average error rate for k=7--> 0.0391304347826087
Average error rate for k=8--> 0.04857142857142857
Average error rate for k=9--> 0.030384615384615385
Average error rate for k=10--> 0.0428
Average error rate for k=11--> 0.03791666666666667
Average error rate for k=12--> 0.0575609756097561
Average error rate for k=13--> 0.03490196078431373

For these values, "optimal k" is k=9.

For the even values of k , error rate increases and for the odd values of k, the error rate deacreses.

################################################cc##############################
'''
