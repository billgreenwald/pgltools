import sys

from ..Module.PyGLtools.conveRt import conveRt
from ..Module.PyGLtools.pgltools_library import processFile, compare_test_outputs
import pytest
from pathlib import Path
from parametrization import Parametrization

ASSET_DIR = Path(__file__).parent

##can parameterize this in a sec
"sum", "min", "max", "absmin", "absmax", "mean", "median", "collapse", "distinct", "count", "count_distinct"


@Parametrization.autodetect_parameters()
@Parametrization.case(
    name="baseline",
    C=0,
    P=0,
    Q=0,
    expected_results_file=str(
        ASSET_DIR / "fixtures/conveRt/conveRt_expected_results.txt"
    ),
)
@Parametrization.case(
    name="C8",
    C=8,
    P=0,
    Q=0,
    expected_results_file=str(
        ASSET_DIR / "fixtures/conveRt/conveRt_expected_results.C8.txt"
    ),
)
@Parametrization.case(
    name="P8",
    C=0,
    P=8,
    Q=0,
    expected_results_file=str(
        ASSET_DIR / "fixtures/conveRt/conveRt_expected_results.P8.txt"
    ),
)
@Parametrization.case(
    name="Q8",
    C=0,
    P=0,
    Q=8,
    expected_results_file=str(
        ASSET_DIR / "fixtures/conveRt/conveRt_expected_results.Q8.txt"
    ),
)
def test_conveRt(C, P, Q, expected_results_file):

    # get files
    headerA, A = processFile(
        str(ASSET_DIR / "fixtures/conveRt/file.A.sorted.annotated.for_conveRt_test.pgl")
    )

    args = {
        "C": C,
        "P": P,
        "Q": Q,
    }

    results = conveRt(A, args)

    results = results.split("\n")

    expected_results = [line.strip() for line in open(expected_results_file)]

    for res, e_res in zip(results, expected_results):
        assert res == e_res
