import sys

sys.path.append("../Module/PyGLtools/")
from ..Module.PyGLtools.coverage import coverage as pgltools_coverage
from pgltools_library import processFile, compare_test_outputs
import pytest
from pathlib import Path
from parametrization import Parametrization

ASSET_DIR = Path(__file__).parent

##can parameterize this in a sec


@Parametrization.autodetect_parameters()
@Parametrization.case(
    name="baseline",
    keep_zero=False,
    expected_results_file=str(
        ASSET_DIR / "fixtures/coverage/coverage_expected_results.pgl"
    ),
)
@Parametrization.case(
    name="keep_zero",
    keep_zero=True,
    expected_results_file=str(
        ASSET_DIR / "fixtures/coverage/coverage_expected_results.z.pgl"
    ),
)
def test_coverage(keep_zero, expected_results_file):

    # get files
    headerA, A = processFile(str(ASSET_DIR / "fixtures/file.A.sorted.annotated.pgl"))

    headerB, B = processFile(str(ASSET_DIR / "fixtures/file.B.sorted.annotated.pgl"))

    results = pgltools_coverage(A, B, headerA, {"z": keep_zero})
    results = sorted(results)

    new_header, expected_results = processFile(expected_results_file)

    test_results = compare_test_outputs(results, expected_results)

    assert test_results
