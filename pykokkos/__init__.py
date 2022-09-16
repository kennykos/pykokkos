import atexit
from typing import Optional

from pykokkos.runtime import runtime_singleton
from pykokkos.core import CompilationDefaults, Runtime
from pykokkos.interface import *
from pykokkos.kokkos_manager import (
    initialize, finalize,
    get_default_space, set_default_space,
    get_default_precision, set_default_precision,
    is_uvm_enabled, enable_uvm, disable_uvm
)

initialize()
from pykokkos.lib.ufuncs import (reciprocal,
                                 log,
                                 log2,
                                 log10,
                                 log1p,
                                 sqrt,
                                 sign,
                                 add,
                                 subtract,
                                 multiply,
                                 matmul,
                                 divide,
                                 negative,
                                 positive,
                                 power,
                                 fmod,
                                 square,
                                 greater,
                                 logaddexp,
                                 true_divide,
                                 logaddexp2,
                                 floor_divide,
                                 sin,
                                 cos,
                                 tan,
                                 logical_and,
                                 logical_or,
                                 logical_xor,
                                 logical_not,
                                 fmax,
                                 fmin,
                                 exp,
                                 exp2,
                                 argmax,
                                 unique,
                                 var,
                                 in1d,
                                 mean,
                                 sum,
                                 divide_num,
                                 mul0d,
                                 add_num,
                                 array,
                                 transpose,
                                 power2,
                                 index,
                                 findMax,
                                 searchsorted,
                                isinf,
                                isnan)
from pykokkos.lib.info import iinfo, finfo
from pykokkos.lib.create import zeros
from pykokkos.lib.util import all, any
from pykokkos.lib.constants import e, pi, inf, nan

runtime_singleton.runtime = Runtime()
defaults: Optional[CompilationDefaults] = runtime_singleton.runtime.compiler.read_defaults()

if defaults is not None:
    set_default_space(ExecutionSpace[defaults.space])
    if defaults.force_uvm:
        enable_uvm()
    else:
        disable_uvm()

def cleanup():
    """
    Delete the runtime instance to avoid Kokkos errors caused by
    deallocation after calling Kokkos::finalize()
    """

    global runtime_singleton
    del runtime_singleton.runtime
    del runtime_singleton

    from pykokkos.interface.parallel_dispatch import workunit_cache
    workunit_cache.clear()

# Will be called in reverse order of registration (cleanup then finalize)
atexit.register(finalize)
atexit.register(cleanup)
