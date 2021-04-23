Time efficiency
---------------

When building our package, we tried to keep an eye on the execution time
of our different functions. We use the package **time** to do so.

We noticed that the only thing that makes some of our function/classes long to
run, is the fact that we are using large data sets. Indeed, in order to
provide a visualization tool for the evolution of the *actual* Covid-19
pandemic, we need to make our function load data sets every time they are
called. We always need the updated version of the data, therefore we can't
just load them once for all.

It is no surprise that the slower functions are the one loading the larger
data sets.

We kept track of these execution times, and the below table is a summary of
this.

The table is given for execution time comparison **between** the
different functions. Time might differ according to computers, background
processes, and so on. These values have all been calculated on the same
machine, under the same conditions.

The execution time is also provided as a message in the terminal when running
any of **vizcodifr**'s functions.

============================  ==================
 function                      Execution time
============================  ==================
vacmap                        74.86038 s.
viz2Dmap                      21.74077 s.
viz3Dmap                      19.54393 s.
sparse_graph                  0.50041 s.
sparse_matrix                 0.43385 s.
regression.R2                 0.53918 s.
regression.poly_fit           0.42157 s.
regression.scatter_reg        0.35140 s.
vacdoses                      0.76860 s.
vactypedoses                  0.42227 s.
predict_curve                 0.53564 s.
bar_age                       0.16586 s.
bar_reg                       0.18026 s.
============================  ==================
