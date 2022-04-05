# GSTAr_mp
Multi-processor wrapper for the GSTAr sRNA aligner


This script basically just a python wrapper for running the small RNA transcriptome aligner GSTAr.pl (https://github.com/MikeAxtell/GSTAr). GSTAr just uses RNAplex from the ViennaRNA package as it's backbone and reports model RNA-RNA duplexes with minimal analyses.

**Warning** GSTAr comes with numerous warnings, as should any tool that might be used to model sRNA-transcript interactions. The results of this software should not be considered predictions and any hypothetical interactions **must** be confirmed through experimental evidence. A full list of these warnings can be found in the documentation: perldoc GSTAr.pl


**Dependencies (must be in PATH variable)**

RNAplex from the ViennaRNA suite (http://rna.tbi.univie.ac.at/)
GSTAr.pl (https://github.com/MikeAxtell/GSTAr)



