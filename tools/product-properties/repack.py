# -*- coding: utf-8 -*-
"""Re-pack the workbook using a shared-strings table.

openpyxl writes every cell value inline, so the option lists -- which repeat across
dozens of categories -- are stored once per row. xlsxwriter pools them in
sharedStrings.xml instead, which cuts the file size dramatically with no change to
the content or the formatting.
"""
import openpyxl, xlsxwriter

SRC = 'MatjarLink_Product_Properties_Expanded.xlsx'
OUT = 'MatjarLink_Product_Properties_Expanded_slim.xlsx'

WIDTHS = {
    'Product Properties': [46, 30, 34, 32, 14, 95, 11],
    'Properties + Options': [46, 30, 34, 32, 10, 95, 11, 10],
    'Summary': [46, 22, 20, 20, 12],
}

src = openpyxl.load_workbook(SRC, read_only=True)
wb = xlsxwriter.Workbook(OUT, {'strings_to_numbers': False})

f_hdr = wb.add_format({'bold': True, 'font_color': 'FFFFFF', 'bg_color': '1F3864',
                       'align': 'center', 'valign': 'vcenter', 'border': 1,
                       'border_color': 'BFBFBF', 'font_size': 11})
f_cat = wb.add_format({'bold': True, 'font_color': '1F3864', 'bg_color': 'D9E2F3', 'font_size': 11})
f_grp = wb.add_format({'bold': True, 'font_color': '404040', 'bg_color': 'F2F2F2', 'font_size': 10})
f_ar = wb.add_format({'align': 'right'})
f_cat_ar = wb.add_format({'bold': True, 'font_color': '1F3864', 'bg_color': 'D9E2F3',
                          'font_size': 11, 'align': 'right'})
f_grp_ar = wb.add_format({'bold': True, 'font_color': '404040', 'bg_color': 'F2F2F2',
                          'font_size': 10, 'align': 'right'})

for name in ('Product Properties', 'Properties + Options', 'Summary'):
    ws_in = src[name]
    ws = wb.add_worksheet(name)
    widths = WIDTHS[name]
    for i, w in enumerate(widths):
        ws.set_column(i, i, w)
    ncol = len(widths)
    is_prop_sheet = name != 'Summary'
    for r, row in enumerate(ws_in.iter_rows(values_only=True)):
        row = list(row)[:ncol]
        if r == 0:
            for c, v in enumerate(row):
                ws.write(0, c, v, f_hdr)
            continue
        if is_prop_sheet:
            if row[0]:
                base, arfmt = f_cat, f_cat_ar
            elif row[1]:
                base, arfmt = f_grp, f_grp_ar
            else:
                base, arfmt = None, f_ar
        else:
            base, arfmt = None, None
        for c, v in enumerate(row):
            if v is None:
                if base is not None:
                    ws.write_blank(r, c, None, base)
                continue
            fmt = arfmt if (is_prop_sheet and c == 3) else base
            ws.write(r, c, v, fmt)
    ws.freeze_panes(1, 0)
    ws.autofilter(0, 0, 0, ncol - 1)

wb.close()

import os
print('old:', os.path.getsize(SRC), 'bytes')
print('new:', os.path.getsize(OUT), 'bytes')
