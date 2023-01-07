
# Script for the usage of the CreateBridgeBeam function

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_BaseElements as AllplanBaseElements
import NemAll_Python_BasisElements as AllplanBasisElements
import NemAll_Python_Utility as AllplanUtil
import GeometryValidate as GeometryValidate

from StdReinfShapeBuilder.RotationAngles import RotationAngles
from HandleDirection import HandleDirection
from HandleProperties import HandleProperties
from HandleService import HandleService

print('Load BridgeBeam.py')


def check_allplan_version(build_ele, version):
    

    del build_ele
    del version


    return True


def create_element(build_part, doc):

    element = CreateBridgeBeam(doc)


    return element.create(build_part)

def move_handle(build_br_part, handle_property, input_pnt, doc):

    build_br_part.change_property(handle_property, input_pnt)

    if (handle_property.handle_id == "BeamHeight"):
        build_br_part.RibHeight.value = build_br_part.BeamHeight.value - build_br_part.TopShHeight.value - build_br_part.BotShLowHeight.value - build_br_part.BotShUpHeight.value
        if (build_br_part.HoleHeight.value > build_br_part.BeamHeight.value - build_br_part.TopShHeight.value - 45.5):
            build_br_part.HoleHeight.value = build_br_part.BeamHeight.value - build_br_part.TopShHeight.value - 45.5


    return create_element(build_br_part, doc)

def modify_element_property(build_part, name, value):

    if (name == "BeamHeight"):
        change = value - build_part.TopShHeight.value - build_part.RibHeight.value - build_part.BotShUpHeight.value - build_part.BotShLowHeight.value
        print(change)
        if (change < 0):
            change = abs(change)
            if (build_part.TopShHeight.value > 320.):
                if (build_part.TopShHeight.value - change < 320.):
                    change -= build_part.TopShHeight.value - 320.
                    build_part.TopShHeight.value = 320.
                else:
                    build_part.TopShHeight.value -= change
                    change = 0.
            if (change != 0) and (build_part.BotShUpHeight.value > 160.):
                if (build_part.BotShUpHeight.value - change < 160.):
                    change -= build_part.BotShUpHeight.value - 160.
                    build_part.BotShUpHeight.value = 160.
                else:
                    build_part.BotShUpHeight.value -= change
                    change = 0.
            if (change != 0) and (build_part.BotShLowHeight.value > 153.):
                if (build_part.BotShLowHeight.value - change < 153.):
                    change -= build_part.BotShLowHeight.value - 153.
                    build_part.BotShLowHeight.value = 153.
                else:
                    build_part.BotShLowHeight.value -= change
                    change = 0.
            if (change != 0) and (build_part.RibHeight.value > 467.):
                if (build_part.RibHeight.value - change < 467.):
                    change -= build_part.RibHeight.value - 467.
                    build_part.RibHeight.value = 467.
                else:
                    build_part.RibHeight.value -= change
                    change = 0.
        else:
            build_part.RibHeight.value += change
        if (value - build_part.TopShHeight.value - 45.5 < build_part.HoleHeight.value):
            build_part.HoleHeight.value = value - build_part.TopShHeight.value - 45.5
    elif (name == "TopShHeight"):
        build_part.BeamHeight.value = value + build_part.RibHeight.value + build_part.BotShUpHeight.value + build_part.BotShLowHeight.value
    elif (name == "RibHeight"):
        build_part.BeamHeight.value = value + build_part.TopShHeight.value + build_part.BotShUpHeight.value + build_part.BotShLowHeight.value
    elif (name == "BotShUpHeight"):
        build_part.BeamHeight.value = value + build_part.TopShHeight.value + build_part.RibHeight.value + build_part.BotShLowHeight.value
        if (value + build_part.BotShLowHeight.value + 45.5 > build_part.HoleHeight.value):
            build_part.HoleHeight.value = value + build_part.BotShLowHeight.value + 45.5
    elif (name == "BotShLowHeight"):
        build_part.BeamHeight.value = value + build_part.TopShHeight.value + build_part.RibHeight.value + build_part.BotShUpHeight.value
        if (build_part.BotShUpHeight.value + value + 45.5 > build_part.HoleHeight.value):
            build_part.HoleHeight.value = build_part.BotShUpHeight.value + value + 45.5
    elif (name == "HoleHeight"):
        if (value > build_part.BeamHeight.value - build_part.TopShHeight.value - 45.5):
            build_part.HoleHeight.value = build_part.BeamHeight.value - build_part.TopShHeight.value - 45.5
        elif (value < build_part.BotShLowHeight.value + build_part.BotShUpHeight.value + 45.5):
            build_part.HoleHeight.value = build_part.BotShLowHeight.value + build_part.BotShUpHeight.value + 45.5
    elif (name == "HoleDepth"):
        if (value >= build_part.BeamLength.value / 2.):
            build_part.HoleDepth.value = build_part.BeamLength.value / 2. - 45.5

    return True

