#!/usr/bin/env python

import os
import shutil

_data_files = [
        ('AG', 'AG_100nt.biom.gz'),
        ('AG', 'AG_100nt.txt'),
        ('PGP', 'PGP_100nt.biom.gz'),
        ('PGP', 'PGP_100nt.txt'),
        ('HMP', 'HMPv35_100nt.biom.gz'),
        ('HMP', 'HMPv35_100nt.txt'),
        ('GG', 'GG_100nt.biom.gz'),
        ('GG', 'GG_100nt.txt')
        ]

_templates = {
        'fecal': ('template_gut.tex', 'macros_gut.tex'),
        'oralskin': ('template_oralskin.tex', 'macros_oralskin.tex')
        }

_identified = ['fecal_identified.txt', 'oral_identified.txt',
               'skin_identified.txt']

def stage_identifed(working_dir):
    data_dir = get_repository_data()

    for f in _identified:
        src = os.path.join(data_dir, 'AG', f)
        shutil.copy(src, working_dir)

def stage_static_files(sample_type, working_dir):
    """Stage static files in the current working directory"""
    _stage_static_data(working_dir)
    _stage_static_latex(sample_type, working_dir)
    _stage_static_pdfs(sample_type, working_dir)

def _stage_static_latex(sample_type, working_dir):
    latex_dir = get_repository_latex()

    for item in _templates[sample_type]:
        src = os.path.join(latex_dir, item)
        shutil.copy(src, working_dir)

def _stage_static_pdfs(sample_type, working_dir):
    pdfs_dir = get_repository_latex_pdfs(sample_type)

    for f in os.listdir(pdfs_dir):
        src = os.path.join(pdfs_dir, f)
        shutil.copy(src, working_dir)

def _stage_static_data(working_dir):
    data_dir = get_repository_data()

    for d, f in _data_files:
        src = os.path.join(data_dir, d, f)
        shutil.copy(src, working_dir)

def get_repository_dir():
    """Get the root of the American-Gut repository"""
    expected = os.path.abspath(__file__).rsplit('/', 2)[0]

    if not os.path.exists(os.path.join(expected, 'data')):
        raise IOError("%s does not look like the AG repo!" % expected)

    if not os.path.exists(os.path.join(expected, 'latex')):
        raise IOError("%s does not look like the AG repo!" % expected)

    return expected

def get_repository_data():
    return os.path.join(get_repository_dir(), 'data')

def get_repository_latex():
    return os.path.join(get_repository_dir(), 'latex')

def get_repository_latex_pdfs(sample_type):
    latex_dir = get_repository_latex()

    if sample_type == 'oralskin':
        pdfs_dir = os.path.join(latex_dir, 'pdfs-oralskin')
    elif sample_type == 'fecal':
        pdfs_dir = os.path.join(latex_dir, 'pdfs-gut')
    else:
        raise ValueError("Unknown sample type: %s" % sample_type)

    if not os.path.exists(pdfs_dir):
        raise IOError("PDFs dir %s doesn't appear to exist!" % pdfs_dir)

    return pdfs_dir

def get_path(d, f):
    path = os.path.join(d, f)
    if not os.path.exists(path):
        raise IOError("%s does not exist!" % path)
    else:
        return path