#!/bin/bash

for i in $(seq 1 40);
do
	
	nome=sim$i
	dir=/home/nilton/Arquivos/EON_SIMULATOR/Examples
	cd $dir
	python sim01.py  $nome $i
done
