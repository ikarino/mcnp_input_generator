from .mcnp_class import MCNPInputSchema
from .mcnp_input_generator import MCNPInputGenerator


def load(s: dict):
    inp = MCNPInputSchema().load(s)
    return MCNPInputGenerator(inp)
