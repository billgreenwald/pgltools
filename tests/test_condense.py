import sys

sys.path.append("../Module/PyGLtools/")
from condense import _condense
from pgltools_library import processFile, compare_test_outputs
import pytest
from pathlib import Path
from parametrization import Parametrization

ASSET_DIR = Path(__file__).parent

##can parameterize this in a sec
def test_condense(capfd):

    # get files
    args = {
        "a": str(ASSET_DIR / "fixtures/file.A.sorted.annotated.pgl"),
        "stdInA": False,
    }
    expected_results_file = str(
        ASSET_DIR / "fixtures/condense/condense_expected_results.bed"
    )

    _condense(args)
    out, err = capfd.readouterr()

    # get the results from std out
    results = [[x for x in (line.strip().split())] for line in out.split("\n")][:-1]

    # compare to real results
    expected_results = [line.strip().split() for line in open(expected_results_file)]

    test_results = compare_test_outputs(results, expected_results)

    assert test_results
