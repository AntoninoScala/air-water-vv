from proteus.default_n import *
from proteus import (Context,
                     LinearAlgebraTools,
                     LinearSolvers,
                     NonlinearSolvers,
                     StepControl,
                     TimeIntegration
                     )
from proteus.mprans import VOF
import vof_p as physics
#from vof_p import *

ct = Context.get()
mesh = ct.domain.MeshOptions

# time stepping
runCFL = ct.runCFL

if ct.timeDiscretization is 'vbdf':
    timeIntegration = TimeIntegration.VBDF
    timeOrder=2
    stepController  = StepControl.Min_dt_cfl_controller
elif ct.timeDiscretization is 'flcbdf':
    timeIntegration = TimeIntegration.FLCBDF
    #stepController = FLCBDF_controller
    stepController  = StepControl.Min_dt_cfl_controller
    time_tol = 10.0*ct.vof_nl_atol_res
    atol_u = {0:time_tol}
    rtol_u = {0:time_tol}
else:
    timeIntegration = TimeIntegration.BackwardEuler_cfl
    stepController  = StepControl.Min_dt_cfl_controller

# mesh options
nLevels = ct.nLevels
parallelPartitioningType = mesh.parallelPartitioningType
nLayersOfOverlapForParallel = mesh.nLayersOfOverlapForParallel
restrictFineSolutionToAllMeshes = mesh.restrictFineSolutionToAllMeshes
triangleOptions = mesh.triangleOptions

elementQuadrature = ct.elementQuadrature
elementBoundaryQuadrature = ct.elementBoundaryQuadrature

femSpaces = {0:ct.basis}

massLumping       = False
numericalFluxType = VOF.NumericalFlux
conservativeFlux  = None
subgridError      = VOF.SubgridError(coefficients=physics.coefficients,
                                     nd=ct.domain.nd)
shockCapturing    = VOF.ShockCapturing(coefficients=physics.coefficients,
                                       nd=ct.domain.nd,
                                       shockCapturingFactor=ct.vof_shockCapturingFactor,
                                       lag=ct.vof_lag_shockCapturing)

fullNewtonFlag = True
multilevelNonlinearSolver = NonlinearSolvers.Newton
levelNonlinearSolver      = NonlinearSolvers.Newton

nonlinearSmoother = None
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

linear_solver_options_prefix = 'vof_'
levelNonlinearSolverConvergenceTest = 'r'
nonlinearSolverConvergenceTest = 'r'
linearSolverConvergenceTest = 'r-true'

tolFac      = 0.0
linTolFac   = 0.0
l_atol_res = 0.1*ct.vof_nl_atol_res
nl_atol_res = ct.vof_nl_atol_res
useEisenstatWalker = False

maxNonlinearIts = 50
maxLineSearches = 0

auxiliaryVariables = ct.domain.auxiliaryVariables['vof']
