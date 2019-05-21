import adsk.core
import adsk.fusion
import traceback
import math

# !!! WE ARE WORKING ON XY PLANE AT THE BOTTOM
#
#
#                   | z   / y
#                   |    /
#                   |   /
#                   |  /
#                   | /
#    -x ____________|/____________
#                   |             x
#                  /|
#                 / |
#                /  |
#               /   |
#           -y /    | -z
#                                               width
#                                        ______________________________
#                                       /                             /|
#                               _______/                             / |
#                              /      /                             /  |
#                      _______/      /_____________________________/   | hight
#                     /      /       |                             |   |
#             _______/      /________|                             |   |
#            /      /       |        |                             |   |
#   length  /      /________|        |                             |   /
#          /       |        |        |                             |  /
#         /________|        |        |                             | /
#         |________|________|________|_____________________________|/
#
##############################################################################
#                      thumb section
#       -------------------------------------------------------------------
#      |            :            :             |    thumb base segment.    |
#      |            :            :             |   align its coord origin  |
#      | [0][0]     : [1][0]     : [2][0]      |  [3][0]                   |
#      |            :            :             |   with the finger coord   |
#      |            :            :             |        origin             |
#       -------------------------------------------------------------------


# convert to cm,
# native fusion api value for dimensions is cm (10mm)
def tocm(mm):
    return 0.1 * mm


################## general settings ###################################### {{{

# all dimensions are in mm, convert to tocm() before using.
BASE_HIGHT = tocm(0)  # use to adjust the hight of all keyboard parts
THUMB_SECTION_HIGHT = BASE_HIGHT + tocm(-25)  # use to adjust the hight of fingers part
# THUMB_SECTION_SHELL_THICKNESS = tocm(2)
THUMB_SECTION_SHELL_THICKNESS = tocm(1.5)
SWITCH_LENGTH = tocm(14)
SWITCH_WIDTH = tocm(14)
# SWITCH_EXTRUDE_DISTANCE = -(THUMB_SECTION_SHELL_THICKNESS + tocm(1))
SWITCH_EXTRUDE_DISTANCE = -tocm(6)

# thumb switch at [0][0] position (refer to the picture above)
THUMB_OUTER_SECTION_SETTINGS = []
# thumb switch at [1][0] position (refer to the picture above)
THUMB_MIDDLE_SECTION_SETTINGS = []
# thumb switch at [2][0] position (refer to the picture above)
THUMB_INNER_SECTION_SETTINGS = []
# thumb switch at [3][0] position (refer to the picture above)
THUMB_BASE_SECTION_SETTINGS = []
# multidimensional array containing lists for column segments.
# refer to the picture above for index referencing.
THUMB_SECTIONS_SETTINGS = [
    THUMB_OUTER_SECTION_SETTINGS,
    THUMB_MIDDLE_SECTION_SETTINGS,
    THUMB_INNER_SECTION_SETTINGS,
    THUMB_BASE_SECTION_SETTINGS
]

# used to select a component where a combined body is placed
IDX_COMPONENT_WITH_COMPBINED_BODY = 0
# adjust for tighter or looser joint
OFFSET_DOVE_TAIL_JOINT = tocm(.1)
DOVE_TAIL_LENGTH = tocm(7)
DOVE_TAIL_WIDTH_BASE = tocm(12)
DOVE_TAIL_WIDTH_END = tocm(17)
########################################################################## }}}

##########################################################################
##################### thumb section settings #############################
########################################################################## {{{
outer_segment_width = tocm(24)
middle_segment_width = tocm(19)
inner_segment_width = tocm(20)
base_segment_width = tocm(98)
base0_length = tocm(58)
# adjust_xcoord_relative_to_fingers_section = tocm(12)
adjust_xcoord_for_base = tocm(9)
adjust_ycoord_for_base = tocm(22.5) - (base0_length / 2)
adjust_xcoord_relative_to_fingers_section = tocm(19)
xcoord_inner0 = inner_segment_width / 2 + tocm(45)
adjust_ycoord_relative_to_fingers_section = tocm(-12)

