from proteus import *
from proteus.default_p import *
from dambreak import *
from proteus.mprans import RANS2P

LevelModelType = RANS2P.LevelModel


# coefficients = RANS2P.Coefficients(epsFact=epsFact_viscosity,
#                                    sigma=0.0,
#                                    rho_0 = rho_0,
#                                    nu_0 = nu_0,
#                                    rho_1 = rho_1,
#                                    nu_1 = nu_1,
#                                    g=g,
#                                    nd=nd,
#                                    VF_model=1,
#                                    LS_model=None,
#                                    Closure_0_model=None,
#                                    Closure_1_model=None,
#                                    epsFact_density=epsFact_density,
#                                    stokes=False,
#                                    useVF=useVF,
#                                    useRBLES=useRBLES,
#                                    useMetrics=useMetrics,
#                                    eb_adjoint_sigma=1.0,
#                                    eb_penalty_constant=weak_bc_penalty_constant,
#                                    forceStrongDirichlet=ns_forceStrongDirichlet,
#                                    turbulenceClosureModel=ns_closure,
#                                    movingDomain=movingDomain,
#                                    nParticles = nParticles,
#                                    use_ball_as_particle = use_ball_as_particle,
#                                    particle_sdfList = particle_sdfList,
#                                    particle_velocityList = particle_velocityList,
#                                    )
class My_Coefficients(RANS2P.Coefficients):
    def __init__(self):
        RANS2P.Coefficients.__init__(self,
                                    epsFact=epsFact_viscosity,
                                    sigma=0.0,
                                    rho_0 = rho_0,
                                    nu_0 = nu_0,
                                    rho_1 = rho_1,
                                    nu_1 = nu_1,
                                    g=g,
                                    nd=nd,
                                    ME_model=V_model,
                                    VF_model=VF_model,
                                    LS_model=LS_model,
                                    Closure_0_model=None,
                                    Closure_1_model=None,
                                    epsFact_density=epsFact_density,
                                    stokes=False,
                                    useVF=useVF,
                                    useRBLES=useRBLES,
                                    useMetrics=useMetrics,
                                    eb_adjoint_sigma=1.0,
                                    eb_penalty_constant=weak_bc_penalty_constant,
                                    forceStrongDirichlet=ns_forceStrongDirichlet,
                                    turbulenceClosureModel=ns_closure,
                                    movingDomain=movingDomain,
                                    nParticles = nParticles,
                                    use_ball_as_particle = use_ball_as_particle,
                                    particle_sdfList = particle_sdfList,
                                    particle_velocityList = particle_velocityList,
                                    MOMENTUM_SGE=1.0,
                                    PRESSURE_SGE=1.0,
                                    VELOCITY_SGE=1.0,
                                    PRESSURE_PROJECTION_STABILIZATION=0.0
                                    )

    def preStep(self, t, firstStep=False):
        if firstStep:
            self.particle_centroids[0,0] = 0.2
            self.particle_centroids[0,1] = 0.2
            RANS2P.Coefficients.preStep(self, t, firstStep)

coefficients = My_Coefficients()

def getDBC_p(x,flag):
    if flag in [boundaryTags['top']]:
        return lambda x,t: 0.0
    else:
        return None
    
def getDBC_u(x,flag):
    if flag in [boundaryTags['top']]:######
        if ct.forceStrongDirichlet:
            return None
        else:
            return lambda x,t: 0.0 ###YY: Use  0.0 means get no-flux if the flow revers.

def getDBC_v(x,flag):
    if flag in [boundaryTags['top']]:######
        if ct.forceStrongDirichlet:
            return None
        else:
            return lambda x,t: 0.0 #####YY: Use  0.0 means get no-flux if the flow revers.

def getAFBC_p(x,flag): 
    if flag in [boundaryTags['top']]:######
        return None
    else:#### YY: u.n=0 slip boundary for front,back,bottom,left,right
        return lambda x,t: 0.0

def getAFBC_u(x,flag): 
    if flag in [boundaryTags['top']]:######
        return None
    else:#### YY: u.n=0 slip boundary for front,back,bottom,left,right
        return lambda x,t: 0.0

def getAFBC_v(x,flag): 
    if flag in [boundaryTags['top']]:######
        return None
    else:#### YY: u.n=0 slip boundary for front,back,bottom,left,right
        return lambda x,t: 0.0

def getDFBC_u(x,flag):
    if flag in [boundaryTags['front'],boundaryTags['back'],boundaryTags['left'],boundaryTags['right'],boundaryTags['bottom']]:
        return lambda x,t: 0.0
    elif flag in [boundaryTags['top']]:
        return None
    else:
        return lambda x,t: 0.0

def getDFBC_v(x,flag):
    if flag in [boundaryTags['front'],boundaryTags['back'],boundaryTags['left'],boundaryTags['right'],boundaryTags['bottom']]:
        return lambda x,t: 0.0
    elif flag in [boundaryTags['top']]:
        return lambda x,t: 0.0
    else:
        return lambda x,t: 0.0


dirichletConditions = {0:getDBC_p,
                       1:getDBC_u,
                       2:getDBC_v}

advectiveFluxBoundaryConditions =  {0:getAFBC_p,
                                    1:getAFBC_u,
                                    2:getAFBC_v}

diffusiveFluxBoundaryConditions = {0:{},
                                   1:{1:getDFBC_u},
                                   2:{2:getDFBC_v}}

class PerturbedSurface_p:
    def __init__(self,waterLevel):
        self.waterLevel=waterLevel
    def uOfXT(self,x,t):
        if signedDistance(x) < 0:
            return -(L[1] - self.waterLevel)*rho_1*g[1] - (self.waterLevel - x[1])*rho_0*g[1]
        else:
            return -(L[1] - self.waterLevel)*rho_1*g[1]

class AtRest:
    def __init__(self):
        pass
    def uOfXT(self,x,t):
        return 0.0

initialConditions = {0:PerturbedSurface_p(waterLine_z),
                     1:AtRest(),
                     2:AtRest()}