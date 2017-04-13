# pgltools

pgltools is a software suite designed for working with pgl files.  pgl files are designed for working with paired-loci data, such as contacts from a Hi-C experiment.  All methods output to stdout.

## Software Dependencies

pgltools is written in Python 2.7, and does not require any external packages.  As such, all operations, except for coverage, have been tested in pypy.  Pypy is an alternative python compiler, and is recommended for use with this tool suite.  Pypy is available on most linux distributions, and can be installed via "apt-get" or "yum".  <b>By utilizing pypy, pgltools sees a 5-7x speed up on all operations, and about a 25% decrease in the amount of RAM utilized</b>.

pgltools will automatically detect if pypy is installed, and will run through pypy if so.  Otherwise, it will default to python.

## Installation:

To install pgltools, clone the directory to the desired location, and add the /sh folder to your system PATH variable.  Methods can then be called with pgltools [command].  To view the avaiable commands, or the available arguments for a command, call pgltools with no command, or call pgltools [command] with no arguments.

## The pgl file format:

The pgl file format consists of 6 columns, plus any additional annotations.  The six required columns are locus A chromosome, locus A start, locus A end, locus B chromosome, locus B start, locus B end.  After these six columns, any additional columns may be included as annotations.  These columns will be perserved by pgltools, and can be manipulated with pgltools merge.  As annotations are arbitrary, header lines may be indcluded in pgl files by starting a line with "#" and will be carried over from the "A" file when using pgltools methods.  **In addition to the six required columns, pgl files are formatted such that each locus A comes before its partner locus B.**  The included **formatpgl** operation will fix any loci violating this rule in addition to sorting the file.  Example pgl files are provided below:

<b>Proper Formatting</b>:
```
#some header information
#some more header information
chr10 1    100   chr10 1000 10000 Annotation1 Annotation2
chr10 1000 10000 chr11 1    100   Annotation1 Annotation2
chr11 100  1000  chr11 2000 2200  Annotation1 Annotation2
...
```

<b>Improprer Formatting</b> (locus A comes after locus B):
```
chr10 1000 10000 chr10 1 100 Annotation1 Annotation2
...
```

## Methods:

## File Formatting and Converting Operations:

### formatpgl:

Converts a bedpe (as defined by bedtools) or similarly formated file to a sorted pgl file:
```
pgltools formatpgl [FILE]
```
Example, storing output to output.pgl:
```
pgltools formatpgl myFile.bedpe > output.pgl
```

### browser:

Formats a pgl file for viewing in the UCSC Genome Browser:
```
pgltools browser [options]
```
options:
```
-a [FILE]:  use [FILE] as input.  
-stdInA:  use stdin as input file.
-N [COLUMN_NUMBER]:  Specify column for naming entry.  If not given, entries are named Contact_#
-S [COLUMN_NUMBER]:  Specify column for scoring entry.  If not given, entries are scored uniformly
-R [COLUMN_NUMBER]:  Specify column for coloring entry.  If not given, entries are all colored black
-P [COLUMN_NUMBER]:  Specify column for pValue of entry.  If not given, pValue is ignored
-Q [COLUMN_NUMBER]:  Specify column for qValue of entry.  If not given, qValue is ignored
-tN [COLUMN_NUMBER]: Track name. If not given, track is named "pgl_track"
```
Example, storing output to output.bed:
```
pgltools browser myFile.pgl > output.bed
```

### conveRt:

Formats a pgl file for use with the GenomicInteractions R package.  Use the "chiapet.tool" format while importing.  Syntax:
```
pgltools conveRt [options]
```
options:
```
-a [FILE]:  use [FILE] as input.  
-stdInA:  use stdin as input file.
-N [COLUMN_NUMBER]:  Specify column for read counts.  If not given, counts are set to 0
-P [COLUMN_NUMBER]:  Specify column for scoring entry.  If not given, pValues are set to 0
-Q [COLUMN_NUMBER]:  Specify column for coloring entry.  If not given, q Values are set to 0
```
Example, storing output to output.pgl:
```
pgltools conveRt myFile.pgl > output.chiapetTool
```

### sort2D:
Sorts a pgl file.  A sorted pgl file is sorted by columns 1-6 in order with columns 1 and 4 treated as strings.  The sort2D file will not flip paired-loci that have locus B occuring before locus A as a pgl file is required to follow this format.  If a file does not follow this formatting, use the "formatpgl" operation.  Most commands below require sorted files.  Syntax:
```
pgltools sort2D [FILE]
```
Example, storing output to output.pgl:
```
pgltools sort2D myFile.pgl > output.pgl
```

### sort1D
Sorts a bed file as required for pgl tools.  A sorted bed file is sorted by columns 1-3 in order with column 1 treated as a string.  Syntax:
```
pgltools sort1D [FILE]
```

## 2D Operations:

