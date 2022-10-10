import sys

from ..Module.PyGLtools.closest1D import closest1D
from ..Module.PyGLtools.pgltools_library import (
    processFile,
    processBedFile,
    compare_test_outputs,
)
import pytest
from pathlib import Path
from parametrization import Parametrization

ASSET_DIR = Path(__file__).parent

##can parameterize this in a sec


@Parametrization.autodetect_parameters()
@Parametrization.case(
    name="baseline",
    dashB=False,
    expected_results_file=str(
        ASSET_DIR / "fixtures/closest1D/closest1D_expected_results.pgl"
    ),
)
@Parametrization.case(
    name="dashB",
    dashB=True,
    expected_results_file=str(
        ASSET_DIR / "fixtures/closest1D/closest1D_expected_results.ba.pgl"
    ),
)
def test_closest_1d(dashB, expected_results_file):

    # get files
    headerA, A = processFile(str(ASSET_DIR / "fixtures/file.A.sorted.annotated.pgl"))

    _, B = processBedFile(str(ASSET_DIR / "fixtures/file.B.sorted.annotated.pgl"))

    results = closest1D(A, B, {"ba": dashB})
    results = sorted(results)

    new_header, expected_results = processFile(expected_results_file)

    test_results = compare_test_outputs(results, expected_results)

    assert test_results
