import sys
import math
import random
import subprocess


#  opens given file
def openFile(filename):
    all_data = []
    points = []
    for line in open(filename).readlines():
		all_data.append(line.split())

    # convert entries to floats
    all_data = [[j for j in i] for i in all_data]

    for each_line in all_data[1:]:
        line = each_line[:4]
        points.append(line)

    for row in points:
        for ind in range(len(row)):
            row[ind] = float(row[ind])

    return points

# opens iris and creates global variable
points = openFile('iris.csv')


def main():
    num_clusters = 3
    opt_cutoff = 0.5

    # data from file
    clusters = kmeans(points, num_clusters, opt_cutoff)

    for i,c in enumerate(clusters):
        for p in c.points:
            print " Cluster: ", i, "\t Point :", p



class Cluster:

    def __init__(self, points):
        if len(points) == 0:
            raise Exception("Cluster is empty!")

        self.points = points

        # set initial centroid
        self.centroid = self.calculateCentroid()

    def __repr__(self):
        return str(self.points)

    def update(self, points):
        old_centroid = self.centroid
        self.points = points
        self.centroid = self.calculateCentroid()
        shift = getDistance(old_centroid, self.centroid)
        return shift

    def calculateCentroid(self):

        numPoints = len(self.points)

        # put all x's, y's, etc. together
        unzipped = zip(*points)
        
        # find mean for each
        for dList in unzipped:
            if numPoints == 0:
                centroid_coords = [0]
            else:
                centroid_coords = [math.fsum(dList)/numPoints]

        return centroid_coords

def kmeans(points, k, cutoff):

    # initialize centroids as random points
    initial = random.sample(points, k)

    # create clusters using the centroids
    clusters = [Cluster(p) for p in initial]

    loops = 0
    while True:
        # list of cluster points
        lists = [ [] for c in clusters]
        clusterCount = len(clusters)

        # counts loops
        loops += 1

        for p in points:
            # point and centroid distance
            smallest_distance = getDistance(p, clusters[0].centroid)

            # first cluster
            clusterIndex = 0

            # for the rest
            for i in range(clusterCount - 1):
                # point and other centroid distance
                distance = getDistance(p, clusters[i+1].centroid)
                # if closer to this centroid, update
                if distance < smallest_distance:
                    smallest_distance = distance
                    clusterIndex = i+1
            lists[clusterIndex].append(p)

        # biggest_shift is zero for this iteration
        biggest_shift = 0.0

        for i in range(clusterCount):
            # shift of centroid each iteration
            shift = clusters[i].update(lists[i])
            # largest shift of all centroid updates
            biggest_shift = max(biggest_shift, shift)

        # if shift is below cutoff, finished
        if biggest_shift < cutoff:
            print "Converged after %s iterations" % loops
            break
    return clusters

def getDistance(a, b):
    size = len(a)
    for ind in range(size):
        ret = reduce(lambda x,y: x + pow((a[y]-b[y]), 2) , range(1), 0.0)

    return math.sqrt(ret)


if __name__ == "__main__": 
    main()

