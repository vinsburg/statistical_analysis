#!/usr/bin/env python

import itertools
import json
import sys
import os
from collections import OrderedDict
from scipy.stats import pearsonr
from lib.csv_printer import *
from lib.research_output_data_constructor import *


class Analyzer(object):

    def __init__(self, file_name):
        # lets read all the worksheet exported data
        self.worksheet = {"file_name": file_name}
        data = []
        # with open(file_name, "r", encoding='utf-8', errors='ignore') as csv_file:
        with open(file_name, "r", newline='') as csv_file:
            for row in csv.reader(csv_file, dialect='excel'):
                data.append(row)
        # pop the titles of the columns , we don't need those, maybe later :)
        self.header = data.pop(0)
        self.worksheet['google_categories'] = list(map(int, self.header[0:20]))
        self.worksheet['students'] = []
        # each student gets his own entry
        # counter = 0
        self.category_amount = 10
        for line in data:
            self.worksheet["students"].append({
                        "rounds": [
                                {
                                    "inputs": [int(num) for num in line[0:20]]
                                },
                                {
                                    "inputs": [int(num) for num in line[20:40]]
                                },
                                {
                                    "inputs": [int(num) for num in line[40:60]]
                                }

                            ],
                        "student_last_name": line[61],
                        "student_name": line[62],
                        "student_id": line[63],
                        "student_notes": line[60]
                })
        self._precalculate_all()

    def _get_all_jaccard_distances(self):
        result = []
        for student in self.worksheet["students"]:
            result.append(student["jdistances"])
        return result

    def _precalculate_all(self):
        self.worksheet["students_per_category"] = []
        for a_round in range(3):
            self._count_categories_per_student(a_round)
            self.worksheet["students_per_category"].append(self.count_students_per_category(a_round))
        self._calculate_jaccard_distances()
        self._calculate_google_statistics()

    def _calculate_google_statistics(self):
        students = self.worksheet["students"]
        for student in students:
            for a_round in student["rounds"]:
                a_round["avg_google_rank"] = self._average_google_rating(a_round["inputs"])
                a_round["pearson"] = self._google_pearson(a_round["inputs"])
                a_round["jdistance"] = self._google_jaccard(a_round["inputs"])

    def _average_google_rating(self, inputs):
        google_value_counters = [0]*10
        google_value_sums = [0]*10
        for index, an_input in enumerate(inputs):
            an_input -= 1
            google_value_counters[an_input] += 1
            google_value_sums[an_input] += self.worksheet['google_categories'][index]
        google_value_counters = [1 if val == 0 else val for val in google_value_counters]
        return [a for a in map(lambda x, y: x/float(y), google_value_sums, google_value_counters)]

    def _google_pearson(self, inputs):
        return self.__pearson(self.worksheet['google_categories'], inputs)

    def _google_jaccard(self, inputs):
        return self.__jaccard_distance(self.worksheet['google_categories'], inputs)

    def _calculate_jaccard_distances(self):
        for student in self.worksheet["students"]:
            selection_vectors = self._get_round_selection_vectors(student)  # gets all the round selection vectors
            combinations = itertools.combinations(enumerate(selection_vectors), 2)
            student["jdistances"] = []
            for combination in combinations:
                combo = "({},{})".format(combination[0][0]+1, combination[1][0]+1)
                print(student['student_id'])
                print(list(combination[0][1]))
                print(list(combination[1][1]))
                print(self.__jaccard_distance(list(combination[0][1]), list(combination[1][1])))
                print()
                student["jdistances"].append(
                        {
                            combo: self.__jaccard_distance(list(combination[0][1]), list(combination[1][1]))
                        }
                    )

    def _get_round_selection_vectors(self, student):
        # given a student returns all padded selection vectors
        # for all his rounds
        selection_vectors = [a_round["inputs"] for a_round in student["rounds"]]
        return selection_vectors

    def _count_categories_per_student(self, round_num=0):
        students = (self.worksheet["students"])
        # inputs = [result["rounds"][round_num]["inputs"] for result in self.worksheet["students"]]
        categories_per_student_count = []
        # categories = self.category_amount
        for student in students:  # for every student
            categories_per_student = OrderedDict()
            for i in range(1, self.category_amount+1):
                categories_per_student[i] = 0
            for category in student["rounds"][round_num]["inputs"]:
                    categories_per_student[int(category)] += 1  # add occurrence to specific cat count
            count = 0
            for k, v in categories_per_student.items():
                if v != 0:
                    count += 1

            categories_per_student_count.append(count)  # add the student's count to the object
            student["rounds"][round_num]["uniq_selected_categories"] = count
            student["rounds"][round_num]["category_selection_count"] = categories_per_student

    def count_categories_per_student(self, round_num=0):
        categories_per_student = []
        for student in self.worksheet["students"]:
            count = student["rounds"][round_num]["uniq_selected_categories"]
            categories_per_student.append(count)  # add the student's count to the object
        return categories_per_student

    def count_students_per_category(self, round_num=0):
        # students = len(self.worksheet["students"])
        inputs = [result["rounds"][round_num]["inputs"] for result in self.worksheet["students"]]
        # categoriesPerStudent = []
        categories = self.category_amount
        students_per_category = [0]*categories  # will be updated from file in init
        for i in range(len(inputs)):  # go over every students input
            # create a flag to know if a category has been counted as marked by this student
            flag = [False]*categories
            for an_input in inputs[i]:  # go over the student's individual category inputs
                an_input -= 1
                if not flag[an_input]:  # if we still haven't marked the category in temp as "used" for this student,
                                        # use temp-1 because input is 1-10 and indexes are 0-9
                    students_per_category[an_input] += 1  # increment the overall usage count of this category
                    flag[an_input] = True  # note that you marked the category as "used" by this student

        return students_per_category

    def __jaccard_distance(self, v1, v2):
        # return distance.jaccard(v1, v2)
        if len(v1) != len(v2):
            raise ValueError
        intersection = sum(list(map(lambda x, y: int(x == y), v1, v2)))
        union = len(v1) + len(v2) - intersection
        return 1-intersection/float(union)

    def testing_jacc(self):
        # v1 = [1, 2, 5, 3, 5, 3, 5, 5, 5, 5, 5, 5, 5, 5, 5, 4, 5, 3, 5, 5]
        # v2 = [1, 3, 2, 3, 1, 3, 2, 1, 4, 1, 1, 1, 1, 1, 4, 1, 3, 2, 1, 1]
        v1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110]
        v2 = [1, 2, 5, 3, 5, 3, 5, 5, 5, 5, 5, 5, 5, 5, 5, 4, 5, 3, 5, 5]

        print(v1)
        print(v2)
        print(self.__jaccard_distance(v1, v2))

    def __pearson(self, v1, v2):
        coefficient, pvalue = pearsonr(v1, v2)
        return {"coefficient": coefficient, "pvalue": pvalue}

    def calculate_all(self):
        results = []
        for round_num in range(3):
            results.append({
                    "categories_per_student": self.count_categories_per_student(),
                    "students_per_category": self.count_students_per_category()
                })
        return results

    def _serialize(self, output="csv"):
        result = {
                    "json": self._serialize_json,
                    "csv": self._serialize_csv
                }[output](self.worksheet)
        return result

    def _serialize_json(self, data):
        return json.dumps(data, indent=4)

    def _serialize_csv(self, data):
        output_dirname, output_filename = os.path.split(self.worksheet['file_name'])
        output_filename = "/".join([output_dirname, "outputs", output_filename])
        print(output_filename)
        csv_line_list = students_per_category_line_list_constructor(self.worksheet['students_per_category'])
        csv_line_list += ['\#\#']  # this will indicate the csv_line_matrix method to add a blank line
        csv_line_list += students_line_list_constructor(self.worksheet)
        csv_line_matrix = make_csv_line_matrix(csv_line_list)
        make_csv_from_line_matrix(csv_line_matrix, output_filename)

if __name__ == "__main__":
    filenames = sys.argv
    filenames.pop(0)
    for filename in filenames:
        analyzer = Analyzer(filename)
        analyzer._serialize('csv')
    # print(analyzer.count_categories_per_student())
    # print(analyzer.count_students_per_category())
    # print(analyzer._get_all_jaccard_distances())
    # print(analyzer._serialize('json'))
