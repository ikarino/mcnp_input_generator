## MCNP Input Generator
unofficial mcnp input file generator.


```python
from mcnp_input_generator import load

_inp = {
    "title": "test",
    "cells": [
        {
            "_name": "outside world",
            "snames": ["+world"],
            "matname": "void",
        },
        {
            "snames": ["-world", "+mycylinder"],
            "matname": "water"
        },
        {
            "snames": ["-mycylinder"],
            "matname": "iron",
        }
    ],
    "surfaces": [
        {
            "name": "world",
            "shape": "RPP",
            "data": [-100, 100, -100, 100, -100, 100]
        },
        {
            "name": "mycylinder",
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

mig = load(_inp)
mig.openscad("test_generator.scad")
# => visualized with openscad, see below links
mig.to_inp("inp")
# => mcnp input
```


## powered by
- *geometry visulaization*: [OpenSCAD](https://openscad.org/) and [SolidPython](https://github.com/SolidCode/SolidPython)
- *inputs deserialization*: [marshmallow](https://marshmallow.readthedocs.io/en/stable/index.html)

## useful links
- [openscad cheatsheet](http://openscad.org/cheatsheet/)

## 日本語情報
### 参考にしたWebページ
- [Python パッケージングその1](https://www.m3tech.blog/entry/python-packaging)
- [Python パッケージングその2](https://qiita.com/gyu-don/items/833ceb2068f33a9a11e1)

