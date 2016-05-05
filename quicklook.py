import dspsr
from matplotlib import pyplot as plt
import numpy as np
import sys, os
import glob
import time
import socket
hostname = socket.gethostname()

import logging
logger = logging.getLogger('quicklook')

useful_keys = ['bandwidth',
'base_frequency',
'basis',
'centre_frequency',
#'coordinates',
'dc_centred',
'dual_sideband',
'end_time',
#'format',
#'identifier',
'machine',
'nbit',
'nbyte',
'nchan',
'ndim',
'npol',
'rate',
'receiver',
'scale',
'source',
'start_time',
'state',
'swap',
'telescope']

def get_keys(ts,keys=useful_keys):
	result = {}
	for key in keys:
		result[key] = getattr(ts,'get_'+key)()
	return result

def print_keys(d,columns=3):
	strings = [('%-10.10s :%14.14s' % (k,v)) for k,v in d.items()]
	rows = []
	row = None
	for n,s in enumerate(strings):
		if n % columns == 0:
			if row:
				rows.append(row)
			row = [s]
		else:
			row.append(s)
	rows.append(row)
	return '\n'.join([' | '.join(row) for row in rows])


def quick_plot(fn,NFFT=2**8):
	iom = dspsr.IOManager()
	ts = dspsr.TimeSeries()
	iom.open(fn)
	iom.set_block_size(2**18)
	iom.load(ts)
	print print_keys(get_keys(ts))

	nchan = ts.get_nchan()
#	print nchan
	fig,axs = plt.subplots(3,1,figsize=(12,12),sharex=True)

	ax1 = axs[0]
	ax2 = axs[1]
	ax3 = axs[2]
	Fs = ts.get_rate()/1e6
#	print Fs

	for ichan in range(nchan):
		cf = ts.get_centre_frequency(ichan)
#		print ichan, cf
		x = ts.get_dat(ichan,0).view('complex64').squeeze()
		y = ts.get_dat(ichan,1).view('complex64').squeeze()
		pxx, fr = plt.mlab.psd(x,NFFT=NFFT,Fs=Fs)
		pyy, fr = plt.mlab.psd(y,NFFT=NFFT,Fs=Fs)
		pxy, fr = plt.mlab.csd(x,y,NFFT=NFFT,Fs=Fs)
		if ichan == 0:
			xlabel = 'Pol0'
			ylabel = 'Pol1'
			clabel = 'coherence'
			alabel = 'angle'
		else:
			xlabel = ''
			ylabel = ''
			clabel = ''
			alabel = ''
		ax1.plot(fr+cf,10*np.log10(pxx),'r',label=xlabel)
		ax1.plot(fr+cf,10*np.log10(pyy),'k',label=ylabel)
		cohere = np.abs(pxy)/np.sqrt(pxx*pyy)
		ax2.plot(fr+cf,cohere,'b',label=clabel)
		mask = cohere > 0.2
		ax2.plot((fr+cf)[mask],(np.angle(pxy[mask])),'r.',label=alabel)
#		ax2.plot(fr+cf,(np.angle(pxy)),'k',alpha=0.1)

		xr = x.real
		yr = y.real
		xrms = xr.std()
		yrms = yr.std()
		ax3.errorbar(cf,xr.mean(dtype='float'),yerr=xrms,linestyle='none',marker='o',color='r')
		ax3.plot(cf,xr.max(),'r^',mew=0)
		ax3.plot(cf,xr.min(),'rv',mew=0)

		ax3.errorbar(cf+1,yr.mean(dtype='float'),yerr=yrms,linestyle='none',marker='o',color='k')
		ax3.plot(cf+1,yr.max(),'k^',mew=0)
		ax3.plot(cf+1,yr.min(),'kv',mew=0)
	ax3.axhline(20,linestyle='--',color='g')
	ax3.axhline(-20,linestyle='--',color='g')
	ax3.set_ylim(-130,130)
	ax1.set_ylabel('dB')
	ax2.set_ylabel('coherence / rad')		
	ax3.set_ylabel('counts (8-bit)')
	ax3.set_xlabel('MHz')
	ax1.set_title(('%s:%s' % (hostname,os.path.abspath(fn))),fontsize='medium')
	ax1.legend(loc='upper right',prop=dict(size='small'))
	ax2.legend(loc='upper right',prop=dict(size='small'))
	
	fig.text(0.02,0.02,time.ctime(),ha='left',va='bottom',size='x-small')

	del ts
	del iom
	return fig,axs
		
if __name__ == "__main__":
	handler = logging.StreamHandler()
	handler.setFormatter(logging.Formatter('%(levelname)s: %(asctime)s - %(name)s.%(funcName)s:%(lineno)d  %('
	                                       'message)s'))
	logger.addHandler(handler)
	handler.setLevel(logging.DEBUG)
	logger.setLevel(logging.DEBUG)

	fn = sys.argv[1]
	if fn == 'latest':
		dirs = glob.glob('/datax/dibas/*')
		dirs.sort()
		latest_dir = dirs[-1]
		files = glob.glob(latest_dir+'/GUPPI/*/*.raw')
#		mtimes = [os.stat(f).st_mtime for f in files]
#		fn = sorted(zip(mtimes,files))[-1][1]
		files.sort()
		fn = files[-1]
#		print fn
#		sys.exit(0)

	logger.debug("Looking at filename %s",fn)
	logger.debug("using dspsr from %s",dspsr.__file__)

	quick_plot(fn)
	plt.show()

