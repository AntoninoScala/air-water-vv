from proteus.default_p import *
from proteus.mprans import RDLS3P
from proteus import Context

ct = Context.get()
domain = ct.domain
nd = domain.nd
mesh = domain.MeshOptions


genMesh = mesh.genMesh
movingDomain = ct.movingDomain
T = ct.T

"""
The redistancing equation in the sloshbox test problem.
"""

LevelModelType = RDLS3P.LevelModel

coefficients = RDLS3P.Coefficients(applyRedistancing=ct.applyRedistancing,
                                 epsFact=ct.epsFact_redistance,
                                 nModelId=1,
                                 rdModelId=2,
                                 useMetrics=ct.useMetrics)
                                 

def getDBC_rd(x, flag):
    pass

dirichletConditions     = {0: getDBC_rd}
weakDirichletConditions = {0: RDLS3P.setZeroLSweakDirichletBCsSimple}

advectiveFluxBoundaryConditions = {}
diffusiveFluxBoundaryConditions = {0: {}}

class PerturbedSurface_phi:
    def uOfXT(self,x,t):
        return ct.signedDistance(x)

initialConditions  = {0:PerturbedSurface_phi()}
