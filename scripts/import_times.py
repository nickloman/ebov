#!/usr/bin/env python
import sys
import csv

import sqlite3
from Bio import SeqIO

con = sqlite3.connect(sys.argv[1])
con.row_factory = sqlite3.Row
cur = con.cursor()

def get_runs(dataset):
	if dataset == 'all':
		cur.execute("select ROWID, * from runs")
	else:
        	cur.execute("select ROWID, * from runs where runs.dataset = ?", (dataset,))
        return cur.fetchall()

runs = get_runs(sys.argv[2])

for row in runs:
	try:
		fh = open("times/%s.times.txt" % (row['batch'],))
	except:
		continue
	print "opened"

	cols = fh.readline().split("\t")

	cur.execute(
		"UPDATE runs SET start = ?, end = ?, duration = ?, num_reads_pass = ?, num_reads_fail = ? WHERE ROWID=?",
		(cols[2], cols[3], cols[4], cols[0], cols[1], row['ROWID'])
	)

con.commit()
