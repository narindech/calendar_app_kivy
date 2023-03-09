from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
# from kivy.properties import BooleanProperty, ListProperty, StringProperty, ObjectProperty, NumericProperty
from kivy.properties import StringProperty

from datetime import date
import zeller as zl
import leapyear_cal as lyc
import todo_json_utils as json_util


label_list = ['row00_label','row01_label','row02_label','row03_label','row04_label','row05_label','row06_label',
    'row10_label','row11_label','row12_label','row13_label','row14_label','row15_label','row16_label',
    'row20_label','row21_label','row22_label','row23_label','row24_label','row25_label','row26_label',
    'row30_label','row31_label','row32_label','row33_label','row34_label','row35_label','row36_label',
    'row40_label','row41_label','row42_label','row43_label','row44_label','row45_label','row46_label',
    'row50_label','row51_label','row52_label']
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
months_length = len(months)

global_pass_date = None
global_pass_month = None
global_pass_year = None


class SplashScreen(Screen):
    pass

class MainScreen(Screen):
    current_month = 0
    current_month_str = StringProperty(str(months[current_month]))
    current_year = 0
    current_year_str = StringProperty("")
    current_date = 0
    today_date = 0
    today_month = 0
    today_year = 0

    date_valid = False

    def show_today_date(self):
        today = date.today()
        print("Today's date:", today)
        x = str(today).split("-")

        self.today_date = int(x[2])
        self.today_month = int(x[1])
        self.today_year = int(x[0])

        self.current_year = int(x[0])
        self.current_year_str = str(self.current_year)

        current_month = int(x[1])
        current_date = int(x[2])
        self.current_month_str = str(str(months[current_month - 1]))
        self.current_month = current_month

        self.current_date = current_date
        self.calculate_for_the_first_of_month(self.current_month, self.current_year)

        self.today_date = int(x[2])
        self.today_month = int(x[1])
        self.today_year = int(x[0])

        # for i in self.ids.calendar_grid.children:
        #     print("show me children --> ", type(i))

        global global_pass_month, global_pass_year
        global_pass_month = self.current_month
        global_pass_year = self.current_year
        
        
            

    def next_button_pressed(self):
        print("next_button_pressed current_month --> ", self.current_month)

        if self.current_month >= 12:
            self.current_month = 1
            self.current_year += 1
            self.current_year_str = str(self.current_year)
        else:
            self.current_month += 1
        self.current_month_str = str(str(months[self.current_month - 1]))
        self.calculate_for_the_first_of_month(self.current_month, self.current_year)

        global global_pass_month, global_pass_year
        global_pass_month = self.current_month
        global_pass_year = self.current_year
        # print("next_button_pressed is called.")

    def back_button_pressed(self):
        print("back_button_pressed current_month --> ", self.current_month)

        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
            self.current_year_str = str(self.current_year)
        else:
            self.current_month -= 1
        self.current_month_str = str(str(months[self.current_month - 1]))
        self.calculate_for_the_first_of_month(self.current_month, self.current_year)

        global global_pass_month, global_pass_year
        global_pass_month = self.current_month
        global_pass_year = self.current_year
        # print("back_button_pressed is called.")
    
    def text_validate_fnc(self):
        print("text_validate_fnc is called.")
        # zeller's rule
        # F=k+ [(13*m-1)/5] +D+ [D/4] +[C/4]-2*C where

        # k is  the day of the month.
        # m is the month number.
        # D is the last two digits of the year.
        # C is the first two digits of the year.

        """
        Note:
            According to Zeller’s rule the month is counted as follows:
            March is 1, April is 2….. January is 11 and February is 12.
            So the year starts from March and ends with February. So if the given date has month as January or February subtract 1 from the year. For example:
            For 1st January 1998 subtract 1 from 1998 i.e. 1998-1=1997 and use 1997 for calculating D.
            Discard all the decimal values and then find the final value of F.
        
            After getting the value of F, divide it by 7.The value of F can be either positive or negative. 
            If it is negative, let us suppose F = -15. When we divide by 7 we have to find the greatest multiple of 7 less than -15, 
            so the remainder will be positive (or zero). -21 is the greatest multiple of 7 less than -15, so the remainder is 6 since -21 + 6 = -15.
        
            Alternatively, we can say that -7 goes into -15 twice, 
            making -14 and leaving a remainder of -1.If we add 7 since the remainder is negative i.e. -1 + 7 we again get 6 as remainder. 
            After getting the remainder we can find the day of the week for the given date. 
            Following are the values for the corresponding remainders:
        
            Sun	Mon	Tue	Wed	Thu	Fri	Sat
            0	1	2	3	4	5	6
        
        """
        for_d = self.current_year
        if self.current_month in (1, 2):
            for_d -= 1
        C = str(for_d)[0:2]
        D = str(for_d)[2:]
        K = self.current_date
        M = self.current_month
        # if self.current_month == 1:
        #     M = 11
        # elif self.current_month == 2:
        #     M = 12
        # elif self.current_month == 3:
        #     M = 1
        # elif self.current_month == 4:
        #     M = 2
        # elif self.current_month == 5:
        #     M = 3
        # elif self.current_month == 6:
        #     M = 4
        # elif self.current_month == 7:
        #     M = 5
        # elif self.current_month == 8:
        #     M = 6
        # elif self.current_month == 9:
        #     M = 7
        # elif self.current_month == 10:
        #     M = 8
        # elif self.current_month == 11:
        #     M = 9
        # elif self.current_month == 12:
        #     M = 10
        print("M--> ", M)
        print("K--> ", K)
        print("C--> ", C)
        print("D--> ", D)

        """Zeller's Congruence | The Day of the Week --> https://www.youtube.com/watch?v=_ji1E8ARMWg"""

        # F = int(K) + int((13*int(M)-1)/5) + int(D) + int(int(D)/4) + int(int(C)/4) - int(2*int(C))
        F = int(K) + int((13 * (M + 1))/5) + int(D) + int(int(D)/4) + 5 - int(C) 
        print("F-->", F)
        ans = F % 7
        print("Ans -> ", ans)
        if ans == 0:
            print("Sunday")
        elif ans == 1:
            print("Monday")
        elif ans == 2:
            print("Tuesday")
        elif ans == 3:
            print("Wednesday")
        elif ans == 4:
            print("Thursday")
        elif ans == 5:
            print("Friday")
        elif ans == 6:
            print("Saturday")

        # create variable for our widget
        name = self.ids.row00_label.text

        # update the label
        # self.ids.row00_label.text = "hello"
        


    def calculate_for_the_first_of_month(self, month, year):

        show_today_date_flag = False
        print(f"show me month : {month}, and year : {year}")
        result_v = zl.Zellercongruence(1, int(month), int(year))
        print(f"Real value from zl library --> {result_v}")

        print(f">>>>>>> show me today year {self.today_year}, today month {self.today_month}, today date {self.today_date}")

        if month == self.today_month and year == self.today_year:
            print("THIS is current month & year...")
            show_today_date_flag = True

        # for_d = year
        # if month in (1, 2):
        #     for_d -= 1
        # C = str(for_d)[0:2]
        # D = str(for_d)[2:]
        # K = 1
        """
        0 : "Saturday",
        1 : "Sunday",
        2 : "Monday",
        3 : "Tuesday",
        4 : "Wednesday",
        5 : "Thursday",
        6 : "Friday",
        """
        if result_v == "Saturday":
            ans = 6
        elif result_v == "Sunday":
            ans = 0
        elif result_v == "Monday":
            ans = 1
        elif result_v == "Tuesday":
            ans = 2
        elif result_v == "Wednesday":
            ans = 3
        elif result_v == "Thursday":
            ans = 4
        elif result_v == "Friday":
            ans = 5

        M = month
        
        # print("M--> ", M)
        # print("K--> ", K)
        # print("C--> ", C)
        # print("D--> ", D)

        """Zeller's Congruence | The Day of the Week --> https://www.youtube.com/watch?v=_ji1E8ARMWg"""

        # F = int(K) + int((13*int(M)-1)/5) + int(D) + int(int(D)/4) + int(int(C)/4) - int(2*int(C))
        # F = int(K) + int((13 * (M + 1))/5) + int(D) + int(int(D)/4) + 5 - int(C) 
        # print("F-->", F)
        # ans = F % 7
        # print("Ans -> ", ans)


        _30_month = [4,6,9,11]
        _31_month = [1,3,5,7,8,10,12]
        _feb_month = [2]

        print("1st of this month is --> ")
        if ans == 0:
            print("Sunday")
            if int(M) in _feb_month:
                if lyc.leapYearCalculator(year=year):
                    # 29 days for feb
                    print("29-day month")
                    for i in range(0):
                        list_of_dates.append("")
                    for i in range(1, 30):
                        list_of_dates.append(str(i))
                    for i in range(9):
                        list_of_dates.append("")

                    for index, i in enumerate(label_list):
                        date_label = self.ids[i]
                        date_label.text = list_of_dates[index]
                        
                else:
                    # 28 days for feb
                    print("28-day month")
                    for i in range(0):
                        list_of_dates.append("")
                    for i in range(1, 29):
                        list_of_dates.append(str(i))
                    for i in range(10):
                        list_of_dates.append("")

                    for index, i in enumerate(label_list):
                        date_label = self.ids[i]
                        date_label.text = list_of_dates[index]
                    

            elif int(M) in _30_month:
                # 30 day month
                print("30-day month")
                for i in range(0):
                    list_of_dates.append("")
                for i in range(1, 31):
                    list_of_dates.append(str(i))
                for i in range(8):
                    list_of_dates.append("")

                for index, i in enumerate(label_list):
                    date_label = self.ids[i]
                    date_label.text = list_of_dates[index]
                
            elif int(M) in _31_month:
                # 31 day month
                print("31-day month")
                list_of_dates = []
                for i in range(0):
                    list_of_dates.append("")
                for i in range(1, 32):
                    list_of_dates.append(str(i))
                for i in range(7):
                    list_of_dates.append("")

                for index, i in enumerate(label_list):
                    date_label = self.ids[i]
                    date_label.text = list_of_dates[index]
                
        elif ans == 1:
            print("Monday")
            # row01
            if int(M) in _feb_month:
                if lyc.leapYearCalculator(year=year):
                    # 29 days for feb
                    list_of_dates = []
                    for i in range(1):
                        list_of_dates.append("")
                    for i in range(1, 30):
                        list_of_dates.append(str(i))
                    for i in range(8):
                        list_of_dates.append("")

                    for index, i in enumerate(label_list):
                        date_label = self.ids[i]
                        date_label.text = list_of_dates[index]
                else:
                    # 28 days for feb
                    list_of_dates = []
                    for i in range(1):
                        list_of_dates.append("")
                    for i in range(1, 29):
                        list_of_dates.append(str(i))
                    for i in range(9):
                        list_of_dates.append("")

                    for index, i in enumerate(label_list):
                        date_label = self.ids[i]
                        date_label.text = list_of_dates[index]

            elif int(M) in _30_month:
                # 30 day month
                print("30-day month")
                list_of_dates = []
                for i in range(1):
                    list_of_dates.append("")
                for i in range(1, 31):
                    list_of_dates.append(str(i))
                for i in range(7):
                    list_of_dates.append("")

                for index, i in enumerate(label_list):
                    date_label = self.ids[i]
                    date_label.text = list_of_dates[index]
            elif int(M) in _31_month:
                # 31 day month
                print("31-day month")
                list_of_dates = []
                for i in range(1):
                    list_of_dates.append("")
                for i in range(1, 32):
                    list_of_dates.append(str(i))
                for i in range(6):
                    list_of_dates.append("")

                for index, i in enumerate(label_list):
                    date_label = self.ids[i]
                    date_label.text = list_of_dates[index]
        elif ans == 2:
            print("Tuesday")
            # row01
            if int(M) in _feb_month:
                if lyc.leapYearCalculator(year=year):
                    # 29 days for feb
                    list_of_dates = []
                    for i in range(2):
                        list_of_dates.append("")
                    for i in range(1, 30):
                        list_of_dates.append(str(i))
                    for i in range(7):
                        list_of_dates.append("")

                    for index, i in enumerate(label_list):
                        date_label = self.ids[i]
                        date_label.text = list_of_dates[index]
                else:
                    # 28 days for feb
                    list_of_dates = []
                    for i in range(2):
                        list_of_dates.append("")
                    for i in range(1, 29):
                        list_of_dates.append(str(i))
                    for i in range(8):
                        list_of_dates.append("")

                    for index, i in enumerate(label_list):
                        date_label = self.ids[i]
                        date_label.text = list_of_dates[index]
            elif int(M) in _30_month:
                # 30 day month
                print("30-day month")
                list_of_dates = []
                for i in range(2):
                    list_of_dates.append("")
                for i in range(1, 31):
                    list_of_dates.append(str(i))
                for i in range(6):
                    list_of_dates.append("")

                for index, i in enumerate(label_list):
                    date_label = self.ids[i]
                    date_label.text = list_of_dates[index]
            elif int(M) in _31_month:
                # 31 day month
                print("31-day month")
                list_of_dates = []
                for i in range(2):
                    list_of_dates.append("")
                for i in range(1, 32):
                    list_of_dates.append(str(i))
                for i in range(5):
                    list_of_dates.append("")

                for index, i in enumerate(label_list):
                    date_label = self.ids[i]
                    date_label.text = list_of_dates[index]
        elif ans == 3:
            print("Wednesday")
            if int(M) in _feb_month:
                if lyc.leapYearCalculator(year=year):
                    # 29 days for feb
                    list_of_dates = []
                    for i in range(3):
                        list_of_dates.append("")
                    for i in range(1, 30):
                        list_of_dates.append(str(i))
                    for i in range(6):
                        list_of_dates.append("")

                    for index, i in enumerate(label_list):
                        date_label = self.ids[i]
                        date_label.text = list_of_dates[index]
                else:
                    # 28 days for feb
                    list_of_dates = []
                    for i in range(3):
                        list_of_dates.append("")
                    for i in range(1, 29):
                        list_of_dates.append(str(i))
                    for i in range(7):
                        list_of_dates.append("")

                    for index, i in enumerate(label_list):
                        date_label = self.ids[i]
                        date_label.text = list_of_dates[index]
            elif int(M) in _30_month:
                # 30 day month
                print("30-day month")
                list_of_dates = []
                for i in range(3):
                    list_of_dates.append("")
                for i in range(1, 31):
                    list_of_dates.append(str(i))
                for i in range(5):
                    list_of_dates.append("")

                for index, i in enumerate(label_list):
                    date_label = self.ids[i]
                    date_label.text = list_of_dates[index]
            elif int(M) in _31_month:
                # 31 day month
                print("31-day month")
                list_of_dates = []
                for i in range(3):
                    list_of_dates.append("")
                for i in range(1, 32):
                    list_of_dates.append(str(i))
                for i in range(4):
                    list_of_dates.append("")

                for index, i in enumerate(label_list):
                    date_label = self.ids[i]
                    date_label.text = list_of_dates[index]
        elif ans == 4:
            print("Thursday")
            if int(M) in _feb_month:
                if lyc.leapYearCalculator(year=year):
                    # 29 days for feb
                    list_of_dates = []
                    for i in range(4):
                        list_of_dates.append("")
                    for i in range(1, 30):
                        list_of_dates.append(str(i))
                    for i in range(5):
                        list_of_dates.append("")

                    for index, i in enumerate(label_list):
                        date_label = self.ids[i]
                        date_label.text = list_of_dates[index]
                else:
                    # 28 days for feb
                    list_of_dates = []
                    for i in range(4):
                        list_of_dates.append("")
                    for i in range(1, 29):
                        list_of_dates.append(str(i))
                    for i in range(6):
                        list_of_dates.append("")

                    for index, i in enumerate(label_list):
                        date_label = self.ids[i]
                        date_label.text = list_of_dates[index]
            elif int(M) in _30_month:
                # 30 day month
                print("30-day month")
                list_of_dates = []
                for i in range(4):
                    list_of_dates.append("")
                for i in range(1, 31):
                    list_of_dates.append(str(i))
                for i in range(4):
                    list_of_dates.append("")

                for index, i in enumerate(label_list):
                    date_label = self.ids[i]
                    date_label.text = list_of_dates[index]
            elif int(M) in _31_month:
                # 31 day month
                print("31-day month")
                list_of_dates = []
                for i in range(4):
                    list_of_dates.append("")
                for i in range(1, 32):
                    list_of_dates.append(str(i))
                for i in range(3):
                    list_of_dates.append("")

                for index, i in enumerate(label_list):
                    date_label = self.ids[i]
                    date_label.text = list_of_dates[index]
        elif ans == 5:
            print("Friday")
            if int(M) in _feb_month:
                if lyc.leapYearCalculator(year=year):
                    # 29 days for feb
                    list_of_dates = []
                    for i in range(5):
                        list_of_dates.append("")
                    for i in range(1, 30):
                        list_of_dates.append(str(i))
                    for i in range(4):
                        list_of_dates.append("")

                    for index, i in enumerate(label_list):
                        date_label = self.ids[i]
                        date_label.text = list_of_dates[index]
                else:
                    # 28 days for feb
                    list_of_dates = []
                    for i in range(5):
                        list_of_dates.append("")
                    for i in range(1, 29):
                        list_of_dates.append(str(i))
                    for i in range(5):
                        list_of_dates.append("")

                    for index, i in enumerate(label_list):
                        date_label = self.ids[i]
                        date_label.text = list_of_dates[index]
            elif int(M) in _30_month:
                # 30 day month
                print("30-day month")
                list_of_dates = []
                for i in range(5):
                    list_of_dates.append("")
                for i in range(1, 31):
                    list_of_dates.append(str(i))
                for i in range(3):
                    list_of_dates.append("")

                for index, i in enumerate(label_list):
                    date_label = self.ids[i]
                    date_label.text = list_of_dates[index]
            elif int(M) in _31_month:
                # 31 day month
                print("31-day month")
                list_of_dates = []
                for i in range(5):
                    list_of_dates.append("")
                for i in range(1, 32):
                    list_of_dates.append(str(i))
                for i in range(2):
                    list_of_dates.append("")

                for index, i in enumerate(label_list):
                    date_label = self.ids[i]
                    date_label.text = list_of_dates[index]
        elif ans == 6:
            print("Saturday")
            if int(M) in _feb_month:
                if lyc.leapYearCalculator(year=year):
                    # 29 days for feb
                    list_of_dates = []
                    for i in range(6):
                        list_of_dates.append("")
                    for i in range(1, 30):
                        list_of_dates.append(str(i))
                    for i in range(3):
                        list_of_dates.append("")

                    for index, i in enumerate(label_list):
                        date_label = self.ids[i]
                        date_label.text = list_of_dates[index]
                else:
                    # 28 days for feb
                    list_of_dates = []
                    for i in range(6):
                        list_of_dates.append("")
                    for i in range(1, 29):
                        list_of_dates.append(str(i))
                    for i in range(4):
                        list_of_dates.append("")

                    for index, i in enumerate(label_list):
                        date_label = self.ids[i]
                        date_label.text = list_of_dates[index]
            elif int(M) in _30_month:
                # 30 day month
                print("30-day month")
                list_of_dates = []
                for i in range(6):
                    list_of_dates.append("")
                for i in range(1, 31):
                    list_of_dates.append(str(i))
                for i in range(2):
                    list_of_dates.append("")

                for index, i in enumerate(label_list):
                    date_label = self.ids[i]
                    date_label.text = list_of_dates[index]
            elif int(M) in _31_month:
                # 31 day month
                print("31-day month")
                self.ids.row00_label.text = ""
                self.ids.row01_label.text = ""
                self.ids.row02_label.text = ""
                self.ids.row03_label.text = ""
                self.ids.row04_label.text = ""
                self.ids.row05_label.text = ""
                self.ids.row06_label.text = "1"
                self.ids.row10_label.text = "2"
                self.ids.row11_label.text = "3"
                self.ids.row12_label.text = "4"
                self.ids.row13_label.text = "5"
                self.ids.row14_label.text = "6"
                self.ids.row15_label.text = "7"
                self.ids.row16_label.text = "8"
                self.ids.row20_label.text = "9"
                self.ids.row21_label.text = "10"
                self.ids.row22_label.text = "11"
                self.ids.row23_label.text = "12"
                self.ids.row24_label.text = "13"
                self.ids.row25_label.text = "14"
                self.ids.row26_label.text = "15"
                self.ids.row30_label.text = "16"
                self.ids.row31_label.text = "17"
                self.ids.row32_label.text = "18"
                self.ids.row33_label.text = "19"
                self.ids.row34_label.text = "20"
                self.ids.row35_label.text = "21"
                self.ids.row36_label.text = "22"
                self.ids.row40_label.text = "23"
                self.ids.row41_label.text = "24"
                self.ids.row42_label.text = "25"
                self.ids.row43_label.text = "26"
                self.ids.row44_label.text = "27"
                self.ids.row45_label.text = "28"
                self.ids.row46_label.text = "29"
                self.ids.row50_label.text = "30"
                self.ids.row51_label.text = "31"
                self.ids.row52_label.text = ""
        
        if show_today_date_flag:    
            for index, i in enumerate(label_list):
                date_label = self.ids[i]
                if str(date_label.text) == str(self.today_date):
                    date_label.color = [0,0.7,1,1] # R,G,B, Transparency
                    date_label.bold = True
        else:
            for index, i in enumerate(label_list):
                date_label = self.ids[i]
                date_label.color = [1,1,1,1]
                date_label.bold = False
                
    def event_pressed(self, hello):
        
        print("event_pressed is called.", hello.text)    
        global global_pass_date
        global_pass_date = str(hello.text)
        print(" show me pass_date in event_pressed --> ", global_pass_date)

        if len(global_pass_date) > 0: # if global_pass_date is not empty, then we can go to 'to_do' screen.
            print("date_valid True")
            self.date_valid = True
            App.get_running_app().root.current = "todo"
        else:
            print("date_valid False")
            self.date_value = False