############################################
################# base ##################### {{{2

################# base 0 ################### {{{3

# base dimensions
base0_width = base_segment_width
base0_hight = tocm(34)

# top surface incline:
base0_surf_low = base0_hight
base0_surf_mdl = base0_surf_low + tocm(0)
base0_surf_high = base0_surf_low + tocm(0)

# the incline direction
# set three corners that would define surface angle.
base0_top_surf_corners = {
    "low": (base0_width / 2, -base0_length / 2, base0_surf_low),
    "mdl": (-base0_width / 2, -base0_length / 2, base0_surf_mdl),
    "high": (-base0_width / 2, base0_length / 2, base0_surf_high),
}

# you do not need to touch these settings
base0_settings = {
    "name": "base0",
    "switch_center": (),  # there is no swith here
    "base_dimensions": {"width": base0_width, "length": base0_length, "hight": base0_hight},
    "top_surf_conners": base0_top_surf_corners,
    "body_rotation_angle": 0,
}
THUMB_BASE_SECTION_SETTINGS.append(base0_settings)
########################################## 3}}}

############segment locations############### {{{3
THUMB_BASE_SECTION_SETTINGS[0]["location"] = (
    adjust_xcoord_for_base,
    adjust_ycoord_for_base,
    tocm(0)
)
########################################## 3}}}

############################################ 2}}}


############################################
################# inner #################### {{{2

################# inner 0 ################## {{{3

# base dimensions
inner0_width = inner_segment_width
# inner0_length = tocm(38)
inner0_length = tocm(33)
# inner0_length = tocm(28)
inner0_hight = THUMB_SECTION_HIGHT + tocm(35)

# switch center
inner0_switch_center = (tocm(0), tocm(5), tocm(0))

# switch surface:
# the incline magnitude
inner0_surf_low = inner0_hight
inner0_surf_mdl = inner0_surf_low + tocm(19)
inner0_surf_high = inner0_surf_low + tocm(24)

# the incline direction
# set three corners that would define surface angle.
inner0_top_surf_corners = {
    "low": (-inner0_width / 2, inner0_length / 2, inner0_surf_low),
    "mdl": (inner0_width / 2, inner0_length / 2, inner0_surf_mdl),
    "high": (inner0_width / 2, -inner0_length / 2, inner0_surf_high),
}

# use this for the rotation in the switch surface XY plane.
# positive values - anti clockwise
# negative values - clockwise
inner0_switch_rotation_angle_deg = 5
inner0_body_rotation_angle_deg = 4

# you do not need to touch these settings
inner0_settings = {
    "name": "inner0",
    "base_dimensions": {"width": inner0_width, "length": inner0_length, "hight": inner0_hight},
    "switch_center": inner0_switch_center,
    "top_surf_conners": inner0_top_surf_corners,
    "switch_rotation_angle": inner0_switch_rotation_angle_deg * math.pi / 180,
    "body_rotation_angle": inner0_body_rotation_angle_deg * math.pi / 180,
}
THUMB_INNER_SECTION_SETTINGS.append(inner0_settings)
########################################## 3}}}

############segment locations############### {{{3
inner0 = THUMB_INNER_SECTION_SETTINGS[0]["base_dimensions"]
# As you rotatate the segment, gaps appear. To avoid that, move segment into the base segment.
inner0_adjust_xcoord_for_rotation = tocm(2)
# adjust xcoord to position thumb section relative
# to the fingers section.
inner0_adjust_xcoord = inner0_adjust_xcoord_for_rotation + adjust_xcoord_relative_to_fingers_section
inner0_ycoord_adjust = tocm(5) + adjust_ycoord_relative_to_fingers_section
THUMB_INNER_SECTION_SETTINGS[0]["location"] = (
    -xcoord_inner0 + inner0_adjust_xcoord,
    tocm(0) - inner0_ycoord_adjust,
    tocm(0)
)
########################################## 3}}}

