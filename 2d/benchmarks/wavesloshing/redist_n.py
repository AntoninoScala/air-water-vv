from proteus.default_n import *
from proteus import (StepControl,
                     TimeIntegration,
                     NonlinearSolvers,
                     LinearSolvers,
                     LinearAlgebraTools,
                     NumericalFlux)
from proteus.mprans import RDLS
import redist_p as physics
from proteus import Context

ct = Context.get()
domain = ct.domain
nd = ct.domain.nd
mesh = domain.MeshOptions

# time stepping
runCFL = ct.runCFL

# mesh options
nLevels = ct.nLevels
parallelPartitioningType = mesh.parallelPartitioningType
nLayersOfOverlapForParallel = mesh.nLayersOfOverlapForParallel
restrictFineSolutionToAllMeshes = mesh.restrictFineSolutionToAllMeshes
triangleOptions = mesh.triangleOptions

elementQuadrature = ct.elementQuadrature
elementBoundaryQuadrature = ct.elementBoundaryQuadrature

nl_atol_res = ct.rd_nl_atol_res
tolFac = 0.0
linTolFac = 0.0
l_atol_res = 0.001*ct.rd_nl_atol_res

if ct.redist_Newton:
    timeIntegration = TimeIntegration.NoIntegration
    stepController = StepControl.Newton_controller
    maxNonlinearIts = 25
    maxLineSearches = 0
    nonlinearSolverConvergenceTest = 'r'
    levelNonlinearSolverConvergenceTest = 'r'
    linearSolverConvergenceTest = 'r-true'
    useEisenstatWalker = True
else:
    timeIntegration = TimeIntegration.BackwardEuler_cfl
    stepController = RDLS.PsiTC
    runCFL=1.0
    psitc['nStepsForce']=3
    psitc['nStepsMax']=25
    psitc['reduceRatio']=2.0
    psitc['startRatio']=1.0
    rtol_res[0] = 0.0
    atol_res[0] = ct.rd_nl_atol_res
    useEisenstatWalker = False
    maxNonlinearIts = 1
    maxLineSearches = 0
    nonlinearSolverConvergenceTest = 'rits'
    levelNonlinearSolverConvergenceTest = 'rits'
    linearSolverConvergenceTest = 'r-true'

femSpaces = {0:ct.basis}
       
massLumping       = False
numericalFluxType = NumericalFlux.DoNothing
conservativeFlux  = None
subgridError      = RDLS.SubgridError(coefficients=physics.coefficients,
                                      nd=ct.domain.nd)
shockCapturing    = RDLS.ShockCapturing(coefficients=physics.coefficients,
                                        nd=ct.domain.nd,
                                        shockCapturingFactor=ct.rd_shockCapturingFactor,
                                        lag=ct.rd_lag_shockCapturing)
fullNewtonFlag = True
multilevelNonlinearSolver  = NonlinearSolvers.Newton
levelNonlinearSolver       = NonlinearSolvers.Newton

nonlinearSmoother = NonlinearSolvers.NLGaussSeidel
linearSmoother    = None

matrix = LinearAlgebraTools.SparseMatrix

if ct.useOldPETSc:
    multilevelLinearSolver = LinearSolvers.PETSc
    levelLinearSolver      = LinearSolvers.PETSc
else:
    multilevelLinearSolver = LinearSolvers.KSP_petsc4py
    levelLinearSolver      = LinearSolvers.KSP_petsc4py
if ct.useSuperlu:
    multilevelLinearSolver = LinearSolvers.LU
    levelLinearSolver      = LinearSolvers.LU

linear_solver_options_prefix = 'rdls_'

auxiliaryVariables = ct.domain.auxiliaryVariables['redist']
