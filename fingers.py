import adsk.core
import adsk.fusion
import traceback
import math

# * segment visuals

# !!! WE ARE WORKING ON XY PLANE AT THE BOTTOM
#                                                        width
#                                                        <--->
#                                                     _________
#                   | z   / y                        /        /|
#                   |    /                 length   /        / |
#                   |   /                          /        /  |  hight
#                   |  /                          /________/   |
#                   | /                           |        |   |
#    -x ____________|/____________                |        |   /
#                   |             x               |        |  /
#                  /|                             |        | /
#                 / |                             |________|/
#                /  |
#               /   |                          finger segment
#           -y /    | -z

# * segment indexes

##############################################################################
#                      finger section
#       ----------------------------------------------------------------
#      | index plus : index      : middle     : ring       : pinky      |
#      |            :            :            :            :            |
#      | [0][0]     : [1][0]     : [2][0]     : [3][0]     : [4][0]     |
#      |            :            :            :            :            |
#      |----------------------------------------------------------------|
#      |            :            : coordinate :            :            |
#      | [0][1]     : [1][1]     : origin     : [3][1]     : [4][1]     |
#      |            :            : [2][1]     :            :            |
#      |----------------------------------------------------------------|
#      |            :            :            :            :            |
#      | [0][2]     : [1][2]     : [2][2]     : [3][2]     : [4][2]     |
#      |            :            :            :            :            |
#       ----------------------------------------------------------------
# coordinate origine (0, 0, 0) is the finger section center,
# adjust finger segment locations accordingly.

# * helper functions


# convert to cm,
# native fusion api value for dimensions is cm (10mm)
def tocm(mm):
    return 0.1 * mm

# * general settings
###################general settings####################################### {{{

# all dimensions are in mm, convert to tocm() before using.
BASE_HIGHT = tocm(0)  # use to adjust the hight of all keyboard parts
FINGERS_SECTION_HIGHT = BASE_HIGHT + tocm(0)  # use to adjust the hight of fingers part
# FINGERS_SECTION_SHELL_THICKNESS = tocm(2)
FINGERS_SECTION_SHELL_THICKNESS = tocm(1.5)
SWITCH_LENGTH = tocm(14)
SWITCH_WIDTH = tocm(14)
# SWITCH_EXTRUDE_DISTANCE = -(FINGERS_SECTION_SHELL_THICKNESS + tocm(1))
SWITCH_EXTRUDE_DISTANCE = -tocm(5)

# settings for the column next to the left of index finger column.
INDEXPLUS_SECTION_SETTINGS = []
# settings for index finger column
INDEX_SECTION_SETTINGS = []
# settings for middle finger column
MIDDLE_SECTION_SETTINGS = []
# settings for ring finger column
RING_SECTION_SETTINGS = []
# settings for pinky finger column
PINKY_SECTION_SETTINGS = []
# multidimensional array containing lists for column segments.
# refer to the picture above for index referencing.
FINGER_SECTIONS_SETTINGS = [
    INDEXPLUS_SECTION_SETTINGS,
    INDEX_SECTION_SETTINGS,
    MIDDLE_SECTION_SETTINGS,
    RING_SECTION_SETTINGS,
    PINKY_SECTION_SETTINGS
]

# used to select a component where a combined body is placed
IDX_COMPONENT_WITH_COMPBINED_BODY = 7  # use section origin (mdl1 segment).
DOVE_TAIL_LOC_LEFT = tocm(-10)
DOVE_TAIL_LOC_RIGHT = tocm(30)
OFFSET_DOVE_TAIL_JOINT = tocm(.15)
DOVE_TAIL_HIGHT = tocm(25)
DOVE_TAIL_LENGTH = tocm(7)
DOVE_TAIL_WIDTH_BASE = tocm(12)
DOVE_TAIL_WIDTH_END = tocm(17)
# }}}

# * section settings

##########################################################################
##################### fingers section settings ###########################
########################################################################## {{{
mdl_row_width = tocm(20)
indx_row_width = tocm(20)
indxpls_width = tocm(20)
ring_row_width = tocm(20)
pinky_row_width = tocm(20)


# * mdl

############################################
################# mdl ###################### {{{2

# ** mdl0

################# mdl 0 #################### {{{3

# base dimensions
mdl0_width = mdl_row_width + tocm(1)
mdl0_length = tocm(22)
mdl0_hight = tocm(12)

# switch center: move away from geometric center by these values
mdl0_switch_center = (tocm(.5), tocm(1.5), tocm(0))

# switch surface:
# the incline magnitude
mdl0_surf_low = mdl0_hight
mdl0_surf_mdl = mdl0_surf_low + tocm(2)
mdl0_surf_high = mdl0_surf_low + tocm(10.5)

# the incline direction
# set three corners that would define surface angle.
mdl0_top_surf_corners = {
    "low": (mdl0_width / 2, -mdl0_length / 2, mdl0_surf_low),
    "mdl": (-mdl0_width / 2, -mdl0_length / 2, mdl0_surf_mdl),
    "high": (-mdl0_width / 2, mdl0_length / 2, mdl0_surf_high),
}

# use this for the rotation in the switch surface XY plane.
# positive values - anti clockwise
# negative values - clockwise
mdl0_switch_rotation_angle_deg = 0.5

# you do not need to touch these settings
mdl0_settings = {
    "name": "mdl0",
    "base_dimensions": {"width": mdl0_width, "length": mdl0_length, "hight": mdl0_hight},
    "switch_center": mdl0_switch_center,
    "top_surf_conners": mdl0_top_surf_corners,
    "switch_rotation_angle": mdl0_switch_rotation_angle_deg * math.pi / 180,
}
MIDDLE_SECTION_SETTINGS.append(mdl0_settings)
########################################## 3}}}

# ** mdl1

################# mdl 1 #################### {{{3

# base dimensions
mdl1_width = mdl_row_width
mdl1_length = tocm(19)
mdl1_hight = tocm(10)

# switch center: move away from geometric center by these values
mdl1_switch_center = (tocm(0), tocm(0.25), tocm(0))

# switch surface:
# the incline magnitude
mdl1_surf_low = mdl1_hight
mdl1_surf_mdl = mdl1_surf_low + tocm(1)
mdl1_surf_high = mdl1_surf_low + tocm(4)

