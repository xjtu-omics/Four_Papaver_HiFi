namelist_dir='/home/shgao/home/Papaver_cen/V4/monomer_detection/HN1'
ref='/home/shgao/home/Papaver_cen/V4/trf/ref/HN1.v2.4.fa'
work_dir='/home/shgao/home/Papaver_cen/V4/monomer_detection/HN1'
for ((i=1; i<=28; i++))
do
namelist_file=$namelist_dir'/namelist.'$i'.txt'

nohup /home/shgao/.conda/envs/SCAT/bin/python runSD.py -n $namelist_file -r $ref -w $work_dir &

done

