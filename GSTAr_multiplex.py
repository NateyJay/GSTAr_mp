#!/usr/bin/env python3


import sys
import os
from tqdm import tqdm
from subprocess import Popen, PIPE
import queue
# from threading import Thread, Lock
import argparse
import random
import string

from multiprocessing import Lock, Process, Queue, current_process, Pool
import time
import shutil
from datetime import datetime
from os.path import isfile



version = 1.0



def call_gstar(job):
	# global number_completed

	i, sRNA_name, sRNA_seq = job
	txome = os.path.abspath(input_txome)

	lock.acquire()
	print(job)
	print("Txome:", input_txome)

	lock.release()

	temp_folder = f"{master_temp}/temp_{i}"

	try:
		os.mkdir(temp_folder)
	except OSError:
		pass

	input_sRNAs = f"{temp_folder}/query.fa"
	with open(input_sRNAs, 'w') as f:
		print(">" + sRNA_name, file=f)
		print(sRNA_seq, file=f)




	args = ["GSTAr.pl", "-q", "-t", input_sRNAs.split("/")[-1], input_txome]


	call = f"GSTAr.pl -q -t query.fa {txome}"

	# print(call)
	# print(temp_folder)
	p = Popen(call.split(), cwd=temp_folder, stdout=PIPE, stderr=PIPE, encoding='utf-8')

	out, err = p.communicate()


	# print(out)
	# for l in out:
	# 	if l[0] != "#":
	# 		print("\t".join(out))

	lock.acquire()
	# number_completed += 1
	print(sRNA_name, flush=True)

	out = out.strip().split("\n")
	while True:
		if "Query	Transcript" in out.pop(0):
			break


	with open(output_file, 'a') as outf:
		for line in out:
			print(line.strip(), file=outf)
	# print(out)

	lock.release()




def init(l, m, t, o):
    global lock
    global input_txome
    global master_temp
    global output_file
    lock = l
    master_temp = m
    input_txome = t
    output_file = o


def main_script():


	seed = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))

	parser = argparse.ArgumentParser()
	parser.add_argument('-q', '--queries', nargs="?", type=str, required=True, 
		help="queries file in fasta format")
	parser.add_argument('-t', '--targets', nargs="?", type=str, required=True,
		help="target transcripts file in fasta format")
	parser.add_argument('-o', '--output_file', nargs="?", type=str, required=True,
		help='Output file location')
	parser.add_argument('-p', '--threads', nargs="?", type=int, required=True,
		help='number of threads')

	# parser.add_argument('-o', '--outputfile', nargs='?', type=int, required=True)

	args = parser.parse_args()

	input_txome = args.targets
	sRNA_input = args.queries
	threads = int(args.threads)
	output_file = args.output_file
	# outputfile = args.outputfile

	assert threads > 0, "FATAL: 'threads' must be > 0"
	assert os.path.isfile(input_txome), "FATAL: transcriptome file {} could not be read!".format(input_txome)
	assert os.path.isfile(input_txome), "FATAL: sRNA file {} could not be read!".format(sRNA_input)

	number_completed = 0


	header_printed = False


	sRNA_dict = {}
	# sRNA_input = "../nbe_clustering/05out-nbe.clusters.HI.fa"




	version = '2.0'
	
	now = datetime.now()
	now = now.strftime("%Y/%m/%d-%H:%M:%S")


	assert not isfile(output_file), "output_file already exists!"
	
	with open(output_file, 'w') as outf:
		print(f'''# GSTAr version 1.0
# mulitplex version {version}
# {now}
# Queries: {sRNA_input}
# Transcripts: {input_txome}
# Minimum Free Energy Ratio cutoff (option -r): 0.65
# Sorted by: MFEratio
# Output Format: Tabular
Query	Transcript	TStart	TStop	TSlice	MFEperfect	MFEsite	MFEratio	AllenScore	Paired	Unpaired	Structure	Sequence''', file=outf)




	master_temp = "temp_files_{}".format(seed)
	try:
		os.mkdir(master_temp)
	except OSError:
		pass

	with open(sRNA_input, 'r') as f:
		for line in f:
			line = line.strip()
			if line[0] == ">":
				header = line[1:]
				sRNA_dict[header] = ''
			else:
				sRNA_dict[header] += line




	lock = Lock()
	pool = Pool(initializer=init, 
		initargs=(lock, master_temp, input_txome, output_file,), 
		processes=threads)


	jobs = []

	for i, sRNA_name in enumerate(sRNA_dict.keys()):


		sRNA_seq = sRNA_dict[sRNA_name]
		jobs.append((i, sRNA_name, sRNA_seq))



	pool.map(call_gstar, jobs)

	pool.close()
	pool.join()


	print(f"cleaning up temp folder: {master_temp}")
	shutil.rmtree(master_temp)





if __name__ == '__main__':
	main_script()

