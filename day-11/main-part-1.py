import time
import copy

def decode_data(data: list):
    inputs = []
    outputs = []
    for line in data:
        input, output = line.replace('\n', '').split(': ')
        inputs.append(input)
        outputs.append(output.split(' '))

    return inputs, outputs

def path_constructor(start_index: int, inputs: list, outputs: list, nr_paths: list):
    for out in outputs[start_index]:
        if out == 'out':
            # Finish recursion loop
            nr_paths[0] += 1
        else:
            # Search next connection in the total list
            idx_next = inputs.index(out)

            # Continue with the recursion until "out" is found
            path_constructor(idx_next, inputs, outputs, nr_paths)

def path_constructor_dac_fft(start_index: int, inputs: list, outputs: list, nr_paths: list, flag_dac: bool, flag_fft:bool, visited_nodes: list):
    tmp_visited_nodes = copy.deepcopy(visited_nodes)
    for out in outputs[start_index]:
        if out == 'out':
            # Finish recursion loop

            # Check if flags are true, if not, do not increase the counter.
            if flag_dac and flag_fft:
                nr_paths[0] += 1
                print('Found one')
        else:
            if out == 'dac':
                flag_dac = True
            elif out == 'fft':
                flag_fft = True

            # Search next connection in the total list
            idx_next = inputs.index(out)

            if out in visited_nodes:
                # Nodes already visited, we are in a loop. Break.
                print('Circular loop, quit path')
            else:
                # Continue with the recursion until "out" is found
                visited_nodes.append(out)
                path_constructor_dac_fft(idx_next, inputs, outputs, nr_paths, flag_dac, flag_fft, visited_nodes)

                # Restore original visited_nodes for the new path
                visited_nodes = copy.deepcopy(tmp_visited_nodes)

def reverse_recursion(start_index: int, inputs: list, outputs: list, nr_paths: list, flag_dac: bool, flag_fft:bool):
    for ins in inputs[start_index]:
        if ins == 'svr':
            # Finish recursion loop
            # Check if flags are true, if not, do not increase the counter.
            if flag_dac and flag_fft:
                nr_paths[0] += 1
        else:
            if ins == 'dac':
                flag_dac = True
            elif ins == 'fft':
                flag_fft = True

            # Search next connections in the total list
            indices = [i for i, x in enumerate(outputs) if x == "whatever"]
            idx_next = inputs.index(out)

            # Continue with the recursion until "out" is found
            path_constructor_dac_fft(idx_next, inputs, outputs, nr_paths, flag_dac, flag_fft)

def path_constructor_new_end(end: str, start_index: int, inputs: list, outputs: list, nr_paths_ending_in_out: list, nr_paths_ending_in_end: list):
    for out in outputs[start_index]:
        if out == 'out':
            # Ending in out before reaching the wanted end
            nr_paths_ending_in_out[0] += 1
        elif out == end:
            nr_paths_ending_in_end[0] += 1

        else:
            # Search next connection in the total list
            idx_next = inputs.index(out)

            # Continue with the recursion until "out" is found
            path_constructor_new_end(end, idx_next, inputs, outputs, nr_paths_ending_in_out, nr_paths_ending_in_end)

# PART 1

start_time = time.time()

password = 0
filename = 'data/input.txt'

with open(filename, 'r') as f:
    data_ = f.readlines()

in_data, out_data = decode_data(data_)

nr_of_paths = [0]

# Find the 'you' path start point
idx_start = in_data.index('you')
path_constructor(idx_start, in_data, out_data, nr_of_paths)

print('Part 1 solution: ', nr_of_paths[0])
print('Elapsed time:', time.time()-start_time, 'seconds')
