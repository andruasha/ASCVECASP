import matplotlib.pyplot as plt
import random


def addNode(nodesCoords):

    nodesCoordsKeys = list(nodesCoords.keys())
    random.shuffle(nodesCoordsKeys)
    nodesCoords = {key: nodesCoords[key] for key in nodesCoordsKeys}

    newNodeCoords = findRightAngle(nodesCoords)

    if not newNodeCoords:
        newNodeCoords = findDoubleNodes(nodesCoords)

    nodesCoords['node' + str(len(nodesCoords) + 1)] = newNodeCoords

    return nodesCoords


def findRightAngle(nodesCoords):
    def check_condition(target, cond1, cond2, exclude):
        if target in nodesCoords.values() and cond1 in nodesCoords.values() and exclude not in nodesCoords.values():
            return exclude
        return None

    for node, coords in nodesCoords.items():
        checks = [
            lambda: check_condition(
                {'x': coords['x']+5, 'y': coords['y']},
                {'x': coords['x'], 'y': coords['y']-5},
                None,
                {'x': coords['x']+5, 'y': coords['y']-5}
            ),
            lambda: check_condition(
                {'x': coords['x']+5, 'y': coords['y']},
                {'x': coords['x'], 'y': coords['y']+5},
                None,
                {'x': coords['x']+5, 'y': coords['y']+5}
            ),
            lambda: check_condition(
                {'x': coords['x']-5, 'y': coords['y']},
                {'x': coords['x'], 'y': coords['y']-5},
                None,
                {'x': coords['x']-5, 'y': coords['y']-5}
            ),
            lambda: check_condition(
                {'x': coords['x']-5, 'y': coords['y']},
                {'x': coords['x'], 'y': coords['y']+5},
                None,
                {'x': coords['x']-5, 'y': coords['y']+5}
            )
        ]

        random.shuffle(checks)

        for check in checks:
            result = check()
            if result:
                return result

    return None


def findDoubleNodes(nodesCoords):

    def check_direction(nodesCoords, target, first_pair, second_pair):
        if target in nodesCoords.values():
            if all(pair not in nodesCoords.values() for pair in first_pair):
                return random.choice(first_pair)
            if all(pair not in nodesCoords.values() for pair in second_pair):
                return random.choice(second_pair)
        return None

    for node, coords in nodesCoords.items():
        checks = [
            lambda: check_direction(
                nodesCoords, {'x': coords['x']+5, 'y': coords['y']},
                [{'x': coords['x'], 'y': coords['y']+5}, {'x': coords['x']+5, 'y': coords['y']+5}],
                [{'x': coords['x'], 'y': coords['y']-5}, {'x': coords['x']+5, 'y': coords['y']-5}]
            ),
            lambda: check_direction(
                nodesCoords, {'x': coords['x']-5, 'y': coords['y']},
                [{'x': coords['x'], 'y': coords['y']+5}, {'x': coords['x']-5, 'y': coords['y']+5}],
                [{'x': coords['x'], 'y': coords['y']-5}, {'x': coords['x']-5, 'y': coords['y']-5}]
            ),
            lambda: check_direction(
                nodesCoords, {'x': coords['x'], 'y': coords['y']+5},
                [{'x': coords['x']+5, 'y': coords['y']}, {'x': coords['x']+5, 'y': coords['y']+5}],
                [{'x': coords['x']-5, 'y': coords['y']}, {'x': coords['x']-5, 'y': coords['y']+5}]
            ),
            lambda: check_direction(
                nodesCoords, {'x': coords['x'], 'y': coords['y']-5},
                [{'x': coords['x']+5, 'y': coords['y']}, {'x': coords['x']+5, 'y': coords['y']-5}],
                [{'x': coords['x']-5, 'y': coords['y']}, {'x': coords['x']-5, 'y': coords['y']-5}]
            )
        ]

        random.shuffle(checks)

        for check in checks:
            result = check()
            if result:
                return result


plt.figure(figsize=(10, 10))
plt.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray')
plt.xticks(range(-12, 13, 1))
plt.yticks(range(-12, 13, 1))

plt.xlim(-12, 12)
plt.ylim(-12, 12)

nodesNum = 8
nodesCoords = {'node1': {'x': 0, 'y': 0},
               'node2': {'x': 5, 'y': 0},
               'node3': {'x': 5, 'y': -5}}

while len(nodesCoords) < nodesNum:
    nodesCoords = addNode(nodesCoords)

for node in nodesCoords.values():
    plt.plot(node['x'], node['y'], 'ko')

plt.show()