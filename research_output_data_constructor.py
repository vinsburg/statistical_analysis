def students_per_category_line_list_constructor(students_per_category_matrix):

    """
    :param students_per_category_matrix: integer matrix of size - students X rounds (3 rounds assumed)
    :return: return_list: list of strings used to construct a 2D array document containing the input matrix.
    details:
    #   each expression in square parentheses is a cell to be printed in the document
    #   cells left blank have the cells below them described in a lower row of the document.
    #   the newrow_cell variable is used to mark a new row.
    """

    newrow_cell = ['\#\#']
    return_list = []
    # constructing the column headers for a 2D array file (like csv):
    return_list += [''] + ['students_per_category'] + newrow_cell
    return_list += [''] + ['round_1'] + ['round_2'] + ['round_3'] + newrow_cell

    # constructing the row headers and inserting the values in students_per_category_matrix
    categories = len(students_per_category_matrix)
    for category_index in range(categories):
        return_list += ['category_' + str(category_index + 1)] #indexed
        return_list += [str(students_per_category_matrix[0][category_index])]
        return_list += [str(students_per_category_matrix[1][category_index])]
        return_list += [str(students_per_category_matrix[2][category_index])]
        return_list +=  newrow_cell

    return return_list

def students_line_list_constructor(students):
    """
    :param: students an object obtained with the syntax <object_name>.worksheet["students"] in analyze.py.
    :return: return_list: list of strings used to construct a 2D array document containing the input matrix.
    details:
    #   each expression in square parentheses is a cell to be printed in the document
    #   cells left blank have the cells below them described in a lower row of the document.
    #   the newrow_cell variable is used to mark a new row.
    """
    newrow_cell = ['\#\#']

    # constructing the table header
    header_row1 = [''] * 7 + ["round_1"] + [''] * 43 + ["round_2"] + [''] * 43 + ["round_3"] + [''] * 43
    roundstring1 = ['google_result_rating'] + [''] * 19 + ['selections_per_category'] + [''] * 9 + [''] + [
        'average_google_category_rank'] + [''] * 12
    header_row2 = [''] * 4 + ["jdistances"] + [''] * 2 + roundstring1 * 3
    roundstring2 = [str(i + 1) for i in range(20)] + [str(i + 1) for i in range(10)] + ['jdistance'] + [str(i + 1) for i in range(10)] + [
                       'pearson_pvalue'] + ['pearson_coefficient'] + ["number_of_categories_selected"]
    header_row3 = ["student_id"] + ["student_last_name"] + ["student_name"] + ["student_notes"] + ['rounds_1&2'] + [
        'rounds_1&3'] + ['rounds_2&3'] + roundstring2 * 3

    return_list=header_row1+newrow_cell
    return_list+=header_row2+newrow_cell
    return_list+=header_row3+newrow_cell

    # constructing the table rows with the data in students
    for student in students:
        current_row = list()
        current_row += [str(student['student_id'])] + [str(student['student_last_name'])] + [str(student['student_name'])] + [
            student['student_notes']]
        jdistances = student['jdistances']
        current_row += [str(jdistances[0]['(1,2)'])] + [str(jdistances[1]['(1,3)'])] + [str(jdistances[2]['(2,3)'])]
        for a_round in student['rounds']:
            for an_input in a_round['inputs']:
                current_row += [str(an_input)]
            category_selection_counts = list(a_round['category_selection_count'].items())
            for index in range(len(category_selection_counts)):  # problem reading from p
                current_row += [str(category_selection_counts[index][1])]
            current_row += [str(a_round['jdistance'])]
            for an_avg_google_rank in a_round['avg_google_rank']:
                current_row += [str(an_avg_google_rank)]
            current_row += [str(a_round['pearson']['pvalue'])]
            current_row += [str(a_round['pearson']['coefficient'])]
            current_row += [str(a_round['uniq_selected_categories'])]
        return_list += current_row + newrow_cell

    return return_list
