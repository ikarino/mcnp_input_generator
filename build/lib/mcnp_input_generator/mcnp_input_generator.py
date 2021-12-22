'''
main
'''
import os

from .constants import MACROBODIES
from .mcnp_class import MCNPInput, MCNPMaterial
from .scad import MCNPGeometry


class MCNPInputGenerator:
    inp: MCNPInput

    def __init__(self, inp: MCNPInput):
        self.inp = inp
        self.inp.data.materials.insert(0, MCNPMaterial(
            matname="void",
            density=0,
            color="white",
            _mass_fractions={},
            _atomic_fractions={}
        ))
        self.__check()

    def __check(self):
        surface_names = [s.name for s in self.inp.surfaces]
        matnames = [m.matname for m in self.inp.data.materials]

        # cells
        for c in self.inp.cells:
            for sc in c.snames:
                assert sc[1:] in surface_names, f"surface {sc} is not defined"
            assert c.matname in matnames, f"'{c.matname}' is not defined"

        # surfaces
        for s in self.inp.surfaces:
            assert s.shape in MACROBODIES, f"invalid surface shape: {s.shape}"
        assert self.inp.data.mode in ["n", "p", "np"]
        for m in self.inp.data.materials:
            assert m._mass_fractions or m._atomic_fractions, f"set fractions for {m.matname}"

    def openscad(self, fname=None):
        mg = MCNPGeometry(self.inp)
        mg.toFile(fname=fname)

    def to_inp(self, fname="inp"):
        lines = [
            self.inp.title
        ]
        lines.append("c cell definitions")
        matname2mat = {
            mat.matname: mat
            for mat in self.inp.data.materials
        }
        matnames = [mat.matname for mat in self.inp.data.materials]
        sname2index = {
            s.name: i+1
            for i, s in enumerate(self.inp.surfaces)
        }
        for i, c in enumerate(self.inp.cells):
            mat = matname2mat[c.matname]
            matid = matnames.index(c.matname)
            den = c._density if c._density else mat.density
            denline = f" -{den:.5e}" if mat.matname != "void" else ""
            lines += [
                f"c {c._name}",
                f"{i+1} {matid}{denline}"
            ]
            for s in c.snames:
                sindex = sname2index[s[1:]]
                lines.append(f"     {s[0]}{sindex}")
            if self.inp.data.mode in ["n", "np"]:
                imp = c._imp_n if c._imp_n else 1
                imp = imp if mat.matname != 'void' else 0
                lines.append(f"     imp:n={imp}")
            if self.inp.data.mode in ["p", "np"]:
                imp = c._imp_p if c._imp_p else 1
                imp = imp if mat.matname != 'void' else 0
                lines.append(f"     imp:p={imp}")

        lines += ["", "c surface definitions"]
        for i, s in enumerate(self.inp.surfaces):
            lines.append(f"c {s.name}")
            lines.append(f"{i+1} {MACROBODIES[s.shape]}")
            for d in s.data:
                lines.append(f"     {d:.4e}")

        lines += ["", "c data cards"]
        lines.append(f"mode {self.inp.data.mode}")
        lines.append("c material definitions")
        for i, mat in enumerate(self.inp.data.materials):
            if mat._atomic_fractions:
                lines.append(f"m{i} $ atomic factions of '{mat.matname}'")
                for nuclide, frac in mat._atomic_fractions.items():
                    lines.append(f"        {nuclide} -{frac:.5e}")
            elif mat._mass_fractions:
                lines.append(f"m{i} $ mass factions of '{mat.matname}'")
                for nuclide, frac in mat._mass_fractions.items():
                    lines.append(f"        {nuclide} {frac:.5e}")

        with open(fname, "w") as f:
            f.write(os.linesep.join(lines))