# https://kivy.org/doc/stable/api-kivy.lang.html

# https://www.youtube.com/watch?v=49BvzmqWh-k

# https://www.techwithtim.net/tutorials/kivy-tutorial/multiple-screens/
# https://www.youtube.com/watch?v=7scwS59MfeU
# https://www.youtube.com/watch?v=iDp9htFE0-U
# https://www.youtube.com/watch?v=NmvNutNqKWM
# video tutorial for changing screen and passing data between them.
class TodoScreen(Screen):
    def todo_enter(self):
        print("todo_enter is called. : show me pass_date/pass_month/pass_year ==> ", global_pass_date, global_pass_month, global_pass_year)
        if global_pass_date and global_pass_month and global_pass_year:
            print("all data is here together.")

            json_util.read_todo_to_file(global_pass_date, global_pass_month, global_pass_year)

    def event_save(self, todo_list=None, to_who=None):
        global global_pass_date, global_pass_month, global_pass_year

        print("event_save is called.")
        print("show me global ---> ", global_pass_date, global_pass_month, global_pass_year)
    
    def event_cancel(self, todo_list=None, to_who=None):
        global global_pass_date, global_pass_month, global_pass_year

        print("event_cancel is called.")
        print("show me global ---> ", global_pass_date, global_pass_month, global_pass_year)
            

class WindowManager(ScreenManager):
    pass

class DesignVersion1_1App(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(SplashScreen(name="splash"))
        sm.add_widget(MainScreen(name="main"))
        sm.add_widget(TodoScreen(name="todo"))
        return sm

if __name__ == "__main__":
    app = DesignVersion1_1App()
    app.run()