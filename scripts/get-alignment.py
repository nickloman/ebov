#!/usr/bin/env python

import sys
from Bio import SeqIO
#from Bio.Seq import Seq
#from Bio.SeqRecord import SeqRecord
from collections import defaultdict

def main():
	records = list(SeqIO.parse(sys.stdin, 'fasta'))
	ids = set([record.id for record in records])
	lens = set([len(record.seq) for record in records])
	if len(lens) != 1:
		print 'Sequence lengths not equal...'
		sys.exit()
	ignore = set(['-'])
	discrim = defaultdict(str)
	discrim_pos = []
	for posn in range(0, list(lens)[0]):
		ids_alleles = dict((record.id, record.seq[posn]) for record in records if record.seq[posn] not in ignore)
		if len(set(ids_alleles.values())) < 2 or (len(set(ids_alleles.values())) is 2 and 'N' in set(ids_alleles.values())):
			continue
		print >>sys.stderr, "%s\t%s" % (posn+1, ids_alleles.values())

		discrim_pos.append(posn)
		for each in ids_alleles:
			discrim[each] += ids_alleles[each]
		gapped = ids - set(ids_alleles.keys())
		for each in gapped:
			discrim[each] += 'N'

#	print >>sys.stderr, discrim_pos
	for each in discrim:
		print ">%s\n%s" % (each, discrim[each])

if __name__ == '__main__':
	main()
