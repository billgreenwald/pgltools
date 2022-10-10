import sys

from ..Module.PyGLtools.subtract1D import subtract1D
from ..Module.PyGLtools.pgltools_library import processFile, processBedFile, compare_test_outputs
import pytest
from pathlib import Path
from parametrization import Parametrization

ASSET_DIR = Path(__file__).parent

##can parameterize this in a sec


@Parametrization.autodetect_parameters()
@Parametrization.case(
    name="baseline",
    expected_results_file=str(
        ASSET_DIR / "fixtures/subtract1D/subtract1D_expected_results.pgl"
    ),
)
def test_subtract_1d(expected_results_file):

    # get files
    headerA, A = processFile(str(ASSET_DIR / "fixtures/file.A.sorted.annotated.pgl"))

    headerB, B = processBedFile(str(ASSET_DIR / "fixtures/file.B.annotated.bed"))

    args = {}

    results = subtract1D(A, B, args, headerA)
    results = sorted(results)

    new_header, expected_results = processFile(expected_results_file)

    test_results = compare_test_outputs(results, expected_results)

    assert test_results