# the incline direction
# set three corners that would define surface angle.
mdl1_top_surf_corners = {
    "low": (mdl1_width / 2, mdl1_length / 2, mdl1_surf_low),
    "mdl": (mdl1_width / 2, -mdl1_length / 2, mdl1_surf_mdl),
    "high": (-mdl1_width / 2, -mdl1_length / 2, mdl1_surf_high),
}

# use this for the rotation in the switch surface XY plane.
# positive values - anti clockwise
# negative values - clockwise
mdl1_switch_rotation_angle_deg = -2

# you do not need to touch these settings
mdl1_settings = {
    "name": "mdl1",
    "base_dimensions": {"width": mdl1_width, "length": mdl1_length, "hight": mdl1_hight},
    "switch_center": mdl1_switch_center,
    "top_surf_conners": mdl1_top_surf_corners,
    "switch_rotation_angle": mdl1_switch_rotation_angle_deg * math.pi / 180,
}
MIDDLE_SECTION_SETTINGS.append(mdl1_settings)
############################################ 3}}}

# ** mdl2

################# mdl 2 #################### {{{3

# base dimensions
mdl2_width = mdl_row_width
mdl2_length = tocm(22)
mdl2_hight = tocm(7)

# switch center will be transformed by these distances from base center
mdl2_switch_center = (tocm(-0.25), tocm(0), tocm(0))

# switch surface:
# the incline magnitude
mdl2_surf_low = mdl2_hight
mdl2_surf_mdl = mdl2_surf_low + tocm(1.5)
mdl2_surf_high = mdl2_surf_low + tocm(8.66)

# the incline direction
# set three corners that would define surface angle.
mdl2_top_surf_corners = {
    "low": (mdl2_width / 2, mdl2_length / 2, mdl2_surf_low),
    "mdl": (-mdl2_width / 2, mdl2_length / 2, mdl2_surf_mdl),
    "high": (-mdl2_width / 2, -mdl2_length / 2, mdl2_surf_high),
}

# use this for the rotation in the switch surface XY plane.
# positive values - anti clockwise
# negative values - clockwise
mdl2_switch_rotation_angle_deg = -3.0

# you do not need to touch these settings
mdl2_settings = {
    "name": "mdl2",
    "base_dimensions": {"width": mdl2_width, "length": mdl2_length, "hight": mdl2_hight},
    "switch_center": mdl2_switch_center,
    "top_surf_conners": mdl2_top_surf_corners,
    "switch_rotation_angle": mdl2_switch_rotation_angle_deg * math.pi / 180,
}
MIDDLE_SECTION_SETTINGS.append(mdl2_settings)
########################################## 3}}}

# ** mdl segment locations

############segment locations############### {{{3
mdl0 = MIDDLE_SECTION_SETTINGS[0]["base_dimensions"]
mdl1 = MIDDLE_SECTION_SETTINGS[1]["base_dimensions"]
mdl2 = MIDDLE_SECTION_SETTINGS[2]["base_dimensions"]
MIDDLE_SECTION_SETTINGS[0]["location"] = (
    # increase xcoord to shift it to the right
    tocm(0.5),
    mdl0["length"] / 2.0 + mdl1["length"] / 2.0,
    tocm(0.0)
)
MIDDLE_SECTION_SETTINGS[1]["location"] = (
    tocm(0.0),
    tocm(0.0),
    tocm(0.0))
MIDDLE_SECTION_SETTINGS[2]["location"] = (
    tocm(0.0),
    -(mdl2["length"] / 2.0 + mdl1["length"] / 2.0),
    tocm(0.0)
)
########################################## 3}}}
########################################## 2}}}

# * indx

############################################
################# indx ##################### {{{2

# ** indx0

################# indx 0 ################### {{{3

# base dimensions
indx0_width = indx_row_width
indx0_length = tocm(22)
indx0_hight = tocm(19)

# switch center: move away from geometric center by these values
indx0_switch_center = (tocm(2), tocm(-1), tocm(0))

# switch surface:
# the incline magnitude
indx0_surf_low = indx0_hight
indx0_surf_mdl = indx0_surf_low + tocm(5)
indx0_surf_high = indx0_surf_low + tocm(13)

# the incline direction
# set three corners that would define surface angle.
indx0_top_surf_corners = {
    "low": (indx0_width / 2, -indx0_length / 2, indx0_surf_low),
    "mdl": (-indx0_width / 2, -indx0_length / 2, indx0_surf_mdl),
    "high": (-indx0_width / 2, indx0_length / 2, indx0_surf_high),
}

# use this for the rotation in the switch surface XY plane.
# positive values - anti clockwise
# negative values - clockwise
indx0_switch_rotation_angle_deg = -2

# you do not need to touch these settings
indx0_settings = {
    "name": "indx0",
    "base_dimensions": {"width": indx0_width, "length": indx0_length, "hight": indx0_hight},
    "switch_center": indx0_switch_center,
    "top_surf_conners": indx0_top_surf_corners,
    "switch_rotation_angle": indx0_switch_rotation_angle_deg * math.pi / 180,
}
INDEX_SECTION_SETTINGS.append(indx0_settings)
########################################## 3}}}

# ** indx1

################# indx 1 ################### {{{3

# base dimensions
indx1_width = indx_row_width
indx1_length = tocm(19)
indx1_hight = tocm(14)

# switch center: move away from geometric center by these values
indx1_switch_center = (tocm(0), tocm(-0.75), tocm(0))

# switch surface:
# the incline magnitude
indx1_surf_low = indx1_hight
indx1_surf_mdl = indx1_surf_low + tocm(1)
indx1_surf_high = indx1_surf_low + tocm(9)

# the incline direction
# set three corners that would define surface angle.
indx1_top_surf_corners = {
    "low": (indx1_width / 2, indx1_length / 2, indx1_surf_low),
    "mdl": (indx1_width / 2, -indx1_length / 2, indx1_surf_mdl),
    "high": (-indx1_width / 2, -indx1_length / 2, indx1_surf_high),
}

# use this for the rotation in the switch surface XY plane.
# positive values - anti clockwise
# negative values - clockwise
indx1_switch_rotation_angle_deg = -2

