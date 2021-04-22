"""
3D maps
========
"""

########################################
# hospitalization, resuscitation, deaths
# --------------------------------------
# One way to compare these criterion between French departments and regions
# is to use the **viz3Dmap** function with the desired arguments, like so:

from vizcovidfr.maps import maps
maps.viz3Dmap(granularity='departement', criterion='hospitalises',
              file_path='', color=[255, 165, 0, 80])
