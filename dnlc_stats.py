#!/usr/bin/python

from __future__ import division
import fileinput
import re

# this script takes "kstat -T d -p -n dnlcstats 1" as it's input and then prints hits, misses as well as hit%
# 1st line out output is average since boot next ones are based on interval
# to run use ./dnlc_stats.py <input_file>
# daniel.borek@nexenta.com

# the below variable names are relevant at the time stats are calculated/printed by this script
current_hits = 0
current_misses = 0
previous_hits = 0
previous_misses = 0
readings = 0 
hit_p = 0
hit_in = 0
miss_in = 0

for line in fileinput.input():
	if re.match(r'January|February|March|April|May|Jun|July|August|September|October|November|December.*', line,):
		readings = readings + 1
		if readings == 1:
			print line, "Hits \t\tMisses\t\t Hit %"
		if readings == 10:
			readings = 0
	if re.match(r'unix.*:hits', line,):
		current_hits = int(re.search(r'\s\d*',line).group())
	if re.match(r'unix.*:misses', line,):
		current_misses = int(re.search(r'\s\d*',line).group())
		hit_in = current_hits - previous_hits
		miss_in = current_misses - previous_misses
		if miss_in == 0:
			print "%d\t\t%d\t\tNA" % (hit_in, miss_in)
		else:
			hit_p = hit_in/(hit_in+miss_in)*100
			print "%d\t\t%d\t\t%2.2f" % (hit_in, miss_in, hit_p)

		previous_hits = current_hits
		previous_misses = current_misses
