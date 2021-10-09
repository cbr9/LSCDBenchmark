: '
# Make predictions
testsets=(testsets/*)
outdir=predictions
mkdir -p $outdir
for testset in "${testsets[@]}"
do
    #echo $testset
    datas=($testset/*/*.csv)
    for data in "${datas[@]}"
    do
	echo $data
	outfile="${data/testsets/$outdir}"
	#echo $outfile
	mkdir -p $(dirname "$outfile")
	python make_prediction.py gold $data $testset $outfile
    done
done
'

outdir=results
mkdir -p $outdir
python evaluate.py testsets predictions $outdir


