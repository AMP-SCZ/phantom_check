import phantom_check
import os
import logging
from pathlib import Path
logger = logging.getLogger(__name__)
from typing import Union


def run_heudiconv(dicom_input_root: Union[Path, str],
                  subject_name: str,
                  session_name: str,
                  nifti_root_dir:Union[Path, str],
                  qc_out_dir: Path) -> None:
    '''Run heudiconv on specified subjects to create nifti structure in BIDS
    
    Key Arguments:
        dicom_input_root: root of dicom directory, where there should be
                          {subject}/{session} directories, Path or str.
                          eg. /data/predict/phantom_human_pilot/sourcedata
                              └── ProNET_UCLA
                                  ├── ses-humanpilot
                                  └── ses-phantom
        subject_name: Name of subject, str.
                      eg) ProNET_UCLA
        session_name: Name of session str. Must not have "ses" in front.
                      eg) humanpilot
        nifti_root_dir: root of the nifti output, Path or str.
        qc_out_dir: QC out directory, Path.

    Returns:
        None

    Note:
        - Heudiconv will use the "phantom_check/data/heuristic.py"
    '''
    heuristic_file = Path(phantom_check.__file__).parent.parent / 'data' / \
            'heuristic.py'

    command = f'heudiconv \
        -d {dicom_input_root}' + '/{subject}/ses-{session}/*/* ' \
        f'-f {heuristic_file} ' \
        f'-s {subject_name} -ss {session_name} -c dcm2niix \
        -b \
        -o {nifti_root_dir}'

    logger.info('Running heudiconv')
    logger.info('heudiconv command: %s' % command)
    output = os.popen(command).read()

    with open(qc_out_dir / '99_heudiconv_log.txt', 'a') as fp:
        fp.write(output)





