from numpy import array
import numpy as np
import re
import pandas as pd


def extrema_file(filename):
	datablock = {}
	data = []
	coords = []
	
	for line in open(filename):
		if line.startswith('s'):
			if coords != []:
				datablock['coords'] = np.matrix(coords)
				data.append(datablock)
			datablock = {'name': line.rstrip()}
			coords = []
		elif line.startswith('n'):
			datablock['number_of_extrema'] = int(line.rsplit(':', 1)[1].strip())
		elif line.startswith('(') and line.endswith(')\n'):
			datablock['val_extrema'] = eval(line)[1]
		elif line.startswith('(') and line.endswith(',\n'):
			datablock['val_extrema'] = eval(line.rstrip(',\n') + ']))')[1]
		elif line.startswith('  '):
			datablock['val_extrema'] = np.append(datablock['val_extrema'], eval('[' + line.lstrip(' ').rstrip(')\n')))
		elif line.startswith(' [') or line.startswith('[['):
			coords.append(list(map(float, re.split(' +', line.strip('[] \n')))))
	datablock['coords'] = np.matrix(coords)
	data.append(datablock)
	#return pd.DataFrame.from_dict(data)
	return data
        


if __name__ == '__main__':
	mydata = extrema_file('file_extrema.txt')
	print(pd.DataFrame.from_records(mydata))
	
	
		



