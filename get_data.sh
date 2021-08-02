### THIS SCRIPT PRODUCES PREDICTIONS AND EVALUATES THEM FOR ALL MODELS WITH SEMEVAL-ENG PARAMETERS ###

## Download corpora and testsets ##
wget https://www.ims.uni-stuttgart.de/documents/ressourcen/experiment-daten/DURel.zip -nc -P testsets/
cd testsets/ && unzip -o semeval2020_ulscd_eng.zip && rm semeval2020_ulscd_eng.zip && cd ..
if [ ! -d corpora/semeval2020_ulscd_eng ];
then
    mkdir -p corpora/semeval2020_ulscd_eng/corpus1/
    mkdir -p corpora/semeval2020_ulscd_eng/corpus2/
    scripts/preprocess.sh testsets/semeval2020_ulscd_eng/corpus1/lemma/ corpora/semeval2020_ulscd_eng/corpus1/corpus1_preprocessed.txt 4
    scripts/preprocess.sh testsets/semeval2020_ulscd_eng/corpus2/lemma/ corpora/semeval2020_ulscd_eng/corpus2/corpus2_preprocessed.txt 4
    gzip corpora/semeval2020_ulscd_eng/corpus1/*
    gzip corpora/semeval2020_ulscd_eng/corpus2/*
fi
rm -r testsets/semeval2020_ulscd_eng/corpus1
rm -r testsets/semeval2020_ulscd_eng/corpus2

## Bring testsets in correct format ##
mkdir -p testsets/semeval2020_ulscd_eng/testset
cp -u testsets/semeval2020_ulscd_eng/targets.txt testsets/semeval2020_ulscd_eng/testset/targets.tsv
cut -f 2- testsets/semeval2020_ulscd_eng/truth/graded.txt > testsets/semeval2020_ulscd_eng/testset/graded.tsv
cut -f 2- testsets/semeval2020_ulscd_eng/truth/binary.txt > testsets/semeval2020_ulscd_eng/testset/binary.tsv
