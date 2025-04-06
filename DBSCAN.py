import numpy as np

def cos_distance(v, w):
    return 1 - np.dot(v, w) / (np.linalg.norm(v) * np.linalg.norm(w))


class DBScan:
    def __init__(self, min_neighbors, eps):
        self.mat = np.empty(0)
        self.labels = np.empty(0, dtype=np.int32)
        self.isCore = np.empty(0, dtype=np.bool)
        self.numClusters = 0

        self.min_neighbors = min_neighbors
        self.eps = eps

    def get_neighbors(self, idx):
        neighbors = []

        for i in range(len(self.mat)):
            if i != idx and cos_distance(self.mat[idx], self.mat[i]) <= self.eps:
                neighbors.append(i)

        return neighbors

    #assume old > new
    def combine(self, old, new):
        if old == new:
            return

        self.numClusters -= 1

        for i in range(len(self.labels)):
            if self.labels[i] == old:
                self.labels[i] = new

            #important
            #don't forget you did this when you combine multiple clusters you big dum dum (me)
            if self.labels[i] > old:
                self.labels[i] -= 1

    def add(self, v):
        if len(self.mat) == 0:
            self.mat = np.array([v])

        else:
            self.mat = np.append(self.mat, [v], axis=0)

        #Get new cores
        #check neighbors and v
        #add to new_cores
        new_cores = []
        neighbor_labels = []
        v_idx = len(self.mat) - 1

        #check if v is core
        if len(self.get_neighbors(v_idx)) >= self.min_neighbors:
            new_cores.append(v_idx)

            self.labels = np.append(self.labels, self.numClusters + 1)
            self.isCore = np.append(self.isCore, True)

        #v is not core
        else:
            self.labels = np.append(self.labels, -1)
            self.isCore = np.append(self.isCore, False)

        #Update neighbors
        #If core: set label
            #update isCore
            #keep track of min cluster
        to_consider = self.get_neighbors(v_idx)
        if self.isCore[v_idx]:
            to_consider.append(v_idx)

        for neighbor in to_consider:
            cousins = self.get_neighbors(neighbor)

            #append new cores
            if self.isCore[neighbor] or len(cousins) >= self.min_neighbors:
                new_cores.append(neighbor)
                self.isCore[neighbor] = True

                #Note: cousins cannot change isCore
                for cousin in cousins:
                    # keep track of neighboring labels for cores
                    if self.labels[cousin] > 0 and self.labels[cousin] not in neighbor_labels:
                        neighbor_labels.append(self.labels[cousin])

                    #account for new non cores
                    elif self.labels[cousin] == -1:
                        self.labels[cousin] = self.numClusters + 1

        #Combine clusters if len of new_cores > 0
        #num clusters ++
        #sort neighbor_labels
        #combine last 2 labels until
        if len(new_cores) > 0:
            neighbor_labels.sort()
            neighbor_labels.append(self.numClusters + 1)

            self.numClusters += 1

            while len(neighbor_labels) >= 2:
                old = neighbor_labels[len(neighbor_labels) - 1]
                new = neighbor_labels[len(neighbor_labels) - 2]

                neighbor_labels.pop(-1)
                self.combine(old, new)

    def save(self):
        np.save("Matrix.npy", self.mat)
        np.save("Labels.npy", self.labels)
        np.save("isCore.npy", self.isCore)
        np.save("numClusters.npy", np.array([self.numClusters], dtype=np.int32))


    def load(self):
        self.mat = np.load("Matrix.npy")
        self.labels = np.load("Labels.npy")
        self.isCore = np.load("isCore.npy")
        self.numClusters = np.load("numClusters.npy")[0]

