import time

class Node:
    def __init__(self, name):
        self.name = name
        self.parents = []
        self.children = []
        self.value = 0
        self.in_edge = []
        self.out_edge = []

class Edge:
    def __init__(self, start: Node, end: Node, start_value=0):
        self.start = start
        self.end = end
        self.value = start_value

def decode_data(data: list):
    inputs = []
    outputs = []
    for line in data:
        input, output = line.replace('\n', '').split(': ')
        inputs.append(input)
        outputs.append(output.split(' '))

    return inputs, outputs

def generate_graph(in_data, out_data):
    # Create graph
    graph = []

    for node_name in in_data:
        new_node = Node(node_name)
        graph.append(new_node)

    # Assign children
    for i, node in enumerate(graph):
        for child in out_data[i]:
            if child != '!':
                child_idx = in_data.index(child)
                child_node = graph[child_idx]
                node.children.append(child_node)

    # Assign parents
    for i, node in enumerate(graph):
        parents_indices = [i for i, outputs in enumerate(out_data) if node.name in outputs]

        for parent_idx in parents_indices:
            parent_node = graph[parent_idx]
            node.parents.append(parent_node)

    # Assign edges
    for i, ins in enumerate(in_data):
        for outs in out_data[i]:
            if outs != '!':
                out_idx = in_data.index(outs)
                new_edge = Edge(graph[i], graph[out_idx])
                graph[i].out_edge.append(new_edge)
                graph[out_idx].in_edge.append(new_edge)

    return graph

def search_node(graph: list, name: str) -> int | None:
    # Return index of node with certain name

    for i, node in enumerate(graph):
        if node.name == name:
            return i

def djisktra_recursive(graph: list, end_idx: int):
    tmp_graph = graph.copy()

    end_node = tmp_graph.pop(end_idx)

    for edge in end_node.in_edge:
        # Assign value = 1 to the in-edges of the end node
        edge.value = 1

    # Start loop
    while len(tmp_graph) > 0:
        current_node = tmp_graph.pop(0)
        no_children_flag = True
        for child in current_node.children:
            if child in tmp_graph:
                # Children not checked yet, to be re-done afterwards
                no_children_flag = False
                break

        if current_node.children == [] or no_children_flag:
            # Update in-edge values
            new_value = sum([x.value for x in current_node.out_edge])
            for in_edge in current_node.in_edge:
                in_edge.value = new_value

            # Update node value
            current_node.value = new_value
        else:
            # Node not ready for analysis, re-add it to the list
            tmp_graph.append(current_node)


start_time = time.time()

password = 0
filename = 'data/input-part-2.txt'

with open(filename, 'r') as f:
    data = f.readlines()

in_data, out_data = decode_data(data)


# END NODE: OUT
graph = generate_graph(in_data, out_data)

# Search ending node
end_idx = search_node(graph, 'out')

# Set nr of path to ending node to 1 and children to []
djisktra_recursive(graph, end_idx)

# Nr of path [dac --> out]
idx_dac = search_node(graph, 'dac')
paths_dac_out = graph[idx_dac].value
print('DAC -> OUT', paths_dac_out)

# Nr of path [fft --> out]
idx_fft = search_node(graph, 'fft')
paths_fft_out = graph[idx_fft].value
print('FFT -> OUT', paths_fft_out)

# Nr of path [svr --> out]
idx_svr = search_node(graph, 'svr')
paths_svr_out = graph[idx_svr].value
print('SVR -> OUT', paths_svr_out)

# Clean graph variable
del graph


# END NODE: FFT
graph = generate_graph(in_data, out_data)

# Search ending node
end_idx = search_node(graph, 'fft')

# Set nr of path to ending node to 1 and children to []
graph[end_idx].children = []
graph[end_idx].out_edge = []
djisktra_recursive(graph, end_idx)

# Nr of path [dac --> fft]
idx_dac = search_node(graph, 'dac')
paths_dac_fft = graph[idx_dac].value
print('DAC -> FFT', paths_dac_fft)

# Nr of path [svr --> fft]
idx_svr = search_node(graph, 'svr')
paths_svr_fft = graph[idx_svr].value
print('SVR -> FFT', paths_svr_fft)

# Clean graph variable
del graph


# END NODE: DAC
graph = generate_graph(in_data, out_data)

# Search ending node
end_idx = search_node(graph, 'dac')

# Set nr of path to ending node to 1 and children to []
graph[end_idx].children = []
graph[end_idx].out_edge = []
djisktra_recursive(graph, end_idx)

# Nr of path [fft --> dac]
idx_fft = search_node(graph, 'fft')
paths_fft_dac = graph[idx_fft].value
print('FFT -> DAC', paths_fft_dac)

# Nr of path [svr --> dac]
idx_svr = search_node(graph, 'svr')
paths_svr_dac = graph[idx_svr].value
print('SVR -> DAC', paths_svr_dac)


print('Part 2 solution: ', paths_svr_fft*paths_fft_dac*paths_dac_out + paths_svr_dac*paths_dac_fft*paths_fft_out)
print('Elapsed time:', time.time()-start_time, 'seconds')