# you do not need to touch these settings
indx1_settings = {
    "name": "indx1",
    "base_dimensions": {"width": indx1_width, "length": indx1_length, "hight": indx1_hight},
    "switch_center": indx1_switch_center,
    "top_surf_conners": indx1_top_surf_corners,
    "switch_rotation_angle": indx1_switch_rotation_angle_deg * math.pi / 180,
}
INDEX_SECTION_SETTINGS.append(indx1_settings)
############################################ 3}}}

# ** indx2

################# indx 2 ################### {{{3

# base dimensions
indx2_width = indx_row_width
indx2_length = tocm(22)
indx2_hight = tocm(10)

# switch center will be transformed by these distances from base center
indx2_switch_center = (tocm(0.25), tocm(-1.5), tocm(0))

# switch surface:
# the incline magnitude
indx2_surf_low = indx2_hight
indx2_surf_mdl = indx2_surf_low + tocm(5)
indx2_surf_high = indx2_surf_low + tocm(11.77)

# the incline direction
# set three corners that would define surface angle.
indx2_top_surf_corners = {
    "low": (indx2_width / 2, indx2_length / 2, indx2_surf_low),
    "mdl": (-indx2_width / 2, indx2_length / 2, indx2_surf_mdl),
    "high": (-indx2_width / 2, -indx2_length / 2, indx2_surf_high),
}

# use this for the rotation in the switch surface XY plane.
# positive values - anti clockwise
# negative values - clockwise
indx2_switch_rotation_angle_deg = 2.0

# you do not need to touch these settings
indx2_settings = {
    "name": "indx2",
    "base_dimensions": {"width": indx2_width, "length": indx2_length, "hight": indx2_hight},
    "switch_center": indx2_switch_center,
    "top_surf_conners": indx2_top_surf_corners,
    "switch_rotation_angle": indx2_switch_rotation_angle_deg * math.pi / 180,
}
INDEX_SECTION_SETTINGS.append(indx2_settings)
########################################## 3}}}

# ** indx segment locations

############segment locations############### {{{3
indx0 = INDEX_SECTION_SETTINGS[0]["base_dimensions"]
indx1 = INDEX_SECTION_SETTINGS[1]["base_dimensions"]
indx2 = INDEX_SECTION_SETTINGS[2]["base_dimensions"]
INDEX_SECTION_SETTINGS[0]["location"] = (
    -(indx0["width"] / 2.0 + mdl0["width"] / 2.0) + MIDDLE_SECTION_SETTINGS[0]["location"][0],
    indx0["length"] / 2.0 + indx1["length"] / 2.0,
    tocm(0)
)
INDEX_SECTION_SETTINGS[1]["location"] = (
    -(indx1["width"] / 2.0 + mdl1["width"] / 2.0) + MIDDLE_SECTION_SETTINGS[1]["location"][0],
    tocm(0),
    tocm(0)
)
INDEX_SECTION_SETTINGS[2]["location"] = (
    -(indx2["width"] / 2.0 + mdl2["width"] / 2.0) + MIDDLE_SECTION_SETTINGS[2]["location"][0],
    -(indx2["length"] / 2.0 + indx1["length"] / 2.0),
    tocm(0)
)
########################################## 3}}}

############################################ 2}}}

# * indxpls

############################################
############## indx plus ################### {{{2

# ** indxpls0

############## indxpls 0 ################# {{{3

# base dimensions
indxpls0_width = indxpls_width
indxpls0_length = tocm(24)
indxpls0_hight = tocm(27)

# switch center: move away from geometric center by these values
indxpls0_switch_center = (tocm(3), tocm(-2.5), tocm(0))

# switch surface:
# the incline magnitude
indxpls0_surf_low = indxpls0_hight
indxpls0_surf_mdl = indxpls0_surf_low + tocm(12)
indxpls0_surf_high = indxpls0_surf_low + tocm(17)

# the incline direction
# set three corners that would define surface angle.
indxpls0_top_surf_corners = {
    "low": (indxpls0_width / 2, -indxpls0_length / 2, indxpls0_surf_low),
    "mdl": (-indxpls0_width / 2, -indxpls0_length / 2, indxpls0_surf_mdl),
    "high": (-indxpls0_width / 2, indxpls0_length / 2, indxpls0_surf_high),
}

# use this for the rotation in the switch surface XY plane.
# positive values - anti clockwise
# negative values - clockwise
indxpls0_switch_rotation_angle_deg = -1.5

# you do not need to touch these settings
indxpls0_settings = {
    "name": "indxpls0",
    "base_dimensions": {"width": indxpls0_width, "length": indxpls0_length, "hight": indxpls0_hight},
    "switch_center": indxpls0_switch_center,
    "top_surf_conners": indxpls0_top_surf_corners,
    "switch_rotation_angle": indxpls0_switch_rotation_angle_deg * math.pi / 180,
}
INDEXPLUS_SECTION_SETTINGS.append(indxpls0_settings)
########################################## 3}}}

# ** indxpls1

############## indxpls 1 ################# {{{3

# base dimensions
indxpls1_width = indxpls_width
indxpls1_length = tocm(20)
indxpls1_hight = tocm(22)

# switch center: move away from geometric center by these values
indxpls1_switch_center = (tocm(2), tocm(0), tocm(0))

# switch surface:
# the incline magnitude
indxpls1_surf_low = indxpls1_hight
indxpls1_surf_mdl = indxpls1_surf_low + tocm(17)
indxpls1_surf_high = indxpls1_surf_low + tocm(17)

# the incline direction
# set three corners that would define surface angle.
indxpls1_top_surf_corners = {
    "low": (indxpls1_width / 2, -indxpls1_length / 2, indxpls1_surf_low),
    "mdl": (-indxpls1_width / 2, -indxpls1_length / 2, indxpls1_surf_mdl),
    "high": (-indxpls1_width / 2, indxpls1_length / 2, indxpls1_surf_high),
}

# use this for the rotation in the switch surface XY plane.
# positive values - anti clockwise
# negative values - clockwise
indxpls1_switch_rotation_angle_deg = 1