############################################ 2}}}

############################################
################# middle #################### {{{2

################# middle 0 ################## {{{3

# base dimensions
middle0_width = middle_segment_width
middle0_length = tocm(33)
middle0_hight = THUMB_SECTION_HIGHT + tocm(30)

# switch center
middle0_switch_center = (tocm(1), tocm(2), tocm(0))

# switch surface:
# the incline magnitude
middle0_surf_low = middle0_hight
middle0_surf_mdl = middle0_surf_low + tocm(10)
middle0_surf_high = middle0_surf_low + tocm(14)

# the incline direction
# set three corners that would define surface angle.
middle0_top_surf_corners = {
    "low": (-middle0_width / 2, middle0_length / 2, middle0_surf_low),
    "mdl": (middle0_width / 2, middle0_length / 2, middle0_surf_mdl),
    "high": (middle0_width / 2, -middle0_length / 2, middle0_surf_high),
}

# use this for the rotation in the switch surface XY plane.
# positive values - anti clockwise
# negative values - clockwise
middle0_switch_rotation_angle_deg = 7
middle0_body_rotation_angle_deg = 5

# you do not need to touch these settings
middle0_settings = {
    "name": "middle0",
    "base_dimensions": {"width": middle0_width, "length": middle0_length, "hight": middle0_hight},
    "switch_center": middle0_switch_center,
    "top_surf_conners": middle0_top_surf_corners,
    "switch_rotation_angle": middle0_switch_rotation_angle_deg * math.pi / 180,
    "body_rotation_angle": middle0_body_rotation_angle_deg * math.pi / 180,
}
THUMB_MIDDLE_SECTION_SETTINGS.append(middle0_settings)
########################################## 3}}}

############segment locations############### {{{3
middle0 = THUMB_MIDDLE_SECTION_SETTINGS[0]["base_dimensions"]
xcoord = middle_segment_width / 2 + inner_segment_width / 2 + xcoord_inner0
middle0_adjust_xcoord_for_rotation = tocm(3)
middle0_adjust_xcoord = middle0_adjust_xcoord_for_rotation + adjust_xcoord_relative_to_fingers_section
middle0_ycoord_adjust = tocm(7) + adjust_ycoord_relative_to_fingers_section
THUMB_MIDDLE_SECTION_SETTINGS[0]["location"] = (
    -xcoord + middle0_adjust_xcoord,
    tocm(0) - middle0_ycoord_adjust,
    tocm(0)
)
########################################## 3}}}

############################################ 2}}}

############################################
################# outer #################### {{{2

################# outer 0 ################## {{{3

# base dimensions
outer0_width = outer_segment_width
outer0_length = tocm(32)
outer0_hight = THUMB_SECTION_HIGHT + tocm(30)

# switch center
outer0_switch_center = (tocm(0), tocm(0), tocm(0))

# switch surface:
# the incline magnitude
outer0_surf_low = outer0_hight
outer0_surf_mdl = outer0_surf_low + tocm(2)
outer0_surf_high = outer0_surf_low + tocm(5)

# the incline direction
# set three corners that would define surface angle.
outer0_top_surf_corners = {
    "low": (-outer0_width / 2, -outer0_length / 2, outer0_surf_low),
    "mdl": (-outer0_width / 2, outer0_length / 2, outer0_surf_mdl),
    "high": (outer0_width / 2, outer0_length / 2, outer0_surf_high),
}

# use this for the rotation in the switch surface XY plane.
# positive values - anti clockwise
# negative values - clockwise
outer0_switch_rotation_angle_deg = 13
outer0_body_rotation_angle_deg = 10

