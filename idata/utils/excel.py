from xlsxwriter.utility import xl_cell_to_rowcol


def name_to_col(name):
    _, index = xl_cell_to_rowcol("{}1".format(name))
    return index
