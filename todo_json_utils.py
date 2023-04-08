import json

# https://www.geeksforgeeks.org/reading-and-writing-json-to-a-file-in-python/

def write_todo_to_file():
    # Data to be written
    dictionary = {
        "id": 2345,
        "date": "25/02/2023",
        "time": "20.10",
        "who": "Narindech Wanadecha",
        "todo": "I have an appointment with Daniel."
    }

    json_object = json.dumps(dictionary, indent=4)
    # write to todo_list_file.json
    with open("todo_list_file.json", "a") as output:
        output.write(json_object)

def read_todo_to_file(date, month, year):
    print(f"read_todo_to_file --> {date}/{month}/{year}")
    # Opening JSON file
    with open('todo_list_file.json', 'r') as openfile:
    
        # Reading from json file
        json_object = json.load(openfile)
    
    print(json_object)
    return_load = []
    for item in json_object:
        print("item --> ", item)
        date_timestamp = item['date']
        result = date_timestamp.split("/")
        date_util = str(result[0])
        month_util = str(result[1])
        year_util = str(result[2])

        print(f"date_util {date_util}, month_util {month_util}, year_util {year_util}")

        if str(date) == date_util and str(month) == month_util and str(year) == year_util:
            print("Found the right item.")
            return_load.append(item)
    return return_load
    # print(type(json_object))