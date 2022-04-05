## GSTAr_mp
*-- Multi-processor wrapper for the GSTAr sRNA aligner --*

This script basically just a python wrapper for running the small RNA transcriptome aligner GSTAr.pl (https://github.com/MikeAxtell/GSTAr). GSTAr just uses RNAplex from the ViennaRNA package as it's backbone and reports model RNA-RNA duplexes with minimal analyses.

#### Why?
GSTAr.pl is slow... Producing a set of putative alignments over entire transcriptomes becomes unfeasable with high numbers of small RNAs (>1000). This uses the multiprocessing module in python to scale to the number of available threads.


#### How? 
`GSTAr_multiplex.py -q [sRNAs.fa] -t [transcriptome.fa] -o [OUTPUT_FILE] -p [THREADS]` 
 
Note: like GSTAr.pl, this will only except a transcriptome with no whitespace in the header.

#### Warning 
GSTAr comes with numerous warnings, as should any tool that might be used to model sRNA-transcript interactions. The results of this software should not be considered predictions and any hypothetical interactions **must** be confirmed through experimental evidence. 

A full list of these warnings can be found in the documentation: `perldoc GSTAr.pl`


#### Dependencies (must be in PATH variable)
`RNAplex` from the ViennaRNA suite (http://rna.tbi.univie.ac.at/)  
`GSTAr.pl` (https://github.com/MikeAxtell/GSTAr)



