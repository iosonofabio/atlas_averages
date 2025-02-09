# vim: fdm=indent
'''
author:     Fabio Zanini
date:       19/07/19
content:    Preprocess pancreas data from Enge et al. 2017.
'''
import os
import sys
import glob
import numpy as np
import pandas as pd
import loompy


if __name__ == '__main__':

    #print('Parse Enge et al. 2017 metadata')
    #fn_pancreas_atlas_meta = '../data_raw/Enge_2017/GSE81547_family.soft'
    #cells = {'name': [], 'cellType': [], 'countsUrl': [], 'cellName2': []}
    #with open(fn_pancreas_atlas_meta, 'rt') as f:
    #    for line in f:
    #        if line.startswith('^SAMPLE ='):
    #            name = line.rstrip('\n').split()[-1]
    #            cells['name'].append(name)
    #        elif line.startswith('!Sample_characteristics_ch1 = inferred_cell_type:'):
    #            ctype = line.rstrip('\n').split(':')[-1][1:]
    #            cells['cellType'].append(ctype)
    #        elif line.startswith('!Sample_supplementary_file_1 = '):
    #            ftp_url = line.rstrip('\n').split()[-1]
    #            cells['countsUrl'].append(ftp_url)
    #            cell_name2 = 'X'+line.rstrip('\n').split('/')[-1].split('_')[1][:-7]
    #            cells['cellName2'].append(cell_name2)
    #cells = pd.DataFrame(cells).set_index('name', drop=False)
    #cells['countsFilename'] = ['../data/pancreas_atlas/'+x.split('/')[-1] for x in cells['countsUrl'].values]

    #print('Exclude unsure cell types')
    #ind = cells['cellType'] != 'unsure'
    #cells = cells.loc[ind]

    #print('Download and parse pancreas atlas counts')
    #from ftplib import FTP
    #ncells = len(cells)
    #counts = None
    #for ic, cn in enumerate(cells.index):
    #    fn = cells.at[cn, 'countsFilename']
    #    if not os.path.isfile(fn):
    #        print('{:}: download file via FTP...'.format(cn), end='')
    #        url = cells.at[cn, 'countsUrl']
    #        ftp_root = 'ftp.ncbi.nlm.nih.gov'
    #        url_fdn = os.path.dirname(url[len('ftp://')+len(ftp_root)+1:])
    #        url_fn = os.path.basename(url)
    #        ftp = FTP(ftp_root)
    #        ftp.login()
    #        ftp.cwd(url_fdn)
    #        with open(fn, 'wb') as f:
    #            ftp.retrbinary(
    #                'RETR {:}'.format(url_fn),
    #                f.write,
    #                )
    #        try:
    #            ftp.quit()
    #        except Exception:
    #            pass
    #        print('done!')
    #    count = pd.read_csv(fn, sep='\t', index_col=0, squeeze=True)
    #    if counts is None:
    #        ngenes = count.shape[0]
    #        genes = count.index.str.rstrip(' ')
    #        counts = np.zeros((ngenes, ncells), np.float32)
    #    counts[:, ic] = count.values
    #counts = pd.DataFrame(counts, index=genes, columns=cells.index)

    #print('Store pancreas atlas to file')
    #loompy.create(
    #    '../data_full/Enge_2017/dataset.loom',
    #    layers={'': counts.values},
    #    row_attrs={'GeneName': counts.index.values},
    #    col_attrs={'CellID': counts.columns.values, 'cellType': cells['cellType'].values},
    #    )

    print('Preprocess manually reannotated Enge 2017')
    print('Metadata')
    meta2 = pd.read_csv(
            '../data_raw/Enge_2017_reannotated/Enge_manual_reannotation.csv',
            sep=',',
            index_col=0).iloc[:, 2]

    print('Counts')
    counts2 = pd.read_csv(
            '../data_raw/Enge_2017_reannotated/AdultAgeingCountTable.csv',
            sep=',',
            index_col=0)
    counts2 = counts2.loc[:, meta2.index].astype(np.float32)

    print('Store reannotated pancreas atlas to file')
    os.makedirs('../data_full/Enge_2017_manual_reannotation', exist_ok=True)
    loompy.create(
        '../data_full/Enge_2017_manual_reannotation/dataset.loom',
        layers={'': counts2.values},
        row_attrs={'GeneName': counts2.index.values},
        col_attrs={'CellID': counts2.columns.values, 'cellType': meta2.values},
        )
