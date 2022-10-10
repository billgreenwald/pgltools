# Tutorial

## Provided files:

* file.A.bed
* file.A.pgl
* file.A.sorted.pgl
* file.B.bed
* file.B.pgl
* file.B.sorted.pgl
* test_sam.sam

## Sorting

The provided files are not sorted.  To begin use
```
pgltools sort2D file.A.pgl > file.A.sorted.pgl
pgltools sort2D file.B.pgl > file.B.sorted.pgl
```

From here, any 2D operations can be run on these files.  As syntax is similar from operation to operation, this tutorial will only cover a few.

## Intersecting

First, we will get the intersection of the two files
```
pgltools intersect -a file.A.sorted.pgl -b file.B.sorted.pgl > intersected.pgl
```

Next, we will filter the intersections to a single chromosome for Locus A.
```
pgltools window -a intersected.pgl -window1 chr10 > filtered.pgl
```

Finally, we will merge the contacts within 100kb (for example purposes)
```
pgltools merge -a filtered.pgl -d 100000 > final.pgl
```

Alternatively, these could be piped together.  From start to finish, we have the following:

```
pgltools intersect -a file.A.sorted.pgl -b file.B.sorted.pgl | pgltools window -stdInA -window1 chr10 | pgltools merge -stdInA > final.bed
```

## Using a SAM file

We can convert the provided sam to a pgl for use with other functions.
```
pgltools samTopgl -a test_sam.sam > reads.pgl
```

## Using a regular bed file

We can intersect a pgl file with a bed file via pgltools:
```
pgltools intersect1D -a file.A.sorted.pgl -b file.B.sorted.pgl
```
