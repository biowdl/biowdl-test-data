human_male_female
=================

These data are created for pipelines that correctly use the ploidy of the X and
Y chromosome.

Files
+++++

Files for testing
-----------------

+ ``reference.fa``: A reference genome. With chromosomes ``22``, ``X`` and
  ``Y``.
+ ``bwa_index``: A folder containing the BWA index files
+ ``female``: A folder containing the female sample files.

  + ``female_R1.fastq.gz`` and ``female_R2.fastq.gz``: fastq files.
  + ``female.bam`` and ``female.bai``: Reads aligned to the reference.
+ ``male``: A folder containing the male sample files.

  + Same types of files as female.
+ ``expected.vcf``: The expected genotypes for female and male samples.
+ ``x_non_par.bed`` and ``y_non_par.bed`` files listing the non-PAR regions for
  X and Y in reference.fa.

Files involved in test-data creation
------------------------------------
+ ``GRCh38`` this folders contains chromosome 22, X and Y downloaded from
  ensembl. These are the GRCh38 build release 98.
+ ``extract.bed``: The regions from hg38 that were used to create
  ``reference.fa``.
+ ``female.ploidy.tsv``: ploidy for each chromosome in the female sample.
+ ``male.ploidy.tsv``: idem for male sample.
+ ``MD5SUMS``: checksums to check if data could be recreated reproducably.
+ ``mutations.vcf``: True mutations. Taking ploidy into account. Used to
  generate the fastq reads for the male and female samples.
+ ``Snakefile``: Workflow to recreate the data
+ Various ``.py`` files. used in test data creation.

Test data creation process
++++++++++++++++++++++++++

+ Chromosome 22, X and Y  were downloaded from ensembl. GRCh38 reference genome
  was used.
+ The chromosomes were concatenated together.
+ ``extract.bed`` was used to create a ``reference.fa``.
+ Using ``translocate.py`` a version of chromosome Y was created were the
  masked PAR region was replaced by the sequence of X.
+ Using select_chromosomes and cat a ``reference_unmasked_y.fa`` was created.
+ Using ``male.ploidy.tsv``, ``female.ploidy.tsv``, ``mutations.vcf``,
  ``reference_unmasked_y.fa`` and the `biotdg
  <https://github.com/biowdl/biotdg>`_ programm reads were created for the male
  and female sample.
+ Using BWA the fastq reads were aligned to reference.fa

