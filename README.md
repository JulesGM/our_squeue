Uses [rich](https://rich.readthedocs.io/en/stable/introduction.html).[table](https://rich.readthedocs.io/en/stable/tables.html) to makes it easier to read what's going on with your SLURM jobs.

Just make `our_squeue.py` executable with `chmod +x` and add a symlink to in in a place that is in your `$PATH`, or add the folder that contains the script to your `$PATH` & create a symlink without the extension.

![Shows a table with the job names, their state in color, and their info in a table made with the Rich Python module.](demo.png)
