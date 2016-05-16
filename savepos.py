import pickle
import os
import time

tmp_file = '/tmp/pos.pkl'
pos_file = '/home/mattvenn/pos.pkl'

import linuxcnc
sta = linuxcnc.stat()

def atomic_write(pos):
	with open(tmp_file, 'w') as fh:
		pickle.dump(pos, fh)
		# make sure that all data is on disk
		fh.flush()
		os.fsync(fh.fileno()) 

	os.rename(tmp_file, pos_file)

if __name__ == '__main__':
	while True:
		sta.poll()
		joints = sta.joint_actual_position
		pos = { 'l' : joints[0], 'r' : joints[1] }
		print(pos)
		atomic_write(pos)
		time.sleep(1)

