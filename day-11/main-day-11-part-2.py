import time

def decode_data(data: list):
    inputs = []
    outputs = []
    for line in data:
        input, output = line.replace('\n', '').split(': ')
        inputs.append(input)
        outputs.append(output.split(' '))

    return inputs, outputs

def recursion_step(start_str_indices: list, inputs: list, outputs: list, path_counter: list, fft_flag: list, dac_flag: list):
    indices_for_next_step = []

    # Search for end_str in output list
    for start_idx in start_str_indices:
        # Search which outputs contains the input
        indices_input = [k for k, output in enumerate(outputs) if inputs[start_idx] in output]
        indices_for_next_step += indices_input

        # Update the path counter and the flags accordingly
        for j in indices_input:
            path_counter[j][outputs[j].index(inputs[start_idx])] *= sum(path_counter[start_idx])
            fft_flag[j] = fft_flag[j] or fft_flag[start_idx]
            dac_flag[j] = dac_flag[j] or dac_flag[start_idx]

        if inputs[start_idx] == 'svr':
            return

    # Polish indices list from duplicated
    indices_for_next_step = list(set(indices_for_next_step))
    print(len(indices_for_next_step))

    # Pop out done lines, otherwise risk of inner loops
    for i in start_str_indices:
        # inputs.pop(i)
        # Empty outputs to not fuck up the length
        outputs[i] = []

    # Continue recursion
    recursion_step(indices_for_next_step, inputs, outputs, path_counter, fft_flag, dac_flag)



start_time = time.time()

password = 0
filename = 'test-data-2.txt'

with open(filename, 'r') as f:
    data = f.readlines()

in_data, out_data = decode_data(data)

# Create path counter vector
path_counter = [len(x)*[1] for x in out_data]

# Create fft flag vector
fft_flag = len(in_data) * [False]
fft_flag[in_data.index('fft')] = True

# Create dac flag vector
dac_flag = len(in_data) * [False]
dac_flag[in_data.index('dac')] = True

end_str = 'out'

indices_start_str = []
for k, output in enumerate(out_data):
    if end_str in output:
        indices_start_str += [k]

recursion_step(indices_start_str, in_data, out_data, path_counter, fft_flag, dac_flag)

print(path_counter)
