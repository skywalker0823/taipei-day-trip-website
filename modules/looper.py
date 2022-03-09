import ast




#新增key判斷
def looper(result,counter=0,summary=[]):
    for site in result:
        counter+=1
        a_set={"id":site["id"],"name":site["name"],"category":site["category2"],"description":site["description"],"address":site["address"],"transport":site["transport"],"mrt":site["mrt"],"latitude":site["latitude"],"longitude":site["longitude"],"images":site["images"]}
        a_set["images"]=ast.literal_eval(a_set["images"])
        summary.append(a_set)
    return summary