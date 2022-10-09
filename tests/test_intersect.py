import sys

sys.path.append("../Module/PyGLtools/")
from intersect import intersect2D
from pgltools_library import processFile, compare_test_outputs
import pytest
from pathlib import Path
from parametrization import Parametrization

ASSET_DIR = Path(__file__).parent

##can parameterize this in a sec


@Parametrization.autodetect_parameters()
@Parametrization.case(
    name="baseline",
    v=False,
    bA=False,
    allA=False,
    m=False,
    mc=False,
    u=False,
    wa=False,
    wb=False,
    wo=False,
    d=0,
    expected_results_file=str(
        ASSET_DIR / "fixtures/intersect/intersect_expected_results.pgl"
    ),
)
@Parametrization.case(
    name="dashV",
    v=True,
    bA=False,
    allA=False,
    m=False,
    mc=False,
    u=False,
    wa=False,
    wb=False,
    wo=False,
    d=0,
    expected_results_file=str(
        ASSET_DIR / "fixtures/intersect/intersect_expected_results.v.pgl"
    ),
)
@Parametrization.case(
    name="B_annotations",
    v=False,
    bA=True,
    allA=False,
    m=False,
    mc=False,
    u=False,
    wa=False,
    wb=False,
    wo=False,
    d=0,
    expected_results_file=str(
        ASSET_DIR / "fixtures/intersect/intersect_expected_results.bA.pgl"
    ),
)
@Parametrization.case(
    name="all_annotations",
    v=False,
    bA=False,
    allA=True,
    m=False,
    mc=False,
    u=False,
    wa=False,
    wb=False,
    wo=False,
    d=0,
    expected_results_file=str(
        ASSET_DIR / "fixtures/intersect/intersect_expected_results.allA.pgl"
    ),
)
@Parametrization.case(
    name="dashM",
    v=False,
    bA=False,
    allA=False,
    m=True,
    mc=False,
    u=False,
    wa=False,
    wb=False,
    wo=False,
    d=0,
    expected_results_file=str(
        ASSET_DIR / "fixtures/intersect/intersect_expected_results.m.pgl"
    ),
)
@Parametrization.case(
    name="dashMc",
    v=False,
    bA=False,
    allA=False,
    m=False,
    mc=True,
    u=False,
    wa=False,
    wb=False,
    wo=False,
    d=0,
    expected_results_file=str(
        ASSET_DIR / "fixtures/intersect/intersect_expected_results.mc.pgl"
    ),
)
@Parametrization.case(
    name="dashU",
    v=False,
    bA=False,
    allA=False,
    m=False,
    mc=False,
    u=True,
    wa=False,
    wb=False,
    wo=False,
    d=0,
    expected_results_file=str(
        ASSET_DIR / "fixtures/intersect/intersect_expected_results.u.pgl"
    ),
)
@Parametrization.case(
    name="dashWa",
    v=False,
    bA=False,
    allA=False,
    m=False,
    mc=False,
    u=False,
    wa=True,
    wb=False,
    wo=False,
    d=0,
    expected_results_file=str(
        ASSET_DIR / "fixtures/intersect/intersect_expected_results.wa.pgl"
    ),
)
@Parametrization.case(
    name="dashWb",
    v=False,
    bA=False,
    allA=False,
    m=False,
    mc=False,
    u=False,
    wa=False,
    wb=True,
    wo=False,
    d=0,
    expected_results_file=str(
        ASSET_DIR / "fixtures/intersect/intersect_expected_results.wb.pgl"
    ),
)
@Parametrization.case(
    name="dashWo",
    v=False,
    bA=False,
    allA=False,
    m=False,
    mc=False,
    u=False,
    wa=False,
    wb=False,
    wo=True,
    d=0,
    expected_results_file=str(
        ASSET_DIR / "fixtures/intersect/intersect_expected_results.wo.pgl"
    ),
)
@Parametrization.case(
    name="Distance_5,000",
    v=False,
    bA=False,
    allA=False,
    m=False,
    mc=False,
    u=False,
    wa=False,
    wb=False,
    wo=False,
    d=5000,
    expected_results_file=str(
        ASSET_DIR / "fixtures/intersect/intersect_expected_results.d5000.pgl"
    ),
)
@Parametrization.case(
    name="Distance_500,000",
    v=False,
    bA=False,
    allA=False,
    m=False,
    mc=False,
    u=False,
    wa=False,
    wb=False,
    wo=False,
    d=500000,
    expected_results_file=str(
        ASSET_DIR / "fixtures/intersect/intersect_expected_results.d500000.pgl"
    ),
)
def test_intersect_2d(v, bA, allA, m, mc, u, wa, wb, wo, d, expected_results_file):

    # get files
    headerA, A = processFile(str(ASSET_DIR / "fixtures/file.A.sorted.annotated.pgl"))

    _, B = processFile(str(ASSET_DIR / "fixtures/file.B.sorted.annotated.pgl"))

    args = {
        "v": v,
        "bA": bA,
        "allA": allA,
        "m": m,
        "mc": mc,
        "u": u,
        "wa": wa,
        "wb": wb,
        "wo": wo,
        "d": d,
    }

    results = intersect2D(A, B, args, headerA)
    results = sorted(results)

    new_header, expected_results = processFile(expected_results_file)

    test_results = compare_test_outputs(results, expected_results)

    assert test_results