# you do not need to touch these settings
outer0_settings = {
    "name": "outer0",
    "base_dimensions": {"width": outer0_width, "length": outer0_length, "hight": outer0_hight},
    "switch_center": outer0_switch_center,
    "top_surf_conners": outer0_top_surf_corners,
    "switch_rotation_angle": outer0_switch_rotation_angle_deg * math.pi / 180,
    "body_rotation_angle": outer0_body_rotation_angle_deg * math.pi / 180,
}
THUMB_OUTER_SECTION_SETTINGS.append(outer0_settings)
########################################## 3}}}

############segment locations############### {{{3
outer0 = THUMB_OUTER_SECTION_SETTINGS[0]["base_dimensions"]
xcoord = outer_segment_width / 2 + middle_segment_width + inner_segment_width / 2 + xcoord_inner0
outer0_adjust_xcoord_for_rotation = tocm(5)
outer0_adjust_xcoord = outer0_adjust_xcoord_for_rotation + adjust_xcoord_relative_to_fingers_section
outer0_ycoord_adjust = tocm(10) + adjust_ycoord_relative_to_fingers_section
THUMB_OUTER_SECTION_SETTINGS[0]["location"] = (
    -xcoord + outer0_adjust_xcoord,
    tocm(0) - outer0_ycoord_adjust,
    tocm(0)
)
########################################## 3}}}

############################################ 2}}}

########################################### }}}


def add_segment(comp, settings, ui):  # {{{
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

    # construct plane only if there is an incline to it:
    # check that z coordinates are different
    switch_surf_plane = None
    if (settings["top_surf_conners"]["low"][2] != settings["top_surf_conners"]["mdl"][2]) or \
            (settings["top_surf_conners"]["low"][2] != settings["top_surf_conners"]["high"][2]):
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
        switch_surf_plane = planes.add(planeInput)

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

    # split base body only if there is a plane to split with
    if switch_surf_plane:
        # Create SplitBodyFeatureInput
        splitBodyFeats = comp.features.splitBodyFeatures
        splitBodyInput = splitBodyFeats.createInput(base_body, switch_surf_plane, True)

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

    # make a switch hole only if there settings for it.
    if settings["switch_center"]:
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
# }}}


def combine(rootComp, ui):  # {{{
    combineFeatures = rootComp.features.combineFeatures
    toolBodies = adsk.core.ObjectCollection.create()
    occs = rootComp.occurrences
    for idx, comp in enumerate(occs):
        comp = comp.component
        if "base" in comp.name:
            continue
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


def combine_with_base(rootComp, ui):  # {{{
    combineFeatures = rootComp.features.combineFeatures
    toolBodies = adsk.core.ObjectCollection.create()
    occs = rootComp.occurrences
    for idx, comp in enumerate(occs):
        comp = comp.component
        if "base" in comp.name:
            for b in comp.bRepBodies:
                if comp.name in b.name:
                    toolBodies.add(b)
                    # ui.messageBox('targetBody name:\n{}'.format(b.name))
            continue
        if idx == IDX_COMPONENT_WITH_COMPBINED_BODY:
            for b in comp.bRepBodies:
                if comp.name in b.name:
                    targetBody = b
                    # ui.messageBox('targetBody name:\n{}'.format(b.name))
        # else:
        #     for b in comp.bRepBodies:
        #         if comp.name in b.name:
        #             # ui.messageBox('toolBodies name:\n{}'.format(b.name))
        #             toolBodies.add(b)

    combineInput = combineFeatures.createInput(targetBody, toolBodies)
    # combineInput.operation = adsk.fusion.FeatureOperations.CutFeatureOperation
    combineInput.operation = adsk.fusion.FeatureOperations.JoinFeatureOperation
    combineInput.isKeepToolBodies = False
    combineFeatures.add(combineInput)
#  }}}