# you do not need to touch these settings
indxpls1_settings = {
    "name": "indxpls1",
    "base_dimensions": {"width": indxpls1_width, "length": indxpls1_length, "hight": indxpls1_hight},
    "switch_center": indxpls1_switch_center,
    "top_surf_conners": indxpls1_top_surf_corners,
    "switch_rotation_angle": indxpls1_switch_rotation_angle_deg * math.pi / 180,
}
INDEXPLUS_SECTION_SETTINGS.append(indxpls1_settings)
############################################ 3}}}

# ** indxpls2

############## indxpls 2 ################# {{{3

# base dimensions
indxpls2_width = indxpls_width
indxpls2_length = tocm(19)
indxpls2_hight = tocm(22)

# switch center will be transformed by these distances from base center
indxpls2_switch_center = (tocm(3), tocm(-0.5), tocm(0))

# switch surface:
# the incline magnitude
indxpls2_surf_low = indxpls2_hight
indxpls2_surf_mdl = indxpls2_surf_low + tocm(15)
indxpls2_surf_high = indxpls2_surf_low + tocm(18)

# the incline direction
# set three corners that would define surface angle.
indxpls2_top_surf_corners = {
    "low": (indxpls2_width / 2, indxpls2_length / 2, indxpls2_surf_low),
    "mdl": (-indxpls2_width / 2, indxpls2_length / 2, indxpls2_surf_mdl),
    "high": (-indxpls2_width / 2, -indxpls2_length / 2, indxpls2_surf_high),
}

# use this for the rotation in the switch surface XY plane.
# positive values - anti clockwise
# negative values - clockwise
indxpls2_switch_rotation_angle_deg = 2

# you do not need to touch these settings
indxpls2_settings = {
    "name": "indxpls2",
    "base_dimensions": {"width": indxpls2_width, "length": indxpls2_length, "hight": indxpls2_hight},
    "switch_center": indxpls2_switch_center,
    "top_surf_conners": indxpls2_top_surf_corners,
    "switch_rotation_angle": indxpls2_switch_rotation_angle_deg * math.pi / 180,
}
INDEXPLUS_SECTION_SETTINGS.append(indxpls2_settings)
########################################## 3}}}

# ** indxpls segment location

############segment locations############### {{{3
indxpls0 = INDEXPLUS_SECTION_SETTINGS[0]["base_dimensions"]
indxpls1 = INDEXPLUS_SECTION_SETTINGS[1]["base_dimensions"]
indxpls2 = INDEXPLUS_SECTION_SETTINGS[2]["base_dimensions"]
# the finger section is centered at mdl1 center,
# we need to adjust the indxpls locations to align with the rest.
indxpls_ycoord_adjustment = (mdl1["length"] / 2 + mdl0["length"]) - (indxpls1["length"] / 2.0 + indxpls0["length"])
INDEXPLUS_SECTION_SETTINGS[0]["location"] = (
    -(indxpls0["width"] / 2.0 + indx0["width"] / 2.0) + INDEX_SECTION_SETTINGS[0]["location"][0],
    indxpls0["length"] / 2.0 + indxpls1["length"] / 2.0 + indxpls_ycoord_adjustment,
    tocm(0)
)
INDEXPLUS_SECTION_SETTINGS[1]["location"] = (
    -(indxpls1["width"] / 2.0 + indx1["width"] / 2.0) + INDEX_SECTION_SETTINGS[1]["location"][0],
    tocm(0) + indxpls_ycoord_adjustment,
    tocm(0)
)
INDEXPLUS_SECTION_SETTINGS[2]["location"] = (
    -(indxpls2["width"] / 2.0 + indx2["width"] / 2.0) + INDEX_SECTION_SETTINGS[2]["location"][0],
    -(indxpls2["length"] / 2.0 + indxpls1["length"] / 2.0) + indxpls_ycoord_adjustment,
    tocm(0)
)
########################################## 3}}}

############################################ 2}}}

# * ring

############################################
################# ring ###################### {{{2

# ** ring0

################# ring 0 #################### {{{3

# base dimensions
ring0_width = ring_row_width - tocm(1)
ring0_length = tocm(22)
ring0_hight = tocm(13)

# switch center: move away from geometric center by these values
ring0_switch_center = (tocm(-0.75), tocm(-0.5), tocm(0))

# switch surface:
ring0_surf_low = ring0_hight
ring0_surf_mdl = ring0_surf_low + tocm(2)
ring0_surf_high = ring0_surf_low + tocm(12.5)

# the incline direction
# set three corners that would define surface angle.
ring0_top_surf_corners = {
    "low": (ring0_width / 2, -ring0_length / 2, ring0_surf_low),
    "mdl": (-ring0_width / 2, -ring0_length / 2, ring0_surf_mdl),
    "high": (-ring0_width / 2, ring0_length / 2, ring0_surf_high),
}

# use this for the rotation in the switch surface XY plane.
# positive values - anti clockwise
# negative values - clockwise
ring0_switch_rotation_angle_deg = -1

# you do not need to touch these settings
ring0_settings = {
    "name": "ring0",
    "base_dimensions": {"width": ring0_width, "length": ring0_length, "hight": ring0_hight},
    "switch_center": ring0_switch_center,
    "top_surf_conners": ring0_top_surf_corners,
    "switch_rotation_angle": ring0_switch_rotation_angle_deg * math.pi / 180,
}
RING_SECTION_SETTINGS.append(ring0_settings)
########################################## 3}}}

# ** ring1

################# ring 1 #################### {{{3

# base dimensions
ring1_width = ring_row_width
ring1_length = tocm(19)
ring1_hight = tocm(8)

# switch center: move away from geometric center by these values
ring1_switch_center = (tocm(-0.25), tocm(-1), tocm(0))

# switch surface:
# the incline magnitude
ring1_surf_low = ring1_hight
ring1_surf_mdl = ring1_surf_low + tocm(1)
ring1_surf_high = ring1_surf_low + tocm(5)

# the incline direction
# set three corners that would define surface angle.
ring1_top_surf_corners = {
    "low": (ring1_width / 2, ring1_length / 2, ring1_surf_low),
    "mdl": (ring1_width / 2, -ring1_length / 2, ring1_surf_mdl),
    "high": (-ring1_width / 2, -ring1_length / 2, ring1_surf_high),
}

# use this for the rotation in the switch surface XY plane.
# positive values - anti clockwise
# negative values - clockwise
ring1_switch_rotation_angle_deg = 0

