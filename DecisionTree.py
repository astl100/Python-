import math


# find most common value for an attribute
def majority(attributes, data, target):
    # collects target values
    valFreq = {}
    target_index = attributes.index(target)

    # calculate frequency of values for target
    for tuple in data:
        if ((tuple[target_index]) in valFreq):
            valFreq[tuple[target_index]] += 1
        else:
            valFreq[tuple[target_index]] = 1
    max = 0
    major = ""

    # finds majority target value
    for key in valFreq.keys():
        if valFreq[key]>max:
            max = valFreq[key]
            major = key
    return major



# calculates entropy of given data set for target attribute
def entropy(attributes, data, targetAttr):
    valFreq = {}
    dataEntropy = 0.0

    # index of the target attribute
    i = 0
    for entry in attributes:
        if (targetAttr == entry):
            break
        ++i

    # find frequency of values of target attribute
    for entry in data:
        if ((entry[i]) in valFreq):
            valFreq[entry[i]] += 1.0
        else:
            valFreq[entry[i]]  = 1.0

    # calculates entropy of data for target attribute
    for freq in valFreq.values():
        dataEntropy += (-freq/len(data)) * math.log(freq/len(data), 2)

    return dataEntropy



# calculates gain by splitting on given attribute
#           reduce entropy
def gain(attributes, data, attr, targetAttr):
    valFreq = {}
    subsetEntropy = 0.0

    # index of given attribute
    i = attributes.index(attr)

    # find frequency of values of target attribute
    for entry in data:
        if ((entry[i]) in valFreq):
            valFreq[entry[i]] += 1.0
        else:
            valFreq[entry[i]]  = 1.0

    # calculate entropy for each subset based on probability in training set
    for val in valFreq.keys():
        prob = valFreq[val] / sum(valFreq.values())
        dataSubset = [entry for entry in data if entry[i] == val]
        subsetEntropy += prob * entropy(attributes, dataSubset, targetAttr)

    # subtract chosen attribute entropy from whole data set and return
    return (entropy(attributes, data, targetAttr) - subsetEntropy)



# find best attibute to classify data off of
def chooseAttr(data, attributes, target):
    best = attributes[0]
    maxGain = 0;

    for att in attributes:
        newGain = gain(attributes, data, att, target)
        if newGain>maxGain:
            maxGain = newGain
            best = att
    return best



# get values in the column of the given attribute
def getValues(data, attributes, attr):
    index = attributes.index(attr)
    values = []

    for entry in data:
        if entry[index] not in values:
            values.append(entry[index])
    return values



def getExamples(data, attributes, best, val):
    examples = [[]]
    index = attributes.index(best)

    for entry in data:
        # find entries with the give value
        if (entry[index] == val):
            newEntry = []
            # add value if it is not in best column
            for i in range(0,len(entry)):
                if(i != index):
                    newEntry.append(entry[i])
            examples.append(newEntry)

    examples.remove([])
    return examples



def makeTree(data, attributes, target, recursion):
    recursion += 1

    vals = [record[attributes.index(target)] for record in data]
    default = majority(attributes, data, target)

    # if dataset empty or attributes list empty(other than target)
    if not data or (len(attributes) - 1) <= 0:
        return default

    # if all same classification
    elif vals.count(vals[0]) == len(vals):
        return vals[0]
    else:
        # next best attribute to classify data
        best = chooseAttr(data, attributes, target)
        # new decision tree/node with the best attribute
        tree = {best:{}}

        # new decision tree/sub-node for values in attribute field
        for val in getValues(data, attributes, best):
            # subtree for value under the "best" field
            examples = getExamples(data, attributes, best, val)
            newAttr = attributes[:]
            newAttr.remove(best)
            subtree = makeTree(examples, newAttr, target, recursion)

            # add subtree to dictionary object in tree
            tree[best][val] = subtree

    return tree
