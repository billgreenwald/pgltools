import sys

sys.path.append("../Module/PyGLtools/")
from expand import expand, _processGenome
from pgltools_library import processFile, compare_test_outputs
import pytest
from pathlib import Path
from parametrization import Parametrization

ASSET_DIR = Path(__file__).parent

##can parameterize this in a sec


@Parametrization.autodetect_parameters()
@Parametrization.case(
    name="50bp_noGenome",
    distance=50,
    genome_file=None,
    expected_results_file=str(
        ASSET_DIR / "fixtures/expand/expand_expected_results.50.g1.pgl"
    ),
)
@Parametrization.case(
    name="50bp_genome1",
    distance=50,
    genome_file=ASSET_DIR / "fixtures/file.A.genome.txt",
    expected_results_file=str(
        ASSET_DIR / "fixtures/expand/expand_expected_results.50.g1.pgl"
    ),
)
@Parametrization.case(
    name="50,000bp_genome1",
    distance=50000,
    genome_file=ASSET_DIR / "fixtures/file.A.genome.txt",
    expected_results_file=str(
        ASSET_DIR / "fixtures/expand/expand_expected_results.50000.g1.pgl"
    ),
)
@Parametrization.case(
    name="50bp_genome2",
    distance=50,
    genome_file=ASSET_DIR / "fixtures/file.A.genome2.txt",
    expected_results_file=str(
        ASSET_DIR / "fixtures/expand/expand_expected_results.50.g2.pgl"
    ),
)
@Parametrization.case(
    name="50,000bp_genome2",
    distance=50000,
    genome_file=ASSET_DIR / "fixtures/file.A.genome2.txt",
    expected_results_file=str(
        ASSET_DIR / "fixtures/expand/expand_expected_results.50000.g2.pgl"
    ),
)
def test_expand(distance, genome_file, expected_results_file):

    # get files
    headerA, A = processFile(str(ASSET_DIR / "fixtures/file.A.sorted.annotated.pgl"))
    if genome_file is not None:
        genome = _processGenome(str(genome_file))
    else:
        genome = {}

    # run the code
    results = expand(A, {"d": distance}, genome)

    # get what we expect
    new_header, expected_results = processFile(expected_results_file)

    # check we got what we expect
    for res, e_res in zip(results, expected_results):
        assert res == e_res