# you do not need to touch these settings
ring1_settings = {
    "name": "ring1",
    "base_dimensions": {"width": ring1_width, "length": ring1_length, "hight": ring1_hight},
    "switch_center": ring1_switch_center,
    "top_surf_conners": ring1_top_surf_corners,
    "switch_rotation_angle": ring1_switch_rotation_angle_deg * math.pi / 180,
}
RING_SECTION_SETTINGS.append(ring1_settings)
############################################ 3}}}

# ** ring2

################# ring 2 #################### {{{3

# base dimensions
ring2_width = ring_row_width
ring2_length = tocm(22)
ring2_hight = tocm(6)

# switch center will be transformed by these distances from base center
ring2_switch_center = (tocm(-0.5), tocm(-1.25), tocm(0))

# switch surface:
# the incline magnitude
ring2_surf_low = ring2_hight
ring2_surf_mdl = ring2_surf_low + tocm(1.5)
ring2_surf_high = ring2_surf_low + tocm(10.4)

# the incline direction
# set three corners that would define surface angle.
ring2_top_surf_corners = {
    "low": (ring2_width / 2, ring2_length / 2, ring2_surf_low),
    "mdl": (-ring2_width / 2, ring2_length / 2, ring2_surf_mdl),
    "high": (-ring2_width / 2, -ring2_length / 2, ring2_surf_high),
}

# use this for the rotation in the switch surface XY plane.
# positive values - anti clockwise
# negative values - clockwise
ring2_switch_rotation_angle_deg = -3.5

# you do not need to touch these settings
ring2_settings = {
    "name": "ring2",
    "base_dimensions": {"width": ring2_width,
                        "length": ring2_length,
                        "hight": ring2_hight},
    "switch_center": ring2_switch_center,
    "top_surf_conners": ring2_top_surf_corners,
    "switch_rotation_angle": ring2_switch_rotation_angle_deg * math.pi / 180,
}
RING_SECTION_SETTINGS.append(ring2_settings)
########################################## 3}}}

# ** ring segment locations

############segment locations############### {{{3
ring0 = RING_SECTION_SETTINGS[0]["base_dimensions"]
ring1 = RING_SECTION_SETTINGS[1]["base_dimensions"]
ring2 = RING_SECTION_SETTINGS[2]["base_dimensions"]
RING_SECTION_SETTINGS[0]["location"] = (
    ring0["width"] / 2.0 + mdl0["width"] / 2.0 + MIDDLE_SECTION_SETTINGS[0]["location"][0],
    ring0["length"] / 2.0 + ring1["length"] / 2.0,
    tocm(0)
)
RING_SECTION_SETTINGS[1]["location"] = (
    ring1["width"] / 2.0 + mdl1["width"] / 2.0 + MIDDLE_SECTION_SETTINGS[1]["location"][0],
    tocm(0),
    tocm(0),
)
RING_SECTION_SETTINGS[2]["location"] = (
    ring2["width"] / 2.0 + mdl2["width"] / 2.0 + MIDDLE_SECTION_SETTINGS[2]["location"][0],
    -(ring2["length"] / 2.0 + ring1["length"] / 2.0),
    tocm(0)
)
########################################## 3}}}
########################################## 2}}}

# * pinky

############################################
################# pinky ###################### {{{2

# ** pinky0

################# pinky 0 #################### {{{3

# base dimensions
pinky0_width = pinky_row_width
pinky0_length = tocm(18)
pinky0_hight = tocm(22.4)

# switch center: move away from geometric center by these values
pinky0_switch_center = (tocm(-1), tocm(-1.5), tocm(0))

# switch surface:
pinky0_surf_low = pinky0_hight
pinky0_surf_mdl = pinky0_surf_low + tocm(11.25)
pinky0_surf_high = pinky0_surf_low + tocm(11.25)

# the incline direction
# set three corners that would define surface angle.
pinky0_top_surf_corners = {
    "low": (pinky0_width / 2, -pinky0_length / 2, pinky0_surf_low),
    "mdl": (pinky0_width / 2, pinky0_length / 2, pinky0_surf_mdl),
    "high": (-pinky0_width / 2, pinky0_length / 2, pinky0_surf_high),
}

# use this for the rotation in the switch surface XY plane.
# positive values - anti clockwise
# negative values - clockwise
pinky0_switch_rotation_angle_deg = 0

# you do not need to touch these settings
pinky0_settings = {
    "name": "pinky0",
    "base_dimensions": {"width": pinky0_width, "length": pinky0_length, "hight": pinky0_hight},
    "switch_center": pinky0_switch_center,
    "top_surf_conners": pinky0_top_surf_corners,
    "switch_rotation_angle": pinky0_switch_rotation_angle_deg * math.pi / 180,
}
PINKY_SECTION_SETTINGS.append(pinky0_settings)
########################################## 3}}}

# ** pinky1

################# pinky 1 #################### {{{3

# base dimensions
pinky1_width = pinky_row_width
pinky1_length = tocm(22)
pinky1_hight = tocm(15)

# switch center: move away from geometric center by these values
pinky1_switch_center = (tocm(-1), tocm(-2), tocm(0))

# switch surface:
# the incline magnitude
pinky1_surf_low = pinky1_hight
pinky1_surf_mdl = pinky1_surf_low + tocm(1)
pinky1_surf_high = pinky1_surf_low + tocm(1)

# the incline direction
# set three corners that would define surface angle.
pinky1_top_surf_corners = {
    "low": (pinky1_width / 2, -pinky1_length / 2, pinky1_surf_low),
    "mdl": (-pinky1_width / 2, -pinky1_length / 2, pinky1_surf_mdl),
    "high": (-pinky1_width / 2, pinky1_length / 2, pinky1_surf_high),
}

# use this for the rotation in the switch surface XY plane.
# positive values - anti clockwise
# negative values - clockwise
pinky1_switch_rotation_angle_deg = 0

# you do not need to touch these settings
pinky1_settings = {
    "name": "pinky1",
    "base_dimensions": {"width": pinky1_width, "length": pinky1_length, "hight": pinky1_hight},
    "switch_center": pinky1_switch_center,
    "top_surf_conners": pinky1_top_surf_corners,
    "switch_rotation_angle": pinky1_switch_rotation_angle_deg * math.pi / 180,
}
PINKY_SECTION_SETTINGS.append(pinky1_settings)
############################################ 3}}}

