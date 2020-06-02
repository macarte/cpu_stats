import pickle

VERSION_PROCESS_CPU_PERCENTAGE = "VERSION_PROCESS_CPU_PERCENTAGE" 
VERSION_CPU_PERCENTAGES = "VERSION_CPU_PERCENTAGES" 
VERSION_CPU_TIMES_PERCENTAGES = "VERSION_CPU_TIMES_PERCENTAGES" 

def start_recording(version, output, start_time, num_cpus):
    pickle.dump(version, output)
    pickle.dump(start_time, output)
    pickle.dump(num_cpus, output)


def write_cpu_stats(output, time_offset, cpu_stats):
    pickle.dump(time_offset, output)
    pickle.dump(cpu_stats, output)

def end_recording(output):
    pass

def start_reading(input):
    binary_version = pickle.load(input)
    start_time = pickle.load(input)
    num_cpus = pickle.load(input)
    return binary_version, start_time, num_cpus

def start_reading_version(version, input):
    binary_version = pickle.load(input)
    assert binary_version == version, "binary file is not of the expected format"

    start_time = pickle.load(input)
    num_cpus = pickle.load(input)
    return start_time, num_cpus

def read_cpu_stats(input):
    time_offset = pickle.load(input)
    cpu_stats = pickle.load(input)
    return time_offset, cpu_stats

def end_reading(input):
    pass