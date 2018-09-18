import DecisionTree
import json

def main():
    target = "Play Tennis"
    data = [[]]

    op2 = open('tennis.csv').read()
    now2 = op2.strip(" ").split("\n")
    full_data = []

    # each element be its own entry in the list
    for line in now2:
        col = line.split("\t")
        full_data.append(col)
    labels = full_data[0]
    data = full_data[1:]

    # generate tree
    tree = DecisionTree.makeTree(data, labels, target, 0)
    print ("Decision Tree:")

    # convert dictionary to string output
    input = json.dumps(tree)
    ind_tree =  json.dumps(tree, sort_keys=True, indent=7)

    print (ind_tree)


main()