# ** pinky2

################# pinky 2 #################### {{{3

# base dimensions
pinky2_width = pinky_row_width
pinky2_length = tocm(24)
pinky2_hight = tocm(8)

# switch center will be transformed by these distances from base center
pinky2_switch_center = (tocm(-1), tocm(-2.5), tocm(0))

# switch surface:
# the incline magnitude
pinky2_surf_low = pinky2_hight
pinky2_surf_mdl = pinky2_surf_low + tocm(12)
pinky2_surf_high = pinky2_surf_low + tocm(15)

# the incline direction
# set three corners that would define surface angle.
pinky2_top_surf_corners = {
    "low": (pinky2_width / 2, pinky2_length / 2, pinky2_surf_low),
    "mdl": (pinky2_width / 2, -pinky2_length / 2, pinky2_surf_mdl),
    "high": (-pinky2_width / 2, -pinky2_length / 2, pinky2_surf_high),
}

# use this for the rotation in the switch surface XY plane.
# positive values - anti clockwise
# negative values - clockwise
pinky2_switch_rotation_angle_deg = 1

# you do not need to touch these settings
pinky2_settings = {
    "name": "pinky2",
    "base_dimensions": {"width": pinky2_width, "length": pinky2_length, "hight": pinky2_hight},
    "switch_center": pinky2_switch_center,
    "top_surf_conners": pinky2_top_surf_corners,
    "switch_rotation_angle": pinky2_switch_rotation_angle_deg * math.pi / 180,
}
PINKY_SECTION_SETTINGS.append(pinky2_settings)
########################################## 3}}}

# ** pinky segment locations

############segment locations############### {{{3
pinky0 = PINKY_SECTION_SETTINGS[0]["base_dimensions"]
pinky1 = PINKY_SECTION_SETTINGS[1]["base_dimensions"]
pinky2 = PINKY_SECTION_SETTINGS[2]["base_dimensions"]
# the finger section is centered at mdl1 center,
# we need to adjust the ycoord locations to align with the rest.
pinky_ycoord_adjustment = (mdl1["length"] / 2 + mdl0["length"]) - (pinky1["length"] / 2.0 + pinky0["length"]) - tocm(13)
PINKY_SECTION_SETTINGS[0]["location"] = (
    pinky0["width"] / 2.0 + ring0["width"] / 2.0 + RING_SECTION_SETTINGS[0]["location"][0],
    pinky0["length"] / 2.0 + pinky1["length"] / 2.0 + pinky_ycoord_adjustment,
    tocm(0)
)
PINKY_SECTION_SETTINGS[1]["location"] = (
    pinky1["width"] / 2.0 + ring1["width"] / 2.0 + RING_SECTION_SETTINGS[1]["location"][0],
    tocm(0) + pinky_ycoord_adjustment,
    tocm(0),
)
PINKY_SECTION_SETTINGS[2]["location"] = (
    pinky2["width"] / 2.0 + ring2["width"] / 2.0 + RING_SECTION_SETTINGS[2]["location"][0],
    -(pinky2["length"] / 2.0 + pinky1["length"] / 2.0) + pinky_ycoord_adjustment,
    tocm(0)
)
########################################## 3}}}
########################################## 2}}}

########################################### }}}


# * functions