class CreateBridgeBeam():

    def __init__(self, doc):

        self.model_part_list = []
        self.handle_list = []
        self.document = doc
        
    def create(self, build_prt):
        
        self._top_sh_width = build_prt.TopShWidth.value
        self._top_sh_height = build_prt.TopShHeight.value

        self._bot_sh_width = build_prt.BotShWidth.value
        self._bot_sh_up_height = build_prt.BotShUpHeight.value
        self._bot_sh_low_height = build_prt.BotShLowHeight.value
        self._bot_sh_height = self._bot_sh_up_height + self._bot_sh_low_height

        if (build_prt.RibThick.value > min(self._top_sh_width, self._bot_sh_width)):
            build_prt.RibThick.value = min(self._top_sh_width, self._bot_sh_width)
        self.rib_thick = build_prt.RibThick.value
        self._rib_height = build_prt.RibHeight.value

        self._beam_length = build_prt.BeamLength.value
        self.beam_wid = max(self._top_sh_width, self._bot_sh_width)
        self.beam_hei = build_prt.BeamHeight.value

        self._hole_depth = build_prt.HoleDepth.value
        self._hole_height = build_prt.HoleHeight.value

        self._angleX = build_prt.RotationAngleX.value
        self._angleY = build_prt.RotationAngleY.value
        self._angleZ = build_prt.RotationAngleZ.value

        self.create_beam(build_prt)
        self.create_handles(build_prt)
        
        AllplanBaseElements.ElementTransform(AllplanGeo.Vector3D(), self._angleX, self._angleY, self._angleZ, self.model_part_list)

        rot_angles = RotationAngles(self._angleX, self._angleY, self._angleZ)
        HandleService.transform_handles(self.handle_list, rot_angles.get_rotation_matrix())
        
        return (self.model_part_list, self.handle_list)


    def create_beam(self, build_part):
        com_prop = AllplanBaseElements.CommonProperties()
        com_prop.GetGlobalProperties()
        com_prop.Pen = 1
        com_prop.Color = build_part.Color3.value
        com_prop.Stroke = 1


        bottom_shelf = AllplanGeo.BRep3D.CreateCuboid(AllplanGeo.AxisPlacement3D(AllplanGeo.Point3D((self.beam_wid - self._bot_sh_width) / 2., 0., 0.), AllplanGeo.Vector3D(1, 0, 0), AllplanGeo.Vector3D(0, 0, 1)), self._bot_sh_width, self._beam_length, self._bot_sh_height)

        edges = AllplanUtil.VecSizeTList()
        edges.append(10)
        edges.append(8)
        err, bottom_shelf = AllplanGeo.ChamferCalculus.Calculate(bottom_shelf, edges, 20., False)
        

        top_shelf = AllplanGeo.BRep3D.CreateCuboid(AllplanGeo.AxisPlacement3D(AllplanGeo.Point3D((self.beam_wid - self._top_sh_width) / 2., 0., self.beam_hei - self._top_sh_height), AllplanGeo.Vector3D(1, 0, 0), AllplanGeo.Vector3D(0, 0, 1)), self._top_sh_width, self._beam_length, self._top_sh_height)

        top_shelf_notch = AllplanGeo.BRep3D.CreateCuboid(AllplanGeo.AxisPlacement3D(AllplanGeo.Point3D((self.beam_wid - self._top_sh_width) / 2., 0., self.beam_hei - 45.), AllplanGeo.Vector3D(1, 0, 0), AllplanGeo.Vector3D(0, 0, 1)), 60., self._beam_length, 45.)
        err, top_shelf = AllplanGeo.MakeSubtraction(top_shelf, top_shelf_notch)
        if not GeometryValidate.polyhedron(err):
            return
        top_shelf_notch = AllplanGeo.Move(top_shelf_notch, AllplanGeo.Vector3D(self._top_sh_width - 60., 0, 0))
        err, top_shelf = AllplanGeo.MakeSubtraction(top_shelf, top_shelf_notch)
        if not GeometryValidate.polyhedron(err):
            return
        
        err, beam = AllplanGeo.MakeUnion(bottom_shelf, top_shelf)
        if not GeometryValidate.polyhedron(err):
            return


        rib = AllplanGeo.BRep3D.CreateCuboid(AllplanGeo.AxisPlacement3D(AllplanGeo.Point3D(0., 0., self._bot_sh_height), AllplanGeo.Vector3D(1, 0, 0), AllplanGeo.Vector3D(0, 0, 1)), self.beam_wid, self._beam_length, self._rib_height)
        
        err, beam = AllplanGeo.MakeUnion(beam, rib)
        if not GeometryValidate.polyhedron(err):
            return
        

        left_notch_pol = AllplanGeo.Polygon2D()
        left_notch_pol += AllplanGeo.Point2D((self.beam_wid - self.rib_thick) / 2., self.beam_hei - self._top_sh_height)
        left_notch_pol += AllplanGeo.Point2D((self.beam_wid - self.rib_thick) / 2., self._bot_sh_height)
        left_notch_pol += AllplanGeo.Point2D((self.beam_wid - self._bot_sh_width) / 2., self._bot_sh_low_height)
        left_notch_pol += AllplanGeo.Point2D(0., self._bot_sh_low_height)     
        left_notch_pol += AllplanGeo.Point2D(0., self.beam_hei - 100.)
        left_notch_pol += AllplanGeo.Point2D(0., self.beam_hei - 100.)
        left_notch_pol += AllplanGeo.Point2D((self.beam_wid - self._top_sh_width) / 2., self.beam_hei - 100.)
        left_notch_pol += AllplanGeo.Point2D((self.beam_wid - self.rib_thick) / 2., self.beam_hei - self._top_sh_height)
        if not GeometryValidate.is_valid(left_notch_pol):
            return
        
        path = AllplanGeo.Polyline3D()
        path += AllplanGeo.Point3D(0, 0, 0)
        path += AllplanGeo.Point3D(0, build_part.BeamLength.value, 0)

        err, notches = AllplanGeo.CreatePolyhedron(left_notch_pol, AllplanGeo.Point2D(0., 0.), path)
        if GeometryValidate.polyhedron(err):
            edges = AllplanUtil.VecSizeTList()
            if (self.rib_thick == self._bot_sh_width):
                edges.append(0)
            elif (self.rib_thick == self._top_sh_width):
                edges.append(1)
            else:
                edges.append(0)
                edges.append(2)
            err, notches = AllplanGeo.FilletCalculus3D.Calculate(notches, edges, 100., False)

            plane = AllplanGeo.Plane3D(AllplanGeo.Point3D(self.beam_wid / 2., 0, 0), AllplanGeo.Vector3D(1, 0, 0))
            right_notch = AllplanGeo.Mirror(notches, plane)

            err, notches = AllplanGeo.MakeUnion(notches, right_notch)
            if not GeometryValidate.polyhedron(err):
                return
            
            err, beam = AllplanGeo.MakeSubtraction(beam, notches)
            if not GeometryValidate.polyhedron(err):
                return


        sling_holes = AllplanGeo.BRep3D.CreateCylinder(AllplanGeo.AxisPlacement3D(AllplanGeo.Point3D(0, build_part.HoleDepth.value, build_part.HoleHeight.value), AllplanGeo.Vector3D(0, 0, 1), AllplanGeo.Vector3D(1, 0, 0)), 45.5, self.beam_wid)
        
        sling_hole_moved = AllplanGeo.Move(sling_holes, AllplanGeo.Vector3D(0., self._beam_length - self._hole_depth * 2, 0))

        err, sling_holes = AllplanGeo.MakeUnion(sling_holes, sling_hole_moved)
        if not GeometryValidate.polyhedron(err):
            return
            
        err, beam = AllplanGeo.MakeSubtraction(beam, sling_holes)
        if not GeometryValidate.polyhedron(err):
            return


        
        self.model_part_list.append(AllplanBasisElements.ModelElement3D(com_prop, beam))
        

    def create_handles(self, build_part):
        

        handle1 = HandleProperties("BeamLength",
                                   AllplanGeo.Point3D(0., self._beam_length, 0.),
                                   AllplanGeo.Point3D(0, 0, 0),
                                   [("BeamLength", HandleDirection.point_dir)],
                                   HandleDirection.point_dir, True)
        self.handle_list.append(handle1)

        handle2 = HandleProperties("BeamHeight",
                                   AllplanGeo.Point3D(0., 0., self.beam_hei),
                                   AllplanGeo.Point3D(0, 0, 0),
                                   [("BeamHeight", HandleDirection.point_dir)],
                                   HandleDirection.point_dir, True)
        self.handle_list.append(handle2)
        
        handle3 = HandleProperties("TopShWidth",
                                   AllplanGeo.Point3D((self.beam_wid - self._top_sh_width) / 2. + self._top_sh_width, 0., self.beam_hei - 45.),
                                   AllplanGeo.Point3D((self.beam_wid - self._top_sh_width) / 2., 0, self.beam_hei - 45.),
                                   [("TopShWidth", HandleDirection.point_dir)],
                                   HandleDirection.point_dir, True)
        self.handle_list.append(handle3)

        handle4 = HandleProperties("BotShWidth",
                                   AllplanGeo.Point3D((self.beam_wid - self._bot_sh_width) / 2. + self._bot_sh_width, 0., self._bot_sh_low_height),
                                   AllplanGeo.Point3D((self.beam_wid - self._bot_sh_width) / 2., 0, self._bot_sh_low_height),
                                   [("BotShWidth", HandleDirection.point_dir)],
                                   HandleDirection.point_dir, True)
        self.handle_list.append(handle4)
        
        handle5 = HandleProperties("RibThick",
                                   AllplanGeo.Point3D((self.beam_wid - self.rib_thick) / 2. + self.rib_thick, 0., self.beam_hei / 2.),
                                   AllplanGeo.Point3D((self.beam_wid - self.rib_thick) / 2., 0, self.beam_hei / 2.),
                                   [("RibThick", HandleDirection.point_dir)],
                                   HandleDirection.point_dir, True)
        self.handle_list.append(handle5)

        