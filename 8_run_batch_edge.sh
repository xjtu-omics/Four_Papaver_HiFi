namelist_dir='/home/shgao/home/Papaver_cen/V4/monomer_detection/HN1'
chr_number=11
work_dir='/home/shgao/home/Papaver_cen/V4/monomer_detection/HN1'
all_name_list_file=$namelist_dir'/namelist.filter.txt'

for ((i=1; i<=28; i++))
do
namelist_file=$namelist_dir'/namelist.'$i'.txt'

nohup /home/shgao/.conda/envs/SCAT/bin/python /home/shgao/home/Papaver_cen/V4/monomer_detection/getEdge.py -n $namelist_file -i $i -w $work_dir -a $all_name_list_file -c $chr_number &

done