def add_finger_segment(comp, settings, ui):  # {{{
    comp.name = settings["name"]
    # Create a new sketch on the xy plane.
    sketches = comp.sketches
    xyPlane = comp.xYConstructionPlane
    base_sketch = sketches.add(xyPlane)

    # sketch the base
    base_center = (tocm(0), tocm(0), tocm(0))
    base_corner = (
        settings["base_dimensions"]["width"] / 2,
        settings["base_dimensions"]["length"] / 2,
        tocm(0))
    lines = base_sketch.sketchCurves.sketchLines
    lines.addCenterPointRectangle(
        adsk.core.Point3D.create(*base_center),
        adsk.core.Point3D.create(*base_corner),
    )

    # Get construction planes
    planes = comp.constructionPlanes
    # Create construction plane input
    planeInput = planes.createInput()
    # Create three sketch points
    sketchPoints = base_sketch.sketchPoints
    # Add construction plane by three points
    planeInput.setByThreePoints(
        sketchPoints.add(adsk.core.Point3D.create(*settings["top_surf_conners"]["low"])),
        sketchPoints.add(adsk.core.Point3D.create(*settings["top_surf_conners"]["mdl"])),
        sketchPoints.add(adsk.core.Point3D.create(*settings["top_surf_conners"]["high"])),
    )
    switch_surf = planes.add(planeInput)
    # Get the health state of the plane
    # health = switch_surf.healthState
    # if health == adsk.fusion.FeatureHealthStates.ErrorFeatureHealthState or health == adsk.fusion.FeatureHealthStates.WarningFeatureHealthState:
    #     message = switch_surf.errorOrWarningMessage
    #     ui.messageBox('Failed:\n{}'.format(message))

    base_prof = base_sketch.profiles.item(0)
    # Create an extrusion input
    extrudes = comp.features.extrudeFeatures
    extInput = extrudes.createInput(base_prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    # the setting is referencing the 'z' coordinate of the highest corner
    distance = adsk.core.ValueInput.createByReal(settings["top_surf_conners"]["high"][2])
    extInput.setDistanceExtent(False, distance)

    # Set the extrude to be a solid one
    extInput.isSolid = True
    extrude = extrudes.add(extInput)

    # Get the body created by the extrusion
    base_body = extrude.bodies.item(0)

    # Create SplitBodyFeatureInput
    splitBodyFeats = comp.features.splitBodyFeatures
    splitBodyInput = splitBodyFeats.createInput(base_body, switch_surf, True)

    # Create split body feature
    splitBodyFeats.add(splitBodyInput)

    # select the correct body - the one that contains the base_corner
    split_body_idx = 0
    for idx, spb in enumerate(comp.bRepBodies):
        for v in spb.vertices:
            if v.geometry.isEqualTo(adsk.core.Point3D.create(*base_corner)):
                bottom_split_body = spb
                split_body_idx = idx
                break
        if split_body_idx != 0:
            break
    bs = [x for i, x in enumerate(comp.bRepBodies) if i != split_body_idx]
    for b in bs:
        b.deleteMe()
    #ui.messageBox('body:\n{}'.format(dir(bottom_split_body)))
    bottom_split_body.name = "{}_bottom".format(settings["name"])

    # select the correct face - the one that contains the opposite corners of
    # the swith surface
    face_idx = 0
    for idx, f in enumerate(bottom_split_body.faces):
        for v in f.vertices:
            if v.geometry.isEqualTo(adsk.core.Point3D.create(*settings["top_surf_conners"]["high"])):
                for v in f.vertices:
                    if v.geometry.isEqualTo(adsk.core.Point3D.create(*settings["top_surf_conners"]["low"])):
                        face = f
                        face_idx = idx
                        break
            if face_idx != 0:
                break
        if face_idx != 0:
            break

    # Create a point straight above the base center on the switch surface.
    # We need it as a reference to the switch location

    # Get construction points
    constructionPoints = comp.constructionPoints

    # Create construction point input
    pointInput = constructionPoints.createInput()

    # Create construction point by three planes
    pointInput.setByThreePlanes(comp.xZConstructionPlane,
                                comp.yZConstructionPlane, face)
    cp = constructionPoints.add(pointInput)

    # new_sketch = target_face.body.parentComponent.sketches.add(target_face)
    # new_sketch.project(target_face)
    sketch_switch = sketches.add(face)
    sketch_switch.project(cp)
    switch_surface_center = sketch_switch.sketchPoints.item(sketch_switch.sketchPoints.count - 1).geometry
    switch_center = (
        switch_surface_center.x + settings["switch_center"][0],
        switch_surface_center.y + settings["switch_center"][1],
        switch_surface_center.z + settings["switch_center"][2],
    )
    switch_corner = (
        switch_center[0] + SWITCH_WIDTH / 2,
        switch_center[1] + SWITCH_LENGTH / 2,
        switch_center[2]
    )

    lines = sketch_switch.sketchCurves.sketchLines
    lines.addCenterPointRectangle(
        adsk.core.Point3D.create(*switch_center),
        adsk.core.Point3D.create(*switch_corner)
    )

    # rotate the sketch
    all = adsk.core.ObjectCollection.create()
    for c in sketch_switch.sketchCurves:
        all.add(c)
    for p in sketch_switch.sketchPoints:
        all.add(p)
    # normal = sketch_switch.xDirection.crossProduct(sketch_switch.yDirection)
    # normal.transformBy(sketch_switch.transform)
    rotation_axis = adsk.core.Vector3D.create(0, 0, 1)
    # origin = sketch_switch.origin
    # origin.transformBy(sketch_switch.transform)
    rotation_origin = adsk.core.Point3D.create(*switch_center)
    mat = adsk.core.Matrix3D.create()
    # mat.setToRotation(1, normal, rotation_origin)
    mat.setToRotation(settings["switch_rotation_angle"], rotation_axis, rotation_origin)
    sketch_switch.move(all, mat)

    comp.isConstructionFolderLightBulbOn = False

    # # move the base to its location in the fingers section. {{{2
    # if settings["location"]:
    #     move_bodies = adsk.core.ObjectCollection.create()
    #     for b in comp.bRepBodies:
    #         move_bodies.add(b)
    #     # Create a transform to do move
    #     # ui.messageBox('loc:\n{}'.format(settings["location"]))
    #     vector = adsk.core.Vector3D.create(*settings["location"])
    #     transform_bodies = adsk.core.Matrix3D.create()
    #     transform_bodies.translation = vector

    #     # Create a move feature
    #     moveFeats = comp.features.moveFeatures
    #     moveFeatureInput = moveFeats.createInput(move_bodies, transform_bodies)
    #     moveFeats.add(moveFeatureInput)
    #     # Create a transform to do move
    #     # rotation_origin = cp.geometry
    #     # transform = adsk.core.Matrix3D.create()
    #     # # success = transform.setToRotation(MDL2_SWITCH_ROTATION_ANGLE_RAD, rotation_axis, rotation_origin)

    #     for sk in sketches:
    #         # transition the sketches
    #         all = adsk.core.ObjectCollection.create()
    #         for c in sk.sketchCurves:
    #             all.add(c)
    #         for p in sketch_switch.sketchPoints:
    #             all.add(p)
    #         # normal = sk.xDirection.crossProduct(sk.yDirection)
    #         # normal.transformBy(sk.transform)
    #         rotation_axis = adsk.core.Vector3D.create(0, 0, 1)
    #         # origin = sk.origin
    #         # origin.transformBy(sk.transform)
    #         # rotation_origin = adsk.core.Point3D.create(*switch_center)
    #         vector = adsk.core.Vector3D.create(*settings["location"])
    #         mat = adsk.core.Matrix3D.create()
    #         mat.translation = vector
    #         # transform_bodies = adsk.core.Matrix3D.create()
    #         # transform_bodies.translation = vector
    #         # mat.setToRotation(1, normal, rotation_origin)
    #         # mat.setToRotation(settings["switch_rotation_angle"], rotation_axis, rotation_origin)
    #         sk.move(all, mat)
    #         # 2}}}

    # # Create a move feature
    # moveFeats = comp.features.moveFeatures
    # moveFeatureInput = moveFeats.createInput(move_bodies, transform)
    # moveFeats.add(moveFeatureInput)
# }}}


def combine(rootComp, ui):  # {{{
    combineFeatures = rootComp.features.combineFeatures
    toolBodies = adsk.core.ObjectCollection.create()
    occs = rootComp.occurrences
    for idx, comp in enumerate(occs):
        comp = comp.component
        if idx == IDX_COMPONENT_WITH_COMPBINED_BODY:
            for b in comp.bRepBodies:
                if comp.name in b.name:
                    targetBody = b
                    # ui.messageBox('targetBody name:\n{}'.format(b.name))
        else:
            for b in comp.bRepBodies:
                if comp.name in b.name:
                    # ui.messageBox('toolBodies name:\n{}'.format(b.name))
                    toolBodies.add(b)

    combineInput = combineFeatures.createInput(targetBody, toolBodies)
    # combineInput.operation = adsk.fusion.FeatureOperations.CutFeatureOperation
    combineInput.operation = adsk.fusion.FeatureOperations.JoinFeatureOperation
    combineInput.isKeepToolBodies = False
    combineFeatures.add(combineInput)
#  }}}


# shell the body, must contain a named body which will be shelled.
def shell(rootComp, ui):  # {{{
    # get the comp containing the target body
    occs = rootComp.occurrences
    comp = occs.item(IDX_COMPONENT_WITH_COMPBINED_BODY).component

    # Create a collection of entities to shell
    entities = adsk.core.ObjectCollection.create()
    # get the target body: the one with correct name
    for b in comp.bRepBodies:
        if comp.name in b.name:
            body = b

    # get the target face: the one with vertices on XY plane.
    for f in body.faces:
        # the opposite ends lie on XY plane: Z coord is zero
        if f.vertices.item(0).geometry.z == 0.0 and f.vertices.item(1).geometry.z == 0.0:
            face = f
    entities.add(face)

    # Create a shell feature
    shellFeats = comp.features.shellFeatures
    isTangentChain = False
    shellFeatureInput = shellFeats.createInput(entities, isTangentChain)
    thickness = adsk.core.ValueInput.createByReal(FINGERS_SECTION_SHELL_THICKNESS)
    shellFeatureInput.insideThickness = thickness
    shellFeats.add(shellFeatureInput)
# }}}

# cut holes through switch surface for switches to sit in.
def cut_switch_holes(rootComp, ui):  # {{{
    occs = rootComp.occurrences

    # Create a collection of switch sketches
    # switch_profs = adsk.core.ObjectCollection.create()
    distance = adsk.core.ValueInput.createByReal(SWITCH_EXTRUDE_DISTANCE)

    # get switch sketches
    for occ in occs:
        comp = occ.component
        for sk in comp.sketches:
            extrudes = comp.features.extrudeFeatures
            # select the surface whose vertices do not lie in XY plane
            if sk.sketchPoints.item(0).worldGeometry.z != 0.0:
                prof = sk.profiles.item(sk.profiles.count - 1)
                extInput_switch = extrudes.createInput(prof, adsk.fusion.FeatureOperations.CutFeatureOperation)
                extInput_switch.setDistanceExtent(False, distance)
                extrudes.add(extInput_switch)
# }}}


# offset the bottom surface edges. The created profile is used to cut
# the receiving part of the dove tail joint.
def offset(rootComp, ui):  # {{{
    occs = rootComp.occurrences
    comp = occs.item(IDX_COMPONENT_WITH_COMPBINED_BODY).component
    for b in comp.bRepBodies:
        if comp.name in b.name:
            targetBody = b
            # find the bottom face to get the front y coord (the least value).
            for f in b.faces:
                if f.vertices.count == 4:
                    if f.vertices.item(0).geometry.z == 0.0 and f.vertices.item(2).geometry.z == 0.0:
                        face = f

#     # Create input entities for offset feature
#     inputEntities = adsk.core.ObjectCollection.create()
#     targetBody.isSolid = False
#     inputEntities.add(targetBody)
#     # Distance for offset feature
#     distance = adsk.core.ValueInput.createByReal(OFFSET_DOVE_TAIL_JOINT)
#     # Create an input for offset feature
#     offsetFeatures = comp.features.offsetFeatures
#     offsetInput = offsetFeatures.createInput(inputEntities, distance, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
#     # Create the offset feature
#     offsetFeatures.add(offsetInput)
#     targetBody.isSolid = True

    sketch_comp = comp
    for b in comp.bRepBodies:
        if sketch_comp.name in b.name:
            for f in b.faces:
                if f.vertices.item(0).geometry.z == 0.0 and f.vertices.item(2).geometry.z == 0.0:
                    face = f
    sketches = sketch_comp.sketches
    sketch_offset = sketches.add(sketch_comp.xYConstructionPlane)
    sketch_offset.project(face)
    # collect all curves in the sketch
    curves = adsk.core.ObjectCollection.create()
    for c in sketch_offset.sketchCurves:
        curves.add(c)
    # Create the offset.
    dirPoint = adsk.core.Point3D.create(0, 0, 0)
    sketch_offset.offset(curves, dirPoint, -OFFSET_DOVE_TAIL_JOINT)
    return

    # collect sketch profiles
    profs = adsk.core.ObjectCollection.create()
    for prof in sketch_offset.profiles:
        profs.add(prof)
    extrudes = sketch_comp.features.extrudeFeatures
    extInput = extrudes.createInput(profs, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    distance = adsk.core.ValueInput.createByReal(tocm(30))
    extInput.setDistanceExtent(False, distance)

    extrude = extrudes.add(extInput)
    # Get the body created by the extrusion
    extrude_body = extrude.bodies.item(0)

    combineFeatures = rootComp.features.combineFeatures
    toolBodies = adsk.core.ObjectCollection.create()
    toolBodies.add(extrude_body)

    combineInput = combineFeatures.createInput(targetBody, toolBodies)
    combineInput.operation = adsk.fusion.FeatureOperations.CutFeatureOperation
    combineInput.isKeepToolBodies = False
    combineFeatures.add(combineInput)
    sketch_offset.deleteMe()
# }}}


def run(context):  # {{{
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface

        # doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
        app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)
        # disable history timeline capture
        design.designType = adsk.fusion.DesignTypes.DirectDesignType

        # Get the root component of the active design.
        rootComp = design.rootComponent

        allOccs = rootComp.occurrences
        for finger_column in FINGER_SECTIONS_SETTINGS:
            for segment_settings in finger_column:
                # if segment_settings["name"] == "mdl1":
                # if "indx" in segment_settings["name"]:
                # if "mdl" in segment_settings["name"]:
                vector = adsk.core.Vector3D.create(*segment_settings["location"])
                transform = adsk.core.Matrix3D.create()
                transform.translation = vector
                # Create a component under root component
                occ = allOccs.addNewComponent(transform)
                subComp = occ.component
                # print(subComp.revisionId)
                add_finger_segment(subComp, segment_settings, ui)
        combine(rootComp, ui)
        # offset(rootComp, ui)
        shell(rootComp, ui)
        cut_switch_holes(rootComp, ui)
    except Exception as e:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
            print(e)
# }}}
