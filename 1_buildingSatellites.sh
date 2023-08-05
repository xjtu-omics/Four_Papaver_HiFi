sp="HN1"
chr_number=11

PYTHON="/home/shgao/.conda/envs/SCAT/bin/python"
script_dir="/home/shgao/home/Papaver_cen/V4/monomer_detection"
trf_dir="/home/shgao/home/Papaver_cen/V4/trf/"$sp
outdir=$script_dir"/"$sp

echo "processTRFforlastz.py"
$PYTHON $script_dir"/processTRFforlastz.py" -t $trf_dir -c $chr_number -o $outdir
echo "filterNamelist.py and splitNamelist.py 28 worker"
$PYTHON $script_dir"/filterNamelist.py" -n $outdir"/namelist.txt" -w $outdir
$PYTHON $script_dir"/splitNamelist.py" -n $outdir"/namelist.filter.txt" -o $outdir
