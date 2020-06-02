import argparse
import datetime
import numpy
import os
import sys
import psutil

import cpu_stat_file

def format_float_value(val: float) -> str:
    return ('%.2f' % val).rjust(6)

def format_float_as_int_value(val: float) -> str:
    return str(int(val)).rjust(6)

def format_int_value(val: int) -> str:
    return str(val).rjust(6)

def run(sample_interval: float, display_interval: float, output: str, duration: float, pid: int) -> None:

    cpu_count = psutil.cpu_count()
    next_output = 0
    process = psutil.Process(os.getpid())
    start_time = datetime.datetime.now()
    num_samples = 0
    process = psutil.Process(pid) if pid else None
    version = cpu_stat_file.VERSION_PROCESS_CPU_PERCENTAGE if pid else cpu_stat_file.VERSION_CPU_PERCENTAGES

    with open(output, "wb") as cpu_stats:
        cpu_stat_file.start_recording(version=version, output=cpu_stats, start_time=start_time, num_cpus=cpu_count)

        try:
            while duration > 0:
                if process:
                    cpu_usage = process.cpu_percent(interval=sample_interval)
                else:
                    cpu_usage = psutil.cpu_percent(interval=sample_interval, percpu=True)
                sample_time = datetime.datetime.now()
                sample_offset =  sample_time - start_time
                duration = duration - sample_interval
                cpu_stat_file.write_cpu_stats(output=cpu_stats, time_offset=sample_offset, cpu_stats=cpu_usage)
                num_samples = num_samples + 1

                if display_interval:
                    next_output = next_output - sample_interval
                    
                    if next_output < 0:
                        next_output = display_interval
                        num_bytes = (sys.getsizeof(cpu_usage) * num_samples) / 1_024

                        if process:
                            total = cpu_usage / cpu_count
                            print(f"{sample_time} [{format_int_value(num_samples)} / {format_float_as_int_value(num_bytes)} KB] {format_float_value(total)} / {format_float_value(cpu_usage)}")
                        else:
                            sum = numpy.sum(cpu_usage)
                            total = sum / cpu_count
                            per_cpu_str = ""
                            for i,j in enumerate(cpu_usage): per_cpu_str = f"{per_cpu_str} {format_float_value(j)},"
                            print(f"{sample_time} [{format_int_value(num_samples)} / {format_float_as_int_value(num_bytes)} KB] {format_float_value(total)} / {format_float_value(sum)} [{per_cpu_str}]")

        except KeyboardInterrupt:
            pass

def configure_arg_parser(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    parser = parser(description="Performance Monitor Script")
    parser.add_argument("--sample", help="sample interval in seconds", required=True, type=float)
    parser.add_argument("--binary_output", help="binary file to save data to", required=True)
    parser.add_argument("--display", help="display interval in seconds", required=False, type=float)
    parser.add_argument("--pid", help="optional process id to constrain stats to", required=False, type=int)
    parser.add_argument("--duration", help="stop recording after duration (if specified) ", required=False, type=float, default=999_999_999)
    return parser

def parse_args(parser: argparse.ArgumentParser) -> {}:
    return parser.parse_args()

def main(parser: argparse.ArgumentParser) -> None:
    args = parse_args(configure_arg_parser(parser))
    run(sample_interval=args.sample, display_interval=args.display, output=args.binary_output, duration=args.duration, pid=args.pid)

if __name__ == "__main__": \
    main(argparse.ArgumentParser)