#!/usr/bin/env python
#
#  Copyright (c) 2013-2014 Bryce Adelstein-Lelbach
#
#  Distributed under the Boost Software License, Version 1.0. (See accompanying
#  file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)

from numpy import zeros 
from optparse import OptionParser

args = OptionParser(usage="%prog [file] [floor]").parse_args()[1]

# The input file.
file = args[0]

# This is the rho floor. It needs to be provided by the user on the command
# line (just copy and past the floor that the driver prints out during the run. 
# If other variables need to be floored to specific values, you'll need to add
# more command line arguments.
floor = float(args[1])

f = open(file, 'r')

# Global variables that records all the Cartesian coordinates in a particular
# dimension that are used for any point in the input. Our end goal is to 
# ensure that every combination of the coordinates used in the input 
# exist in the output (which makes the mesh uniform).
#
#   For all i in {x | (x, y) in input}
#       For all j in {y | (x, y) in input}
#           There exists (i, j)
#
x = {}
y = {}

# A lookup table that maps the Cartesian coordinates to the state variables.
master = {}

try:
    while True:
        # Each line in the input contains a set of floating point numbers,
        # separated by spaces, e.g.
        #
        #   0.1234 5.678 9.012

        # Parse the line. The variable 'line' is a python list. Each element of
        # the list is a string that represents a floating point number.
        line = f.next().split()

        # Convert the strings to values. 
        x_here = float(line[0])
        y_here = float(line[1])
        rho_here = float(line[2])
        tracker_here = float(line[3])

        # Record the Cartesian coordinates of this point (again, note that they
        # are tracked independently of each other.
        x[x_here] = 0
        y[y_here] = 0

        # Master tracks the points that exist in the input.
        master[(x_here, y_here)] = (rho_here, tracker_here)

except StopIteration:
    pass


# For all i in {x | (x, y) in input}
for i in sorted(x.iterkeys()):
    # For all j in {y | (x, y) in input}
    for j in sorted(y.iterkeys()):
        # Does (i, j) exist in the input?
        if (i, j) in master:
            # The third element we print, 0.0, is the z coordinate. We do this
            # so that we can treat the data as 3D data in GNUplot. You could,
            # however, artificially add the third dimension in GNUplot, e.g.
            #
            #   splot INPUT using 1:2:(0)
            #
            print i, j, 0.0, master[(i, j)][0], master[(i, j)][1]
        # If (i, j) doesn't exist, create an entry for it, setting the state to
        # the floor value.
        else:
            print i, j, 0.0, floor, floor

    print 

