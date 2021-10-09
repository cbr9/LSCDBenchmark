: '
'
rm -rf testsets_source
rm -rf testsets

# Download gold data in WUG format
#wget https://zenodo.org/record/5541340/files/durel.zip -nc -P testsets_source/
wget https://zenodo.org/record/5544198/files/dwug_de.zip -nc -P testsets_source/

# Unzip data
testsets=(testsets_source/*)
for testset in "${testsets[@]}"
do
    cd testsets_source/ && unzip -o $(basename "$testset") && rm -r $(basename "$testset") && cd ..
done

# Transform, split and clean data
testsets=(testsets_source/*)
outdir=testsets
mkdir -p $outdir
for testset in "${testsets[@]}"
do
    echo $testset
    python make_data.py $testset $(basename "${testset%.*}") $outdir
done
