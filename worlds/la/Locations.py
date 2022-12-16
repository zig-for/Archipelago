from __future__ import absolute_import

import sys
from os.path import dirname
sys.path.append(dirname(__file__) + "/LADXR")

from LADXR.logic.overworld import World as LADXRWorld
from LADXR.settings import Settings as LADXRSettings
from LADXR.worldSetup import WorldSetup as LADXRWorldSetup
from LADXR.logic.requirements import RequirementsSettings

def generate_reference_locations():
    options =  LADXRSettings()
    world_setup = LADXRWorldSetup()
    r = RequirementsSettings()
    world = LADXRWorld(options = options, world_setup = world_setup, r = r)
    