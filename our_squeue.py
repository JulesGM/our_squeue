#!/usr/bin/env python
# author: jules.gagnonm.alt@gmail.com.
​
​
import collections
import os
import subprocess
​
import rich
import rich.table
import rich.console
​
​
# Modify this to show different commands, or to change
# The order of commands, as `dict`s are ordered nowadays.
# The script could obviously be modified to accept an
# eg. json config with the commands to show.
SQUEUE_NAMES_TO_CODES = {
    "STATE": "%T",
    "NAME": "%j",
    "JOBID": "%i",
    "TRES_PER_NODE": "%b",
    "MIN_CPUS": "%c",
    "MIN_MEMORY": "%m",
    "RESERVATION": "%v",
    "NODELIST(REASON)": "%R",
}
​
​
COLOR_DICT = {"STATE": {"RUNNING": "green", "PENDING": "yellow", "default": "red"}}
​
​
def cmd(command):
    return subprocess.check_output(command).strip().decode().split("\n")
​
​
def get_info():
    """Call squeue for each command, parse the output.
    The first call to squeue is slow, the subsequent ones are very fast.
    This multi call approach allows us to have perfect parsing for
    extremely cheap. Things like comments, reasons and names can be otherwise
    tricky to parse correctly.
    """
    jobs = cmd(["squeue", "-u", os.environ["USER"], "-h", "-o", "%A"])
    outputs = collections.defaultdict(dict)
    for expected_name, code in SQUEUE_NAMES_TO_CODES.items():
        for job in jobs:
            cmd_output = cmd(
                ["squeue", "-u", os.environ["USER"], "-o", code, "--job", job]
            )
            if len(cmd_output) > 1:
                name = cmd_output[0]
                assert name == expected_name
                outputs[name][job] = cmd_output[1]
    return outputs, jobs
​
​
def main():
    ##########################################################################
    # Prepare the content.
    ##########################################################################
    parsed, jobs = get_info()
    columns = SQUEUE_NAMES_TO_CODES.keys()
    if parsed:
        assert SQUEUE_NAMES_TO_CODES.keys() == parsed.keys()
​
    ##########################################################################
    # Prepare the table.
    ##########################################################################
    table = rich.table.Table()
    for name in columns:
        table.add_column(name)
​
    for job_id in jobs:
        row = []
​
        for name in columns:
            content = parsed[name].get(job_id, "[empty]")
            if name in COLOR_DICT:
                if content in COLOR_DICT[name] or "default" in COLOR_DICT[name]:
                    color = COLOR_DICT[name].get(content, COLOR_DICT[name]["default"])
                    content = f"[{color}]" + content + "[/]"
            row.append(content)
​
        table.add_row(*row)
​
    ##########################################################################
    # Print it
    ##########################################################################
    console = rich.console.Console(force_terminal=True)
    console.print(table)
​
​
if __name__ == "__main__":
    main()
