# import pytest
import pathlib

from mcnp_input_generator.mcnp_class import MCNPInputSchema
from mcnp_input_generator.mcnp_input_generator import MCNPInputGenerator


def test_generator():
    _inp = {
        "title": "test",
        "cells": [
            {
                "snames": ["+world"],
                "matname": "void",
            },
            {
                "snames": ["-world", "+バウムクーヘン"],
                "matname": "iron"
            },
            {
                "snames": ["-バウムクーヘン"],
                "matname": "water",
            }
        ],
        "surfaces": [
            {
                "name": "world",
                "shape": "RPP",
                "data": [-100, 100, -100, 100, -100, 100]
            },
            {
                "name": "バウムクーヘン",
                "shape": "cylinder",
                "data": [0, 0, 0, 0, 0, 10, 5]
            }
        ],
        "data": {
            "mode": "p",
            "materials": [
                {
                    "matname": "iron",
                    "_mass_fractions": {
                        "28000": 1,
                    },
                    "density": 7.8,
                    "color": "gray"
                },
                {
                    "matname": "water",
                    "_mass_fractions": {
                        "1000": 2,
                        "16000": 1,
                    },
                    "density": 0.988,
                    "color": "blue",
                },
            ]
        }
    }
    inp = MCNPInputSchema().load(_inp)
    mig = MCNPInputGenerator(inp)

    p = pathlib.Path(__file__).parent  # tests dir
    mig.openscad(p.joinpath("files", "test_generator.scad"))
    mig.to_inp(p.joinpath("files", "inp"))
