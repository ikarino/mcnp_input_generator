import numpy as np
from solid import (color, cube, cylinder, rotate, scad_render_to_file, sphere,
                   translate)

from .mcnp_class import MCNPInput, MCNPSurface


def surface2solid(inp: MCNPSurface):
    shape = inp.shape
    d = inp.data
    if shape == "RCC" or shape == "cylinder":
        assert len(d) == 7
        _v = np.array(d[:3])
        _h = np.array(d[3:6])
        _r = d[6]

        # z軸と_hベクトルの為す平面に対し、
        # - その法線ベクトル
        # - 原点を中心とした回転角
        normal_vector = [-_h[1], _h[0], 0]
        angle = np.arccos(_h[2]/np.sqrt(np.sum(_h**2)))/np.pi*180
        return translate(_v+_h/2)(
            rotate(a=angle, v=normal_vector)(
                cylinder(r=_r, h=np.sqrt(np.sum(_h**2)), center=True)
            )
        )
    elif shape == "RPP":
        assert len(d) == 6
        return translate([d[0], d[2], d[4]])(
            cube([
                d[1]-d[0],
                d[3]-d[2],
                d[5]-d[4]
            ], False)
        )
    elif shape == "SPH" or shape == "sphere":
        assert len(d) == 4
        return translate(d[:3])(
            sphere(r=d[3])
        )
    else:
        raise NotImplementedError


class MCNPGeometry:
    def __init__(self, inp: MCNPInput):
        self.surface_names = [s.name for s in inp.surfaces]
        self.surface_solids = [surface2solid(s) for s in inp.surfaces]
        self.cells = inp.cells

        self.matname2mat = {
            mat.matname: mat
            for mat in inp.data.materials
        }

    def __create_model(self):
        solids = None
        for cell in self.cells:
            _mat = self.matname2mat[cell.matname]
            if _mat.density <= 0:
                continue
            _solid = None
            for sname in cell.snames:
                sindex = self.surface_names.index(sname[1:])
                __solid = self.surface_solids[sindex]
                if _solid is None:
                    _solid = __solid
                elif sname[0] == "-":
                    _solid = _solid*__solid
                elif sname[0] == "+":
                    _solid = _solid - __solid

            _solid = color(_mat.color, _mat._alpha)(_solid)
            if solids is None:
                solids = _solid
            else:
                solids += _solid
        return solids

    def toFile(self, fname="output.scad"):
        scad_render_to_file(
            self.__create_model(),
            fname,
            include_orig_code=False
        )
