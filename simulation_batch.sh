#!/bin/bash

for i in $(seq 1 10);
do
	
	nome=dddm_k_60_$i
	dir=/home/nilton/Arquivos/EON_SIMULATOR_k_60/Examples
	cd $dir
	python sim06.py  $nome $i
done
