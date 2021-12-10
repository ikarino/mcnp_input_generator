import pathlib

from mcnp_input_generator.mcnp_class import MCNPInputSchema
from mcnp_input_generator.scad import MCNPGeometry


def test_toFile():
    inp = MCNPInputSchema().load({
        "title": "test",
        "surfaces": [
            {
                "name": "world",
                "shape": "RPP",
                "data": [-100, 100, -100, 100, -100, 100]
            },
            {
                "name": "source",
                "shape": "cylinder",
                "data": [
                    0, 0, 0,
                    10, 10, 10,
                    0.5
                ]
            },
            {
                "name": "box",
                "shape": "RPP",
                "data": [20, 30, -10, 10, -10, 10]
            }
        ],
        "cells": [
            {
                "_name": "outside world",
                "snames": ["+world"],
                "matname": "void"
            },
            {
                "_name": "inside world",
                "snames": ["-world", "+source", "+box"],
                "matname": "void"
            },
            {
                "snames": ["-source"],
                "matname": "iron",
            },
            {
                "snames": ["-box"],
                "matname": "water",
            }
        ],
        "data": {
            "mode": "p",
            "materials": [
                {
                    "matname": "iron",
                    "density": 7.8,
                    "color": "gray"
                },
                {
                    "matname": "water",
                    "density": 1.0,
                    "color": "blue",
                },
                {
                    "matname": "void",
                    "density": 0,
                    "color": "white",
                    "_alpha": 0.0
                }
            ]
        }
    })
    mg = MCNPGeometry(inp)
    p = pathlib.Path(__file__).parent  # tests dir
    mg.toFile(fname=p.joinpath("files", "test_toFile.scad"))
