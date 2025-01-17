from proteus.default_n import *
from proteus import (StepControl,
                     TimeIntegration,
                     NonlinearSolvers,
                     LinearSolvers,
                     LinearAlgebraTools)
from proteus.mprans import Kappa
import kappa_p as physics
from proteus import Context
ct = Context.get()
nd = ct.domain.nd

timeIntegration = TimeIntegration.BackwardEuler_cfl
stepController = StepControl.Min_dt_controller

femSpaces = {0:ct.basis}

massLumping       = False
numericalFluxType = Kappa.NumericalFlux
conservativeFlux  = None
subgridError      = Kappa.SubgridError(coefficients=physics.coefficients,
                                       nd=nd)
shockCapturing    = Kappa.ShockCapturing(coefficients=physics.coefficients,
                                         nd=nd,
                                         shockCapturingFactor=ct.kappa_shockCapturingFactor,
                                         lag=ct.kappa_lag_shockCapturing)

fullNewtonFlag  = True
multilevelNonlinearSolver = NonlinearSolvers.Newton
levelNonlinearSolver      = NonlinearSolvers.Newton

nonlinearSmoother = None
linearSmoother    = None
#printNonlinearSolverInfo = True
matrix = LinearAlgebraTools.SparseMatrix

if not ct.useOldPETSc and not ct.useSuperlu:
    multilevelLinearSolver = LinearSolvers.KSP_petsc4py
    levelLinearSolver      = LinearSolvers.KSP_petsc4py
else:
    multilevelLinearSolver = LinearSolvers.LU
    levelLinearSolver      = LinearSolvers.LU

linear_solver_options_prefix = 'kappa_'
levelNonlinearSolverConvergenceTest = 'r'#'rits'
linearSolverConvergenceTest         = 'r'#'rits'

tolFac = 0.0
linTolFac =0.0
l_atol_res = 0.001*ct.kappa_nl_atol_res
nl_atol_res = ct.kappa_nl_atol_res
useEisenstatWalker = True

maxNonlinearIts = 50
maxLineSearches = 0

auxiliaryVariables = ct.domain.auxiliaryVariables['kappa']