def cut_off_at_base_top_level(rootComp, ui):  # {{{
    # combineFeatures = rootComp.features.combineFeatures
    # toolBodies = adsk.core.ObjectCollection.create()
    occs = rootComp.occurrences
    for idx, comp in enumerate(occs):
        comp = comp.component
        if "base" in comp.name:
            for b in comp.bRepBodies:
                if comp.name in b.name:
                    # toolBodies.add(b)
                    for f in b.faces:
                        # the opposite ends do not lie on XY plane
                        if f.vertices.item(0).geometry.z != 0.0 and f.vertices.item(2).geometry.z != 0.0:
                            cut_off_top_face = f
                    continue
        if idx == IDX_COMPONENT_WITH_COMPBINED_BODY:
            target_comp = comp
            for b in target_comp.bRepBodies:
                if comp.name in b.name:
                    targetBody = b

#     # cut off the bit that sticks into the base body.
#     combineInput = combineFeatures.createInput(targetBody, toolBodies)
#     combineInput.operation = adsk.fusion.FeatureOperations.CutFeatureOperation
#     # combineInput.operation = adsk.fusion.FeatureOperations.JoinFeatureOperation
#     combineInput.isKeepToolBodies = True
#     combineFeatures.add(combineInput)

    # cut off the bit that sticks out the top face of the base body.
    # Create SplitBodyFeatureInput
    splitBodyFeats = rootComp.features.splitBodyFeatures
    splitBodyInput = splitBodyFeats.createInput(targetBody, cut_off_top_face, True)
    # Create split body feature
    splitBodyFeats.add(splitBodyInput)

    # select the correct body - the one that contains the base_corner
    split_body_idx = 0
    # for idx, spb in enumerate(occs.item(IDX_COMPONENT_WITH_COMPBINED_BODY).component.bRepBodies):
    for idx, spb in enumerate(target_comp.bRepBodies):
        for v in spb.vertices:
            if v.geometry.z == 0.0:
                # bottom_split_body = spb
                split_body_idx = idx
                break
        if split_body_idx != 0:
            break
    bs = [x for i, x in enumerate(target_comp.bRepBodies) if i != split_body_idx]
    for b in bs:
        b.isVisible = False
        b.name = "notneeded"
    #ui.messageBox('body:\n{}'.format(dir(bottom_split_body)))
    # bottom_split_body.name = "{}_bottom".format(settings["name"])
#  }}}


def cut_off_at_base_back_level(rootComp, ui):  # {{{
    occs = rootComp.occurrences
    for idx, comp in enumerate(occs):
        comp = comp.component
        if "base" in comp.name:
            for b in comp.bRepBodies:
                if comp.name in b.name:
                    for f in b.faces:
                        # all ycoords are positive and equal
                        if f.vertices.item(0).geometry.y == f.vertices.item(2).geometry.y \
                            == f.vertices.item(1).geometry.y \
                                and f.vertices.item(0).geometry.y > 0.0 and f.vertices.item(2).geometry.y > 0.0:
                            cut_off_back_base = f
                    continue
        if idx == IDX_COMPONENT_WITH_COMPBINED_BODY:
            target_comp = comp
            for b in target_comp.bRepBodies:
                if comp.name in b.name:
                    targetBody = b

    # cut off the bit that sticks out the front face of the base body.
    # Create SplitBodyFeatureInput
    splitBodyFeats = rootComp.features.splitBodyFeatures
    splitBodyInput = splitBodyFeats.createInput(targetBody, cut_off_back_base, True)
    # Create split body feature
    splitBodyFeats.add(splitBodyInput)

    # select the correct body - the one that contains the base_corner
    keep_body_idx = 0
    # for idx, spb in enumerate(occs.item(IDX_COMPONENT_WITH_COMPBINED_BODY).component.bRepBodies):
    for idx, spb in enumerate(target_comp.bRepBodies):
        for v in spb.vertices:
            if v.geometry.y < 0.0:
                keep_body_idx = idx
                break
        if keep_body_idx != 0:
            break
    bs = [x for i, x in enumerate(target_comp.bRepBodies) if i != keep_body_idx]
    for b in bs:
        b.deleteMe()
    #ui.messageBox('body:\n{}'.format(dir(bottom_split_body)))
    # bottom_split_body.name = "{}_bottom".format(settings["name"])
