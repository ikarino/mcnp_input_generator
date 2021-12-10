'''
入力のdeserializationと簡単なチェックをする。

詳細なチェックはできないので、別の場所で実装する。
基本的にmarshmallowを使うが、それではschemaとdataclassの再定義が面倒になる。
そこでmarshmallow_dataclassを利用することで、
dataclassの定義からschemaを生成している。
'''
from dataclasses import dataclass, field
from typing import Optional, Union

import marshmallow_dataclass
from marshmallow import ValidationError
from marshmallow.validate import OneOf, Range

from .constants import MACROBODIES


def validate_snames(snames):
    for sname in snames:
        if sname[0] in "-+":
            continue
        raise ValidationError(
            "surface names in cell definition must start from '+' or '-'")


@dataclass
class MCNPCell:
    _name: Optional[str] = field(metadata=dict(
        load_default="anonymous cell"
    ))
    snames: list[str] = field(metadata=dict(
        validate=validate_snames
    ))
    matname: str
    _density: Optional[float] = field(metadata=dict(
        validate=Range(min=0)
    ))
    _imp_p: Optional[int] = field(metadata=dict(
        validate=Range(min=1),
    ))
    _imp_n: Optional[int] = field(metadata=dict(
        validate=Range(min=1),
    ))


@dataclass
class MCNPSurface:
    name: str
    shape: str = field(metadata=dict(
        validate=OneOf(list(MACROBODIES.keys()))
    ))
    data: list[float]


@dataclass
class MCNPMaterial:
    matname: str
    density: float = field(metadata=dict(
        validate=Range(min=0)
    ))
    color: str
    _mass_fractions: Optional[dict[str, float]]
    _atomic_fractions: Optional[dict[str, Union[int, float]]]
    _alpha: Optional[float] = 1.0


@dataclass
class MCNPData:
    mode: str
    materials: list[MCNPMaterial]


@dataclass
class MCNPInput:
    title: str
    cells: list[MCNPCell]
    surfaces: list[MCNPSurface]
    data: MCNPData


MCNPCellSchema = marshmallow_dataclass.class_schema(MCNPCell)
MCNPSurfaceSchema = marshmallow_dataclass.class_schema(MCNPSurface)
MCNPMaterialSchema = marshmallow_dataclass.class_schema(MCNPMaterial)
MCNPInputSchema = marshmallow_dataclass.class_schema(MCNPInput)
