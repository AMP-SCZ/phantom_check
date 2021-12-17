from pathlib import Path
from phantom_check.utils.files import get_diffusion_data_from_nifti_prefix, \
        get_nondmri_data, load_data_bval
from phantom_check.utils.visualize import create_b0_signal_figure, \
        create_image_signal_figure 


def quick_figures(subject_dir: Path, outdir: Path):
    # quick figures
    # b0 signal
    fig_num_in_row = 3
    dwi_dir = subject_dir / 'dwi'

    threshold = 50
    dataset = []
    for nifti_path in dwi_dir.glob('*.nii.gz'):
        if 'sbref' not in nifti_path.name:
            nifti_prefix = nifti_path.parent / nifti_path.name.split('.')[0]
            data, bval_arr = get_diffusion_data_from_nifti_prefix(
                    nifti_prefix, '', threshold, False)
            dataset.append((data, bval_arr,
                            nifti_prefix.name.split('ses-')[1]))

    create_b0_signal_figure(dataset, outdir / 'summary_b0.png',
                            True, fig_num_in_row, wide_fig=False)


    dwi_dir = subject_dir / 'dwi'
    dataset = []
    for nifti_path in dwi_dir.glob('*.nii.gz'):
        if 'sbref' not in nifti_path.name:
            nifti_prefix = nifti_path.parent / nifti_path.name.split('.')[0]
            data, _ = load_data_bval(nifti_prefix)
            dataset.append((data, nifti_prefix.name.split('ses-')[1]))

    create_image_signal_figure(dataset, outdir / 'summary_dwi.png',
                            True, fig_num_in_row, wide_fig=False)


    fmri_dir = subject_dir / 'func'
    dataset = []
    for nifti_path in fmri_dir.glob('*.nii.gz'):
        if 'sbref' not in nifti_path.name:
            nifti_prefix = nifti_path.parent / nifti_path.name.split('.')[0]
            data = get_nondmri_data(nifti_prefix, 'nifti_prefix', '', False)
            dataset.append((data, nifti_prefix.name.split('ses-')[1]))

    create_image_signal_figure(dataset, outdir / 'summary_fmri.png',
                            True, 4, wide_fig=True)