![pgltools merge](/Images/Merge.PNG?raw=true)
Merges adjacent loci within a pgl file.  Requires sorted input. All operations can only utilize the annotation columns, except count.  If no annotations are present in the file, count can be used by passing -c 0.  If annotations are present, use any annotation column or -c 0.  A header will be automatically generated for the resulting file unless -noH is used.  Syntax:
```
pgltools merge [options]
```
options:
```
-a [FILE]:  use [FILE] as input.  
-stdInA:  use stdin as input file.
-c [COLUMN_NUMBER]:  perform an operation on the given column when merged
-o [OPERATION]:  perform the specified operation when merging.  operations listed below
-delim: change the delimeter for -o collapse and -o distinct.  Default is ","
-d: Distance allowed between loci for merging.  default 0
-noH: Do not create a header for the output file.
```
operations (*NOTE* that the program assumes you have passed columns with correct types for the desired operations).  A comma separated list may be given (ie -c 10,10,11,12 -o sum,min,sum,collapse):  
* sum -- sum the values from the specified column.  *Numeric*
* min -- find the minimum value from the specified column.  *Numeric*
* max -- find the maximum value from the specified column.  *Numeric*
* absmin -- find the minimum magintude value and report the signed value (ie [-1,-7,9] will report -1). *Numeric*
* absmax -- find the maximum magintude value and report the signed value (ie [-1,-7,9] will report 9).  *Numeric*
* mean -- find the mean of the values from the specified column.  *Numeric*
* median -- find the median of the values from the specified column. *Numeric*
* collapse -- combine the annotations from the column as a comma separated list. *String*
* distinct -- combine the unique annotations from the column as a comma separated list. *String*
* count -- Return the number of merged loci.  *NA*
* count_distinct -- Return the number of unique annotations from the specified column. *String*

Example, storing output to output.pgl:
```
pgltools merge -a myFile.pgl -c 10,10,11,12 -o min,max,count,collapse -d 200 > output.pgl
```
Example, storing output to output.pgl, reading input from stdin:
```
[some command] | pgltools merge -stdInA myFile.pgl > output.pgl
```

![pgltools intersect](/Images/Intersect.PNG?raw=true)
Finds the overlapping loci of two pgl files.  If using -m or -mc, the seventh column will contain the id of the file the locus came from.  Requires sorted inputs.  Syntax:
```
pgltools intersect [options]
```
options:
```
-a [FILE]:  use [FILE] as input.  
-stdInA:  use stdin as input file.
-b [FILE]:  use [FILE] as input.  
-stdInB:  use stdin as input file.
-v:  Returns entries in A that do not overlap any entries in B
-m:  Returns the union of loci instead of the intersection of loci
-mc:  Returns only unions of loci where an overlap between files occurred
-u: Returns the original loci from A if an overlap occurs (ie report an overlap happened).  An entry will be generated per overlap.
-bA:  Keep the annotations from file B instead of file A
```
Example, storing output to output.pgl:
```
pgltools intersect -a myFile.pgl -b myOtherFile.pgl > output.pgl
```

![pgltools windowpgl](/Images/Window.PNG?raw=true)
Finds the loci with locus A overlapping window1 and locus B overlapping window2.  Alternatively, only 1 window can be provided.  Syntax:
```
pgltools intersect [options]
```
options:
```
-a [FILE]:  use [FILE] as input.  
-stdInA:  use stdin as input file.
-window1 [chr:start-stop]
-window2 [chr:start-stop]
```
Example, storing output to output.pgl:
```
pgltools windowpgl -a myFile.pgl -window1 chr1:1-10000 -window2 chr10:1000-100000 > output.pgl
```

![pgltools subtract](/Images/Subtract.PNG?raw=true)
Finds the parts of loci from file A that do not overlap loci from file B.  Requires sorted input. Syntax:
```
pgltools subtract [options]
```
options:
```
-a [FILE]:  use [FILE] as input.  
-stdInA:  use stdin as input file.
-b [FILE]:  use [FILE] as input.  
-stdInB:  use stdin as input file.
```
Example, storing output to output.pgl:
```
pgltools subtract -a myFile.pgl -b myOtherFile.pgl > output.pgl
```

![pgltools closest](/Images/Closest.PNG?raw=true)
Finds the closest loci in file B for each loci in file A.  Locus A chromosomes must match, and locus B chromosomes must match to be considered for distance.  If no loci share the same chromosomal composition, the paired-loci from file A will not be matched with a paired-loci from file B.  The output fil will have 12 columns, with annotations overwritten: the six columns from file A followed by the six columns from file B if a paired-loci was found, else 6 ".".  Syntax:
```
pgltools closest [options]
```
options:
```
-a [FILE]:  use [FILE] as input.  
-stdInA:  use stdin as input file.
-b [FILE]:  use [FILE] as input.  
-stdInB:  use stdin as input file.
```
Example, storing output to output.pgl:
```
pgltools closest -a myFile.pgl -b myOtherFile.pgl > output.pgl
```

