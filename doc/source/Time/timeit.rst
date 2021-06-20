Time efficiency
---------------

When building our package, we tried to keep an eye on the execution time
of our different functions. We use the package **time** to do so.

We noticed that the only thing that makes some of our function/classes long to
run, is the fact that we are using large datasets. Indeed, in order to
provide a visualization tool for the evolution of the *actual* Covid-19
pandemic, we need to make our function load datasets every time they are
called. We always need the updated version of the data, therefore we can't
just load them once for all.

It is no surprise that the slower functions are the one loading the larger
datasets.

We kept track of these execution times, and the below table is a summary of
this. The first column contains the name of the function, the second one contains
its execution time. Some of the functions load different datasets depending
on the chosen arguments, and in this case the execution times are given
from the fastest to the slowest. The third column contains the size of the
loaded dataset(s) written in the same order as they appear in the second column.

The table is given for execution time comparison **between** the
different functions. Time might differ according to computers, background
processes, and so on. These values have all been calculated on the same
machine, under the same conditions. Also note that datasets are growing with
time ; this time table was last edited on April 2021.

The execution time is also provided as a message in the terminal when running
any of **vizcovidfr**'s functions.

============================  ===============================  ===============================
 Function                      Execution time(s)                Size of the loaded dataset(s)
============================  ===============================  ===============================
vacmap                        74.86038 s.                      12.0MB
piechart                      from 2.62365 s. to 69.43795 s.   from 6.5MB to 12.0MB
viz2Dmap                      21.74077 s.                      6.79MB
viz3Dmap                      19.54393 s.                      6.79MB
transfer_map                  1.14778 s.                       1.79kB
sparse_graph                  0.50041 s.                       1.79kB
sparse_matrix                 0.43385 s.                       1.79kB
regression.R2                 2.04217 s.                       3.2MB
regression.poly_fit           2.34914 s.                       3.2MB
regression.scatter_reg        1.92033 s.                       3.2MB
vacdoses                      0.76860 s.                       2kB
vactypedoses                  0.42227 s.                       2kB
predict_curve                 2.69524 s.                       3.2MB
predict_value                 2.12597 s.                       3.2MB
bar_age                       1.41214 s.                       3.2MB
bar_reg                       1.55690 s.                       3.2MB
compareMF                     from 0.52738 s. to 2.04961 s.    from 228KB to 3.6MB
keytimeseries                 from 0.67941 s. to 3.18099 s.    from 25KB to 6.5MB
heatmap_age                   form 0.53875 s. to 2.09932 s.    from 3.3KB to 34KB
heatmap_reg_age               from 0.67732 s. to 1.75079 s.    from 491KB to 3.3KB
heatmap_reg_day               from 0.69503 s. to 1.66679 s.    from 401KB to 3.3KB
============================  ===============================  ===============================
