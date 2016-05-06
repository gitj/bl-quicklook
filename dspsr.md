### Notes on running dspsr

Dave has compiled a DIRECIO aware version of dspsr in /home/davidm/pulsar_software

I copied the environment activation script /home/davidm/pulsar_software/pulsar.bash to /home/gjones/pulsar.bash and edited the TEMPO and PATH variables so that dspsr can find TEMPO (becuase Dave's installation doesn't include TEMPO).
Then after sourcing /home/gjones/pulsar.bash you can run dspsr on the .raw files. 

For dedispersion to work, you need the OBSBW value to be -187.5 instead of 187.5. Dave has a script that fixes this for data taken to date.

Then you can run a command like:

`dspsr -E /home/gjones/J1713+0747.par -A -t 8 -L 10 -F1024:D -e dspsr_F1024D -O blc07_PSRJ1713+0737 /datax/dibas/AGBT16A_999_175/GUPPI/?/blc*_guppi_*_DIAG_PSR_J1713+0747_00??.00*.raw`

The options are:
  *  -E parfile : specify the par file to use for folding. Parfiles for MSPs can be found in /users/pdemores/tzpar
  *  -A : optional, this makes just a single output file instead of one file per subintegration
  *  -t numthreads : number of threads to use for processing
  *  -L subintlength : number of seconds per subintegration
  *  -F1024:D : this is optional. It takes the 64 coarse channels and uses an FFT filterbank to make 1024 total channels (16 per coarse channel) while doing the dedispersion. This makes RFI easier to spot and excise.
  *  -e dspsr_F1024D : use dspsr_F1024D as the output filename extension
  *  -O blc07_PSRJ1713+0737 : The base of the output filename. not very imaginitive.
  *  Finally, give a glob or list of files to process. It is smart enough to recognize that the *0000.raw *0001.raw... are a sequence to process in order

The output will be blc07_PSRJ1713+0737.dspsr_F1024D

You can view this file using `pav`
`pav -dGT -f 16 blc07_PSRJ1713+0737.dspsr_F1024D`

  * -d : remove interchannel dispersion delay in plot
  * -G : make a phase vs frequency plot
  * -T : add all the subintegrations together
  * -f 16 : scrunch frequency bins by a factor of 16 (so back to 64 channels). Try with and without.


Once running this on all nodes, you can then add all the data together with `psradd`
I copied the blc0?_PSRJ1713+0737.dspsr_F1024D files to bls0:/datax/gjones/AGBT16A_999_175 and ran:
`psradd -R -o PSRJ1713+0737.dspsr_F1024D_added blc0*.dspsr_F1024D`

The -R option says stack the bands in the frequency direction and is important.

view the resulting file:
`pav -dGT -f 16 PSRJ1713+0737.dspsr_F1024D_added`


