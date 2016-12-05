#!/usr/bin/python

import csv 

class Analyzer(object):
    
    def __init__(self, filename):
        self.parsed_file = {"file_name": filename}
        data = []
        with open(filename, "r") as csv_file:
            for row in csv.reader(csv_file, dialect='excel'):
                data.append(row)
        header = data.pop(0)
        self.parsed_file["results"] = []
        # each student gets his own entry
        counter = 0
        for line in data:
            counter += 1
            print("counter: " + str(counter) + "line: " +  str(line[0:20]))
            self.parsed_file["results"].append({
                        "rounds"            : [
                                [ int(num) for num in line[0:20]  ],
                                [ int(num) for num in line[20:40] ],
                                [ int(num) for num in line[40:60] ]
                            ],
                        "student_last_name" : line[61],
                        "student_name"      : line[62],
                        "student_id"        : line[63],
                        "student_notes"     : line[60]
                })

    def countCategoriesPerStudent(self, round_num=0):
        students = len(self.parsed_file["results"])
        inputs = [result["rounds"][round_num] for result in self.parsed_file["results"]]
        categoriesPerStudent = []

        categories = 20
        for i in range(students): #for every student
            flag = [False for k in range(categories)] #mark all categories as uncounted
            count = 0 #set counter to zero
            for temp in inputs[i]: #for every student choice
                if not flag[(temp)-1]: #if this category hasnt been counted yet:
                    count+=1 #count the category
                    flag[(temp)-1] = True #mark the category as counted
            categoriesPerStudent.append(count) #add the student's count to the object
        return categoriesPerStudent
    
    def countStudentsPerCategory(self, round_num=0):
        students = len(self.parsed_file["results"])
        inputs = [result["rounds"][round_num] for result in self.parsed_file["results"]]
        categoriesPerStudent = []
        categories = 20
        studentsPerCategory = [0 for i in range(categories)] #will be updated from file in init
        for i in range(len(inputs)): # go over every students input
            flag = [False for k in range(categories)] #create a flag to know if a category has been counted as marked by this student
            for temp in inputs[i]: # go over the student's individual category inputs
                if not flag[temp-1]: # if we still havent marked the category in temp as "used" for this student,
                                     # use temp-1 because input is 1-10 and indexes are 0-9 
                    studentsPerCategory[temp-1] += 1 #increment the overall usage count of this category 
                    flag[temp-1] = True #note that you marked the category as "used" by this student

        return studentsPerCategory

    def calculate_all(self):
        results = []
        for round_num in range(3):
            results.append({
                    "categories_per_student": self.countCategoriesPerStudent(),
                    "students_per_category": self.countStudentsPerCategory()
                })
        return results



if __name__ == "__main__":
    filename = "top3-4judit.xlsx - cloudB.csv"
    analayzer = Analyzer(filename)
    print(analayzer.countCategoriesPerStudent())
    print(analayzer.countStudentsPerCategory())
