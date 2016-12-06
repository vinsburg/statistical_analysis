#!/usr/bin/env python

import csv 
import scipy.spatial.distance as distance
from scipy.stats import pearsonr 
from collections import OrderedDict
import itertools
import json

class Analyzer(object):
    
    def __init__(self, filename):
        # lets read all the worksheet exported data
        self.worksheet = {"file_name": filename}
        data = []
        with open(filename, "r") as csv_file:
            for row in csv.reader(csv_file, dialect='excel'):
                data.append(row)
        # pop the titles of the columns , we dont need those, maybe later :)
        header = data.pop(0)
        self.worksheet["students"] = []
        # each student gets his own entry
        counter = 0
        self.categorie_amount = 10
        for line in data:
            self.worksheet["students"].append({
                        "rounds"            : [
                                { 
                                    "inputs" : [ int(num) for num in line[0:20]  ] 
                                },
                                { 
                                    "inputs" : [ int(num) for num in line[20:40] ] 
                                },
                                { 
                                    "inputs" : [ int(num) for num in line[40:60] ] 
                                }
                              
                            ],
                        "student_last_name" : line[61],
                        "student_name"      : line[62],
                        "student_id"        : line[63],
                        "student_notes"     : line[60]
                })
        self._precalculate_all()

    def _get_all_jaccard_distances(self):
        result = []
        for student in self.worksheet["students"]:
            result.append(student["jdistances"])
        return result

    def _precalculate_all(self):
        for round in range(3):
            self._countCategoriesPerStudent(round)
        self._calculate_jaccard_distances()

    def _calculate_jaccard_distances(self):
        for student in self.worksheet["students"]:
            selection_vectors = self._get_round_selection_vectors(student) # gets all the round selection vectors
            combinations = itertools.combinations(enumerate(selection_vectors), 2)
            student["jdistances"] = [] 
            for combination in combinations:
                student["jdistances"].append(
                        { 
                           "({},{})".format(combination[0][0]+1, combination[1][0]+1) : self.__jaccard_distance(combination[0][1], combination[1][1])
                        }
                    )

    def _get_round_selection_vectors(self, student):
        # given a student returns all padded selection vecrots
        # for all his rounds
        selection_vectors = [a_round["categorie_selection_count"].values() for a_round in student["rounds"]]
        return selection_vectors

    def _countCategoriesPerStudent(self, round_num=0):
        students = (self.worksheet["students"])
        inputs = [result["rounds"][round_num]["inputs"] for result in self.worksheet["students"]]
        categoriesPerStudent = []

        categories = self.categorie_amount
        for student in students: #for every student
            categories_per_student = OrderedDict() 
            for i in range(1,self.categorie_amount+1):
                categories_per_student[i] = 0
            for categorie in student["rounds"][round_num]["inputs"]:
                    categories_per_student[int(categorie)] += 1 #add accurance to specific cat count
            count = 0
            for k,v in categories_per_student.items():
                if v != 0:
                 count += 1

            categoriesPerStudent.append(count) #add the student's count to the object
            student["rounds"][round_num]["uniq_selected_categories"] = count
            student["rounds"][round_num]["categorie_selection_count"] = categories_per_student

    def countCategoriesPerStudent(self, round_num=0):
        categoriesPerStudent = []
        for student in self.worksheet["students"]:
            count = student["rounds"][round_num]["uniq_selected_categories"]
            categoriesPerStudent.append(count) #add the student's count to the object
        return categoriesPerStudent
    
    def countStudentsPerCategory(self, round_num=0):
        students = len(self.worksheet["students"])
        inputs = [result["rounds"][round_num]["inputs"] for result in self.worksheet["students"]]
        categoriesPerStudent = []
        categories = self.categorie_amount
        studentsPerCategory = [0 for i in range(categories)] #will be updated from file in init
        for i in range(len(inputs)): # go over every students input
            flag = [False for k in range(categories)] #create a flag to know if a category has been counted as marked by this student
            for temp in inputs[i]: # go over the student's individual category inputs
                if not flag[temp-1]: # if we still havent marked the category in temp as "used" for this student,
                                     # use temp-1 because input is 1-10 and indexes are 0-9 
                    studentsPerCategory[temp-1] += 1 #increment the overall usage count of this category 
                    flag[temp-1] = True #note that you marked the category as "used" by this student

        return studentsPerCategory

    def __jaccard_distance(self, v1, v2):
        return distance.jaccard(v1, v2)

    def _pearson(self, v1, v2):
        coefficient, pvalue =  pearsonr(v1, v2)
        return {"coefficient": coefficient, "pvalue": pvalue} 

    def calculate_all(self):
        results = []
        for round_num in range(3):
            results.append({
                    "categories_per_student": self.countCategoriesPerStudent(),
                    "students_per_category": self.countStudentsPerCategory()
                })
        return results
    
    def _serialize(self, output="csv"):
        result = {
                    "json" : self._serialize_json,
                    "csv" : self._serialize_csv
                }[output](self.worksheet)
        return result
    
    def _serialize_json(self, data):
       return json.dumps(data, indent=4)
   
    def _serialize_csv(self, data):
       return json.dumps(data, indent=3) #fixme - make this export csv instead of json


if __name__ == "__main__":
    filename = "data/atkinsA.csv"
    analayzer = Analyzer(filename)
    #print(analayzer.countCategoriesPerStudent())
    #print(analayzer.countStudentsPerCategory())
    #print(analayzer._get_all_jaccard_distances())
    print(analayzer._serialize())
    print(analayzer._pearson([1,2,3],[3,4,9]))
