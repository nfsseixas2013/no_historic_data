#!/bin/bash

for i in $(seq 1 10);
do
	
	nome=no_historic_k_10_$i
	dir=/home/nilton/Arquivos/no_historic_data/Examples
	cd $dir
	python sim06.py  $nome $i
done