#  }}}


# cut off the bit that sticks out the top face of the inner segment  body.
def cut_off_at_inner_top_from_base(rootComp, ui):  # {{{
    occs = rootComp.occurrences
    for comp in occs:
        comp = comp.component
        if "base" in comp.name:
            for b in comp.bRepBodies:
                if comp.name in b.name:
                    targetBody = b
            target_comp = comp
            continue
        if "inner" in comp.name:
            for b in comp.bRepBodies:
                if comp.name in b.name:
                    for f in b.faces:
                        # all zcoords are greater than zero
                        if f.vertices.item(0).geometry.z > 0.0 and f.vertices.item(2).geometry.y > 0.0 \
                                and f.vertices.item(1).geometry.z > 0.0 and f.vertices.item(3).geometry.z > 0.0:
                            cut_off_inner_top_face = f
                            break
            continue

    # Create SplitBodyFeatureInput
    splitBodyFeats = rootComp.features.splitBodyFeatures
    splitBodyInput = splitBodyFeats.createInput(targetBody, cut_off_inner_top_face, True)
    # Create split body feature
    splitBodyFeats.add(splitBodyInput)

    # select the correct body - the one that has a bottom face
    keep_body_idx = None
    for idx, spb in enumerate(target_comp.bRepBodies):
        # ui.messageBox('spb.name:\n{}'.format(spb.name))
        for f in spb.faces:
            for v in f.vertices:
                # select the bottom body: zcoord == 0.0
                # ui.messageBox('f.vertices.item(0).geometry.z:\n{}'.format(f.vertices.item(0).geometry.z))
                # ui.messageBox('f.vertices.item(2).geometry.z:\n{}'.format(f.vertices.item(2).geometry.z))
                if f.vertices.item(0).geometry.z == 0.0 and f.vertices.item(2).geometry.z == 0.0:
                    keep_body_idx = idx
                    # ui.messageBox('set keep_body_idx to {}\n: '.format(keep_body_idx))
                    break
        if keep_body_idx is not None:
            break
    bs = [x for i, x in enumerate(target_comp.bRepBodies) if i != keep_body_idx]
    for b in bs:
        b.deleteMe()
    #ui.messageBox('body:\n{}'.format(dir(bottom_split_body)))
    # bottom_split_body.name = "{}_bottom".format(settings["name"])
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
        if f.vertices.item(0).geometry.z == 0.0 and f.vertices.item(2).geometry.z == 0.0:
            face = f
    entities.add(face)

    # Create a shell feature
    shellFeats = comp.features.shellFeatures
    isTangentChain = False
    shellFeatureInput = shellFeats.createInput(entities, isTangentChain)
    thickness = adsk.core.ValueInput.createByReal(THUMB_SECTION_SHELL_THICKNESS)
    shellFeatureInput.insideThickness = thickness
    shellFeats.add(shellFeatureInput)
# }}}