![pgltools merge](/Images/Coverage.PNG?raw=true)
Finds the coverage of file B on file A.  Any overlap of loci are counted in coverage calculation.  Syntax:
```
pgltools coverage [options]
```
options:
```
-a [FILE]:  use [FILE] as input.  
-stdInA:  use stdin as input file.
-b [FILE]:  use [FILE] as input.  
-stdInB:  use stdin as input file.
```
Example, storing output to output.pgl:
```
pgltools coverage -a myFile.pgl -b myOtherFile.pgl > output.pgl
```

### sam2pgl:
Converts a sam file to a pgl file.  A single paired end sam file must be used where paired end reads have the same name, or have the same name leading up to a delimeter which can be specified.  File must be sorted on the read name column (first column).  Reads with two alignments will be transformed into paired-loci.  Reads with greater than two alignments (which can occur in Hi-C from multiple contacts) will use the furthest end points on both chromosomes.  If all reads align to the same chromosomes, the specified insert size will be used to split apart loci ends.  If all read alignments are within the insert size, no paired-loci entry will be generated in the resulting pgl file.  Single alignment reads will be ignored.  As of now, soft-clipped reads are not supported. The sam file Syntax:
```
pgltools sam2pgl [options]
```
options:
```
-a [FILE]:  convert [FILE] to a pgl file.  
-stdInA:  convert the sam file piped from stdin to a pgl file.
-delim [DELIM]:  specify the delimeter in the read name
-ins [INT] : specify the insert size for multiple alignments to a single chromosome.  Default 1000
```
Example, storing output to output.pgl:
```
pgltools sam2pgl -a myFile.sam > output.pgl
```
Example, storing output to output.pgl, using BAM and samtools with a pipe:
```
samtools view myFile.sam | pgltools sam2pgl -stdInA > output.pgl
```

### expand:
Expands the start and end of both loci for each loci by the provided distance.  A genome file can be provided to prevent invalid positions from occuring within the file.  Syntax:
```
pgltools expand [options]
```
options:
```
-a [FILE]:  use [FILE] as input.  
-stdInA:  use stdin as input file.
-d [INT]:  size to expand by.  
-g [FILE]:  genome file formatted as below.
```
Genome file formatting:
```
chr1 endPosition
chr2 endPosition
chr3 endPosition
...
```
Example, storing output to output.pgl:
```
pgltools expand -a myFile.pgl -d 200 -g myGenomeFile > output.pgl
```

## 1D Operations:

![pgltools intersect1D](/Images/Intersect1D.PNG?raw=true)
Finds the intersection of loci from a pgl file and a standard bed file.  Following the standard 6 columns, the seventh column holds the locus (A, B, or AB) the bed region overlapped. Requires sorted inputs. Syntax:
```
pgltools intersect1D [options]
```
options:
```
-a [bed2dFILE]:  use [bed2dFILE] as input.  
-stdInA:  use stdin as input file.
-b [bedFILE]:  use [bedFILE] as input.  
-stdInB:  use stdin as input file.
-bA:  Keep annotations from the bed file rather than the pgl file
-allA:  Keep the annotation from both files.  Will output annotations from pgl followed by bed
-aL:  Prints the original loci from A upon finding overlapping region rather than the intersection
-pA [INT]:  Adds [INT] to end of each loci and subtracts [INT] from start of loci in pgl
-pB [INT]:  Adds [INT] to end of each region and subtracts [INT] from start of each region in bed
```
Example, storing output to output.pgl:
```
pgltools intersect1D -a myFile.pgl -b myOtherFile.bed > output.pgl
```

![pgltools subtract1D](/Images/Subtract1D.PNG?raw=true)
Finds the parts of loci from file A that do not overlap regions from file B.  Requires sorted input.  Syntax:
```
pgltools subtract [options]
```
options:
```
-a [bed2dFILE]:  use [bed2dFILE] as input.  
-stdInA:  use stdin as input file.
-b [bedFILE]:  use [bedFILE] as input.  
-stdInB:  use stdin as input file.
```
Example, storing output to output.pgl:
```
pgltools subtract1D -a myFile.pgl -b myOtherFile.bed > output.pgl
```

![pgltools closest1D](/Images/Closest1D.PNG?raw=true)
Finds the closest region in bed file B for each loci in file A.  Syntax:
```
pgltools closest [options]
```
options:
```
-a [bed2dFILE]:  use [bed2dFILE] as input.  
-stdInA:  use stdin as input file.
-b [bedFILE]:  use [bedFILE] as input.  
-stdInB:  use stdin as input file.
```
Example, storing output to output.pgl:
```
pgltools closest1D -a myFile.pgl -b myOtherFile.bed > output.pgl
```
