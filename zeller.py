# Python3 program to  Find the Day
# for a Date
 
def switch(h) :
    return {
        0 : "Saturday",
        1 : "Sunday",
        2 : "Monday",
        3 : "Tuesday",
        4 : "Wednesday",
        5 : "Thursday",
        6 : "Friday",
    }[h]
 
def Zellercongruence(day, month, year) :
    if (month == 1) :
        month = 13
        year = year - 1
 
    if (month == 2) :
        month = 14
        year = year - 1
    q = day
    m = month
    k = year % 100;
    j = year // 100;
    h = q + 13 * (m + 1) // 5 + k + k // 4 + j // 4 + 5 * j
    h = h % 7
    # print(switch (h))
    return switch(h)
     
     
     
# Driver code
# Zellercongruence(22, 10, 2017) #date (dd/mm/yyyy)
# This code is contributed by Nikita Tiwari
if __name__ == "__main__":
    print(Zellercongruence(1,1,2023))