import click
import pyipatcher.patchfinder.asrpatchfinder as asr
import pyipatcher.patchfinder.rextpatchfinder as rext
from pyipatcher.patchfinder.patchfinder64 import patchfinder64
from pyipatcher.logger import get_my_logger

@click.command()
@click.argument('input', type=click.File('rb'))
@click.argument('output', type=click.File('wb'))
@click.option(
    '-a',
    '--asr',
    'is_asr',
    is_flag=True,
    help='Patch input file as an ASR (Patch signature check)'
)
@click.option(
    '-r',
    '--restored-external',
    'is_rext',
    is_flag=True,
    help='Patch input file as a restored_external (iOS 14 only) (Patch skip sealing system volume)'
)
@click.option(
    '-v',
    '--verbose',
    'verbose',
    is_flag=True,
    help='Show more debug information'
)

def ramdiskpatcher(input, output, is_asr, is_rext, verbose):
    logger = get_my_logger('asrpatcher', verbose)
    asr.verbose = verbose
    rext.verbose = verbose
    data = input.read()
    pf = patchfinder64(data)
    if is_asr:
        logger.info('Getting get_asr_patch()')
        if asr.get_asr_patch(pf) == -1:
            logger.warning('Failed getting get_asr_patch()')
    elif is_rext:
        logger.info('Getting get_skip_sealing_patch()')
        if rext.get_skip_sealing_patch(pf) == -1:
            logger.warning('Failed getting get_skip_sealing_patch()')
    logger.info(f'Writing out patched file to {output.name}')
    output.write(pf._buf)
    return 0
    
