from collections import defaultdict
import copy


def def_list():
    return []


def def_val():
    return 0


def euler_cycle(adjacency_list, debug=False):
    """
    for each qualified starting location, build a sample euler path from an adjacency list
    """
    unique_mers = set()
    # build dict from list
    mers_outbound = defaultdict(def_list)
    mers_count = defaultdict(def_val)
    seq_length = 1
    for line in adjacency_list:
        a, b = line.split("->")
        a = a.strip()
        unique_mers.add(a)
        mers = [n.strip() for n in b.split(",")]
        mers_outbound[a] += mers
        seq_length += len(mers)
        for m in mers:
            mers_count[m] += 1

    # build inbound dict
    mers_inbound = defaultdict(def_list)
    for k, v in mers_outbound.items():
        for mer in v:
            mers_inbound[mer].append(k)
            unique_mers.add(mer)

    starting_locations = []
    # find unbalanced nodes for starting location
    for mer in unique_mers:
        if len(mers_outbound[mer]) > len(mers_inbound[mer]):
            starting_locations.append(mer)

    # if no unbalanced node found, use all nodes as starting locations
    if not starting_locations:
        starting_locations = unique_mers

    eul_candidates = []
    for location in starting_locations:
        mers_outbound_temp = copy.deepcopy(mers_outbound)
        circuit = []
        stack = []
        while True:
            # http://www.graph-magics.com/articles/euler.php
            if location in mers_outbound_temp and len(mers_outbound_temp[location]) > 0:
                stack.append(location)
                location = mers_outbound_temp[location].pop()
            else:
                circuit.append(location)
                if stack:
                    location = stack.pop()
                else:
                    break
            if len(circuit) >= seq_length:
                break
        circuit.reverse()

        if len(circuit) > 1:
            eul_candidates.append(circuit)

    if debug:
        for e in eul_candidates:
            print(eul_candidates)
    return eul_candidates


def euler_cycle_all(adjacency_list, debug=False):
    """
    get all euler paths from a debrujin graph
    """
    unique_mers = set()
    # build dict from list
    mers_outbound = defaultdict(def_list)
    mers_count = defaultdict(def_val)
    seq_length = 1
    for l in adjacency_list:
        a, b = l.split("->")
        a = a.strip()
        unique_mers.add(a)
        mers = [n.strip() for n in b.split(",")]
        mers_outbound[a] += mers
        seq_length += len(mers)
        for m in mers:
            mers_count[m] += 1

    # build inbound dict
    mers_inbound = defaultdict(def_list)
    for k, v in mers_outbound.items():
        for mer in v:
            mers_inbound[mer].append(k)
            unique_mers.add(mer)

    starting_locations = []
    # find unbalanced nodes for starting location
    for mer in unique_mers:
        if len(mers_outbound[mer]) > len(mers_inbound[mer]):
            starting_locations.append(mer)

    # if no unbalanced node found, use all nodes as starting locations
    if not starting_locations:
        starting_locations = unique_mers

    all_paths = []
    for location in starting_locations:
        paths = []
        eul_recursive(mers_outbound, [location], paths)
        all_paths += paths

    qualified_paths = []
    for a in all_paths:
        if len(a) > len(adjacency_list):
            qualified_paths.append(a)

    if debug:
        print("euler paths")
        for q in qualified_paths:
            print(q)

    return qualified_paths


def eul_recursive(outbound, path, paths):
    """
    recursion helper for euler_cylce_all
    """
    if not outbound[path[-1]]:
        paths.append(path)
        return None
    for node in outbound[path[-1]]:
        outboundc = copy.deepcopy(outbound)
        outboundc[path[-1]].remove(node)
        eul_recursive(outboundc, path + [node], paths)


if __name__ == "__main__":

    datasets = ["dataset_203_sample.txt", "dataset_203_2-3.txt", "dataset_203_6-2.txt"]
    for i, d in enumerate(datasets):
        with open(d, "r") as f:
            adjanceny_list = f.read().splitlines()
            seq = euler_cycle(adjanceny_list)
            file = open('out_' + str(i) + '.txt', 'w')
            file.write("->".join(str(n) for n in seq))
            file.close()
