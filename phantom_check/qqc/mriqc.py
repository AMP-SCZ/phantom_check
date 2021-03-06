import re
from subprocess import PIPE, Popen
from pathlib import Path


def run_mriqc_on_data(rawdata_dir: Path,
                      subject_id: str,
                      session_id: str,
                      mriqc_outdir_root: Path,
                      temp_dir: str = '/data/predict/kcho/tmp',
                      bsub: bool = True) -> None:
    '''Run MRI-QC following the quick QC

    Key Argument:
        rawdata_dir: root of the BIDS nifti structure
        subject_id: subject ID, including 'sub-'
        session_id: session ID, including 'ses-'
        mriqc_outdir_root: root of the MRIQC out dir, Path.
        temp_dir: location of mriqc working directory
        bsub: bsub option, bool.
    '''
    img_loc = '/data/predict/mg1050/singularity_images/mriqc-0.16.1.sif'
    singularity = '/apps/released/gcc-toolchain/gcc-4.x/singularity/' \
                  'singularity-3.7.0/bin/singularity'

    work_dir = Path(temp_dir) / 'mriqc' / subject_id / session_id
    work_dir.mkdir(exist_ok=True, parents=True)

    command = f'{singularity} run -e \
        -B {rawdata_dir}:/data:ro \
        -B {work_dir}:/work \
        -B {mriqc_outdir_root}:/out \
        -B /data/pnl/soft/pnlpipe3/freesurfer/license.txt:/opt/freesurfer/license.txt \
        {img_loc} \
        /data /out participant \
        -w /work --participant-label {subject_id} \
        --session-id {session_id.split("-")[1]} \
        --nprocs 4 --mem 8G --omp-nthreads 2 \
        --no-sub \
        --verbose-reports'
    
    if bsub:
        command = f'bsub -q pri_pnl \
                -o {mriqc_outdir_root}/mriqc.out \
                -e {mriqc_outdir_root}/mriqc.err \
                -n 4 -J mriqc_{subject_id}_{session_id} \
                {command}'

    command = re.sub('\s+', ' ', command)
    print(command)

    p = Popen(command, shell=True, stdout=PIPE, bufsize=1)
    for line in iter(p.stdout.readline, b''):
        print(line)
    p.stdout.close()
    p.wait()
