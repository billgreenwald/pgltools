import sys

sys.path.append("../Module/PyGLtools/")
from merge import merge
from pgltools_library import processFile, compare_test_outputs
import pytest
from pathlib import Path
from parametrization import Parametrization

ASSET_DIR = Path(__file__).parent

##can parameterize this in a sec
"sum", "min", "max", "absmin", "absmax", "mean", "median", "collapse", "distinct", "count", "count_distinct"


@Parametrization.autodetect_parameters()
@Parametrization.case(
    name="baseline",
    o="%#$",
    c="%#$",
    delim=",",
    d=0,
    noH=False,
    expected_results_file=str(ASSET_DIR / "fixtures/merge/merge_expected_results.pgl"),
)
@Parametrization.case(
    name="distance_5,000",
    o="%#$",
    c="%#$",
    delim=",",
    d=5000,
    noH=False,
    expected_results_file=str(
        ASSET_DIR / "fixtures/merge/merge_expected_results.d5000.pgl"
    ),
)
@Parametrization.case(
    name="distance_500,000",
    o="%#$",
    c="%#$",
    delim=",",
    d=500000,
    noH=False,
    expected_results_file=str(
        ASSET_DIR / "fixtures/merge/merge_expected_results.d500000.pgl"
    ),
)
@Parametrization.case(
    name="no_header",
    o="%#$",
    c="%#$",
    delim=",",
    d=0,
    noH=True,
    expected_results_file=str(
        ASSET_DIR / "fixtures/merge/merge_expected_results.noH.pgl"
    ),
)
@Parametrization.case(
    name="operation_distinct",
    o="distinct",
    c="8",
    delim=",",
    d=50000,
    noH=True,
    expected_results_file=str(
        ASSET_DIR / "fixtures/merge/merge_expected_results.op_distinct.pgl"
    ),
)
@Parametrization.case(
    name="operation_sum",
    o="sum",
    c="8",
    delim=",",
    d=50000,
    noH=True,
    expected_results_file=str(
        ASSET_DIR / "fixtures/merge/merge_expected_results.op_sum.pgl"
    ),
)
@Parametrization.case(
    name="operation_min",
    o="min",
    c="8",
    delim=",",
    d=50000,
    noH=True,
    expected_results_file=str(
        ASSET_DIR / "fixtures/merge/merge_expected_results.op_min.pgl"
    ),
)
@Parametrization.case(
    name="operation_max",
    o="max",
    c="8",
    delim=",",
    d=50000,
    noH=True,
    expected_results_file=str(
        ASSET_DIR / "fixtures/merge/merge_expected_results.op_max.pgl"
    ),
)
@Parametrization.case(
    name="operation_absmin",
    o="absmin",
    c="8",
    delim=",",
    d=50000,
    noH=True,
    expected_results_file=str(
        ASSET_DIR / "fixtures/merge/merge_expected_results.op_absmin.pgl"
    ),
)
@Parametrization.case(
    name="operation_absmax",
    o="absmax",
    c="8",
    delim=",",
    d=50000,
    noH=True,
    expected_results_file=str(
        ASSET_DIR / "fixtures/merge/merge_expected_results.op_absmax.pgl"
    ),
)
@Parametrization.case(
    name="operation_mean",
    o="mean",
    c="8",
    delim=",",
    d=50000,
    noH=True,
    expected_results_file=str(
        ASSET_DIR / "fixtures/merge/merge_expected_results.op_mean.pgl"
    ),
)
@Parametrization.case(
    name="operation_median",
    o="median",
    c="8",
    delim=",",
    d=50000,
    noH=True,
    expected_results_file=str(
        ASSET_DIR / "fixtures/merge/merge_expected_results.op_median.pgl"
    ),
)
@Parametrization.case(
    name="operation_collapse",
    o="collapse",
    c="8",
    delim=",",
    d=50000,
    noH=True,
    expected_results_file=str(
        ASSET_DIR / "fixtures/merge/merge_expected_results.op_collapse.pgl"
    ),
)
@Parametrization.case(
    name="operation_count",
    o="count",
    c="8",
    delim=",",
    d=50000,
    noH=True,
    expected_results_file=str(
        ASSET_DIR / "fixtures/merge/merge_expected_results.op_count.pgl"
    ),
)
@Parametrization.case(
    name="operation_count_distinct",
    o="count_distinct",
    c="8",
    delim=",",
    d=50000,
    noH=True,
    expected_results_file=str(
        ASSET_DIR / "fixtures/merge/merge_expected_results.op_count_distinct.pgl"
    ),
)
@Parametrization.case(
    name="multi_op",
    o="count_distinct,count,collapse",
    c="8,8,7",
    delim=",",
    d=50000,
    noH=True,
    expected_results_file=str(
        ASSET_DIR / "fixtures/merge/merge_expected_results.multi_op.pgl"
    ),
)
@Parametrization.case(
    name="op_delim",
    o="distinct",
    c="8",
    delim=";",
    d=50000,
    noH=True,
    expected_results_file=str(
        ASSET_DIR / "fixtures/merge/merge_expected_results.op_delim.pgl"
    ),
)
def test_merge(o, c, delim, d, noH, expected_results_file):

    # get files
    headerA, A = processFile(
        str(ASSET_DIR / "fixtures/merge/file.A.sorted.annotated.for_merge_test.pgl")
    )

    args = {"o": o, "c": c, "delim": delim, "d": d, "noH": noH}

    results = merge(A, args, headerA)
    results = sorted(results)

    new_header, expected_results = processFile(expected_results_file)

    test_results = compare_test_outputs(results, expected_results)

    assert test_results
