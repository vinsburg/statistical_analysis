# !/usr/bin/env python
import csv

def make_csv_line_matrix(line_list):
    line_matrix = [[]]
    matrix_row_index = 0
    for string_cell in line_list:
        if string_cell != '\#\#':
            line_matrix[matrix_row_index] += [string_cell]
        else:
            line_matrix += [[]]
            matrix_row_index += 1
    return line_matrix


def make_csv_from_line_matrix(line_matrix, output_filename):
    with open(output_filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, dialect='excel')
        for line in line_matrix:
            csvwriter.writerow(line)

    '''
    line_list = []
    line_list += [''] + ['students_per_category'] + ['\#\#']
    line_list += [''] + ['round_1'] + ['round_2'] + ['round_3']

    line_matrix = make_csv_line_matrix(line_list)
    make_csv_from_line_matrix(line_matrix, 'output.csv')
    '''