def add_dove_tail(rootComp, ui):  # {{{
    occs = rootComp.occurrences
    for c in occs:
        c = c.component
        if "inner" in c.name:
            comp = c
            break
    # get the left face.
    for b in comp.bRepBodies:
        if comp.name in b.name:
            for f in b.faces:
                if f.vertices.item(0).geometry.x > 0.0 and f.vertices.item(2).geometry.x > 0.0:
                        face = f
    # Create a dove tail sketch on the xy plane.
    sketches = comp.sketches
    sketch = sketches.add(comp.xYConstructionPlane)
    sketch.name = "{}_dove_tail".format(comp.name)
    x0 = face.vertices.item(0).geometry.x
    x1 = x0
    x2 = x0 + DOVE_TAIL_LENGTH
    y1 = DOVE_TAIL_WIDTH_BASE / 2.0
    y2 = DOVE_TAIL_WIDTH_END / 2.0
    lines = sketch.sketchCurves.sketchLines
    line1 = lines.addByTwoPoints(adsk.core.Point3D.create(x1, y1, 0), adsk.core.Point3D.create(x2, y2, 0))
    line2 = lines.addByTwoPoints(line1.endSketchPoint, adsk.core.Point3D.create(x2, -y2, 0))
    line3 = lines.addByTwoPoints(line2.endSketchPoint, adsk.core.Point3D.create(x1, -y1, 0))
    lines.addByTwoPoints(line3.endSketchPoint, line1.startSketchPoint)
    #comp.bRepBodies extrude the sketch
    extrudes = comp.features.extrudeFeatures
    prof = sketch.profiles.item(sketch.profiles.count - 1)
    extInput_switch = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    distance = adsk.core.ValueInput.createByReal(max(face.vertices.item(0).geometry.z, face.vertices.item(2).geometry.z))
    extInput_switch.setDistanceExtent(False, distance)
    extrudes.add(extInput_switch)
    comp.bRepBodies.item(comp.bRepBodies.count - 1).name = "{}_dove_tail".format(comp.name)
# }}}


def chamfer_top_right_edges(rootComp, ui):  # {{{
    occs = rootComp.occurrences
    comp = occs.item(IDX_COMPONENT_WITH_COMPBINED_BODY).component

    # collect the bodies to fillet
    bodies = adsk.core.ObjectCollection.create()
    for idx, comp in enumerate(occs):
        comp = comp.component
        if "base" in comp.name:
            continue
        if "inner" in comp.name:
            continue
        for b in comp.bRepBodies:
            if comp.name in b.name:
                bodies.add(b)

    # collect the top edges, with no vertices on XY plane (z coord is 0)
    # collect edges with both y coord > 0
    edges = adsk.core.ObjectCollection.create()
    for b in bodies:
        for e in b.edges:
            # the opposite ends lie on XY plane: Z coord is zero
            if e.startVertex.geometry.z != 0.0 and e.endVertex.geometry.z != 0.0:
                if e.startVertex.geometry.x > 0.0 and e.endVertex.geometry.x > 0.0:
                    edges.add(e)
                    # ui.messageBox('got an edge:\n{}'.format(edges.count))
    # radius1 = adsk.core.ValueInput.createByReal()
    # # Get fillet features
    # fillets = rootComp.features.filletFeatures
    # input1 = fillets.createInput()
    # input1.addConstantRadiusEdgeSet(edges, radius1, True)
    # input1.isG2 = False
    # input1.isRollingBallCorner = True
    # fillet1 = fillets.add(input1)
    # fillet1.deleteMe()

    # Create the ChamferInput object.
    chamfers = rootComp.features.chamferFeatures
    chamferInput = chamfers.createInput(edges, True)
    chamferInput.setToEqualDistance(adsk.core.ValueInput.createByReal(tocm(2)))
    # chamfer = chamfers.add(chamferInput)
    chamfers.add(chamferInput)
# }}}


