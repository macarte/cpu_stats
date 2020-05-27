import argparse
import datetime
import numpy
import os
import sys
import psutil

import cpu_stat_file

def format_float_value(val: float) -> str:
    return ('%.2f' % val)

def run(input: str, display_header: bool) -> None:

    with open(input, "rb") as cpu_stats_input:
        start_time, num_cpus = cpu_stat_file.start_reading(version=cpu_stat_file.VERSION_CPU_PERCENTAGES, input=cpu_stats_input)
        num_samples = 0

        if display_header:
            header = "SampleTime,SampleOffset,Sample,CpuUsage,AggCpuUsage"
            for i in range(0,num_cpus): header = f"{header},Cpu{i}"
            print(header)

        try:
            while True:
                time_offset, cpu_usage = cpu_stat_file.read_cpu_stats(cpu_stats_input)
                sample_time = start_time + time_offset

                sum = numpy.sum(cpu_usage)
                total = sum / num_cpus
                per_cpu_str = ""
                for i,j in enumerate(cpu_usage): per_cpu_str = f"{per_cpu_str},{j}"
                print(f"{sample_time},{time_offset},{num_samples},{format_float_value(total)},{format_float_value(sum)}{per_cpu_str}")
                num_samples = num_samples + 1
        except EOFError:
            pass

def configure_arg_parser(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    parser = parser(description="Performance Monitor Script")
    parser.add_argument("--binary_input", help="binary file to dump to csv", required=True)
    parser.add_argument("--header", help="include csv header", action="store_true")
    return parser

def parse_args(parser: argparse.ArgumentParser) -> {}:
    return parser.parse_args()

def main(parser: argparse.ArgumentParser) -> None:
    args = parse_args(configure_arg_parser(parser))
    run(input=args.binary_input, display_header=args.header)

if __name__ == "__main__": \
    main(argparse.ArgumentParser)