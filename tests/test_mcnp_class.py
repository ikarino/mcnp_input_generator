import pytest
from marshmallow.exceptions import ValidationError
from mcnp_input_generator.mcnp_class import (
    MCNPCellSchema,
    MCNPMaterialSchema,
    MCNPSurfaceSchema,
)


def test_cell_schema():
    inp = {
        "_name": "aa",
        "snames": ["+aa", "-bb"],
        "matname": "air",
    }
    MCNPCellSchema().load(inp)


def test_surface_schema():
    inp = {
        "name": "water",
        "shape": "RCC",
        "data": [2, 3, 4]
    }
    MCNPSurfaceSchema().load(inp)
    with pytest.raises(ValidationError):
        inp['shape'] = 'aaaaaaa'
        MCNPSurfaceSchema().load(inp)


def test_material_schema():
    inp = {
        "matname": "iron",
        "density": 7.8,
        "color": "red",
        "_mass_fractions": {
            "28000": -1
        }
    }
    MCNPMaterialSchema().load(inp)