def chamfer_outer_vertical_edges(rootComp, ui):  # {{{
    occs = rootComp.occurrences
    comp = occs.item(IDX_COMPONENT_WITH_COMPBINED_BODY).component

    # collect the bodies to fillet
    bodies = adsk.core.ObjectCollection.create()
    for idx, comp in enumerate(occs):
        comp = comp.component
        if "base" in comp.name:
            continue
        for b in comp.bRepBodies:
            if comp.name in b.name:
                bodies.add(b)

    # collect the outer, vertical edges, with one end on XY plane (z coord is 0)
    # the other end has z coord > 0,
    # collect edges with both y coord < 0
    edges = adsk.core.ObjectCollection.create()
    for b in bodies:
        if "outer" in b.name:
            for e in b.edges:
                # the opposite ends lie on XY plane: Z coord is zero
                if (e.startVertex.geometry.z == 0.0 and e.endVertex.geometry.z != 0.0) or \
                        (e.startVertex.geometry.z != 0.0 and e.endVertex.geometry.z == 0.0):
                    if e.startVertex.geometry.x < 0.0:
                        edges.add(e)
                        # ui.messageBox('start z:\n{}'.format(e.startVertex.geometry.z))
    # radius1 = adsk.core.ValueInput.createByReal()
    # # Get fillet features
    # fillets = rootComp.features.filletFeatures
    # input1 = fillets.createInput()
    # input1.addConstantRadiusEdgeSet(edges, radius1, True)
    # input1.isG2 = False
    # input1.isRollingBallCorner = True
    # fillet1 = fillets.add(input1)
    # fillet1.deleteMe()

    # Create the ChamferInput object.
    chamfers = rootComp.features.chamferFeatures
    chamferInput = chamfers.createInput(edges, True)
    chamferInput.setToEqualDistance(adsk.core.ValueInput.createByReal(tocm(4)))
    # chamfer = chamfers.add(chamferInput)
    chamfers.add(chamferInput)
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


# cut switches section from base segment so that it can be inserted into base
def cut_into_base(rootComp, ui):  # {{{
    occs = rootComp.occurrences
    for idx, comp in enumerate(occs):
        comp = comp.component
        if idx == IDX_COMPONENT_WITH_COMPBINED_BODY:
            sketch_comp = comp
            for b in comp.bRepBodies:
                if comp.name in b.name:
                    for f in b.faces:
                        if f.vertices.item(0).geometry.z == 0.0 and f.vertices.item(2).geometry.z == 0.0:
                            face = f
        if "base" in comp.name:
            for b in comp.bRepBodies:
                if comp.name in b.name:
                    targetBody = b
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

    # collect sketch profiles
    profs = adsk.core.ObjectCollection.create()
    for prof in sketch_offset.profiles:
        profs.add(prof)
    extrudes = sketch_comp.features.extrudeFeatures
    extInput = extrudes.createInput(profs, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    distance = adsk.core.ValueInput.createByReal(base0_hight)
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
        for thumb_column in THUMB_SECTIONS_SETTINGS:
            for segment_settings in thumb_column:
                # if segment_settings["name"] == "mdl1":
                # if "indx" in segment_settings["name"]:
                # if "mdl" in segment_settings["name"]:
                    vector = adsk.core.Vector3D.create(*segment_settings["location"])
                    transform = adsk.core.Matrix3D.create()
                    if segment_settings["body_rotation_angle"]:
                        # Create a transform to do move
                        rotation_axis = adsk.core.Vector3D.create(0, 0, 1)
                        rotation_origin = adsk.core.Point3D.create(0, 0, 0)
                        transform.setToRotation(segment_settings["body_rotation_angle"], rotation_axis, rotation_origin)
                    transform.translation = vector

                    # Create a component under root component
                    occ = allOccs.addNewComponent(transform)
                    subComp = occ.component
                    # print(subComp.revisionId)
                    add_segment(subComp, segment_settings, ui)
        chamfer_top_right_edges(rootComp, ui)
        chamfer_outer_vertical_edges(rootComp, ui)
        # add_dove_tail(rootComp, ui)
        cut_off_at_inner_top_from_base(rootComp, ui)
        combine(rootComp, ui)
        # cut_into_base(rootComp, ui)
        cut_off_at_base_back_level(rootComp, ui)
        # cut off the tip of the inner switch,
        # use only if it sticks out obove the base top surface
        if inner0_surf_high > base0_hight:
            cut_off_at_base_top_level(rootComp, ui)
        combine_with_base(rootComp, ui)
        shell(rootComp, ui)
        cut_switch_holes(rootComp, ui)
    except Exception as e:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
            print(e)
# }}}
