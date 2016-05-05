### Notes on running dspsr

Dave has compiled a DIRECIO aware version of dspsr in /home/davidm/pulsar_software

I copied the environment activation script /home/davidm/pulsar_software/pulsar.bash to /home/gjones/pulsar.bash and edited the TEMPO and PATH variables so that dspsr can find TEMPO (becuase Dave's installation doesn't include TEMPO).
Then after sourcing /home/gjones/pulsar.bash you can run dspsr on the .raw files. 

For dedispersion to work, you need the OBSBW value to be -187.5 instead of 187.5. Dave has a script that fixes this for data taken to date.

Then you can run a command like:
`dspsr -E /home/gjones/J1713+0747.par -A -t 8 -L 10 -F1024:D -e dspsr_F1024D -O blc07_PSRJ1713+0737 /datax/dibas/AGBT16A_999_175/GUPPI/?/blc*_guppi_*_DIAG_PSR_J1713+0747_00??.00*.raw`
