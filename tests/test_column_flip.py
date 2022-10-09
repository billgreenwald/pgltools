import sys
sys.path.append('../Module/PyGLtools/')
from column_flip import formatbedpe
from pgltools_library import  processFile, compare_test_outputs
import pytest
from pathlib import Path
from parametrization import Parametrization

ASSET_DIR=Path(__file__).parent

##can parameterize this in a sec
def test_column_flip(capfd):

    #get files
    headerA,A=processFile(str(ASSET_DIR/"fixtures/file.A.pgl"))
    expected_results_file = str(ASSET_DIR/"fixtures/column_flip/column_flip_expected_results.pgl")

    formatbedpe(A,headerA)
    out, err = capfd.readouterr()

    # get the results from std out
    results =  [[x.encode() for x in (line.strip().split())] for line in out.split("\n")][:-1]

    #sort the data since in reaily we use unix sort for speed
    #this means split off the header, sort the rest, put it back
    results_header = [results[0]]
    results_not_header = sorted(results[1:],key=lambda x:(x[0],int(x[1]),int(x[2]),x[3],int(x[4]),int(x[5])))
    results = results_header
    results.extend(results_not_header)

    #compare to real results
    expected_results = [line.strip().split() for line in open(expected_results_file)]

    test_results = compare_test_outputs(results,expected_results)

    assert test_results
