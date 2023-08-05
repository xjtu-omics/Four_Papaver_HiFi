namelist_dir='/home/shgao/home/Papaver_cen/V4/monomer_detection/HN1'
split_chr_dir='/home/shgao/home/Papaver_cen/V4/split_ref/HN1'
chr_number=11
work_dir='/home/shgao/home/Papaver_cen/V4/monomer_detection/HN1'

for ((i=1; i<=28; i++))
do
namelist_file=$namelist_dir'/namelist.'$i'.txt'

nohup /home/shgao/.conda/envs/SCAT/bin/python /home/shgao/home/Papaver_cen/V4/monomer_detection/run_lastz.py -n $namelist_file -s $split_chr_dir -c $chr_number -w $work_dir &

done

