from tkinter import *
from tkinter import ttk
from tkinter import Tk
from tkinter import messagebox
import Food_Schedule as fs
import os
import pandas as pd
import numpy as np

def UI():
    main_windows = Tk()
    main_windows.title("Food Schedule")

    main_windows.geometry("1600x900")
    main_windows.bind('<Escape>', lambda fn: main_windows.destroy())

    font_head = ('Angsana New', 20, 'bold')
    font_body_bold = ('Angsana New', 16, 'bold')
    font_body = ('Angsana New', 16)

    # DISEASES
    # head of diseases
    disease_label = Label(main_windows, text="Diseases", font=font_head)
    disease_label.place(x=20, y=20)

    # combo box of diseases
    disease_values = ('Diabetes', 'Gout Diseases', 'Kidney Diseases')
    disease_combo = ttk.Combobox(main_windows,
                                 values=disease_values,
                                 font=font_body,
                                 state='readonly')
    disease_combo.current(0)
    disease_combo.place(x=20, y=60)

    # WEIGHT
    # head of weight
    weight_label = Label(main_windows, text="Weight", font=font_head)
    weight_label.place(x=220, y=20)

    # entry of weight
    weight_entry = Entry(main_windows, font=font_body)
    weight_entry.place(x=220, y=60)

    # label of kg
    kg_label = Label(main_windows, text='kg', font=font_body)
    kg_label.place(x=370, y=60)

    def check():
        def Diabetes():
            main_path = os.path.join(data_path, "Diabetes_Gout_Main.csv")
            dessert_path = os.path.join(data_path, "Diabetes_Gout_Dessert.csv")

            main_df = pd.read_csv(main_path)  # อ่านไฟล์อาหารจานหลัก
            dessert_df = pd.read_csv(dessert_path)  # ของหวาน
            
            energy_min = 1200
            energy_max = 1600

            prot_min = 36
            prot_max = 60

            carbo_min = 165
            carbo_max = 240

            fat_min = 39
            fat_max = 51

            except_food = ["Coconut Milk"]

            food_schedule = fs.diseases(main_df, dessert_df,
                                        energy_min, energy_max,
                                        prot_min, prot_max,
                                        carbo_min, carbo_max,
                                        fat_min, fat_max,
                                        except_food)
            return food_schedule

        def Gout():
            main_path = os.path.join(data_path, "Diabetes_Gout_Main.csv")
            dessert_path = os.path.join(data_path, "Diabetes_Gout_Dessert.csv")

            main_df = pd.read_csv(main_path)  # อ่านไฟล์อาหารจานหลัก
            dessert_df = pd.read_csv(dessert_path)  # ของหวาน
            
            energy_min = 1200
            energy_max = 1600

            prot_min = 36
            prot_max = 60

            carbo_min = 165
            carbo_max = 240

            fat_min = 33
            fat_max = 51

            except_food = ["Chicken", "Shrimp", "Prawns", "Brown Rice"]

            food_schedule = fs.diseases(main_df, dessert_df,
                                        energy_min, energy_max,
                                        prot_min, prot_max,
                                        carbo_min, carbo_max,
                                        fat_min, fat_max,
                                        except_food)
            return food_schedule

        def Kidney(weight):
            main_path = os.path.join(data_path, "Diabetes_Gout_Main.csv")
            dessert_path = os.path.join(data_path, "Diabetes_Gout_Dessert.csv")

            main_df = pd.read_csv(main_path)  # อ่านไฟล์อาหารจานหลัก
            dessert_df = pd.read_csv(dessert_path)  # ของหวาน
            
            energy_min = weight * 20
            energy_max = weight * 50

            carbo_min = 0
            carbo_max = 400
            
            prot_min = 20
            prot_max = 40
            
            fat_min = 0
            fat_max = 200

            except_food = ["Broccoli", "Basil", "Brown Rice"]

            food_schedule = fs.diseases(main_df, dessert_df,
                                        energy_min, energy_max,
                                        prot_min, prot_max,
                                        carbo_min, carbo_max,
                                        fat_min, fat_max,
                                        except_food)
            return food_schedule

        def GUI(food_schedule):
            breakfast_label = Label(main_windows, text="Breakfast", font=font_head)
            breakfast_label.place(x=50, y=200)

            lunch_label = Label(main_windows, text="Lunch", font=font_head)
            lunch_label.place(x=50, y=350)

            dinner_label = Label(main_windows, text="Dinnder", font=font_head)
            dinner_label.place(x=50, y=500)

            snack_label = Label(main_windows, text="Snack", font=font_head)
            snack_label.place(x=50, y=650)
            
            day_in_week = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
            for day, food_in_day in enumerate(food_schedule):
                x_pos = day*200 + 200
                Day = Label(main_windows, text=day_in_week[day], font=font_head)
                Day.place(x=x_pos, y=150)
                #print(day, food_in_day)
                for num_menu in range(len(food_in_day)):
                    y_pos = num_menu*150 + 200
                    
                    food_name = Label(main_windows, text=food_in_day.loc[num_menu, "Food Name"][:10]+"...", font=font_body_bold)
                    food_name.place(x=x_pos, y=y_pos)

                    energy = Label(main_windows, text="Energy: "+str(food_in_day.loc[num_menu, "Energy"])+" kcal", font=font_body)
                    energy.place(x=x_pos, y=y_pos+25)
                    
                    prot = Label(main_windows, text="Prot: "+str(food_in_day.loc[num_menu, "Protein"])+" g", font=font_body)
                    prot.place(x=x_pos, y=y_pos+50)

                    carb = Label(main_windows, text="Carb: "+str(food_in_day.loc[num_menu, "Carbohydrate"])+" g", font=font_body)
                    carb.place(x=x_pos, y=y_pos+75)

                    fat = Label(main_windows, text="Fat: "+str(food_in_day.loc[num_menu, "Fat"])+" g", font=font_body)
                    fat.place(x=x_pos, y=y_pos+100)

                    
                    
                    
        def decision(disease, weight):
            if disease == "Diabetes":
                food_schedule = Diabetes()
            elif disease == "Gout Diseases":
                food_schedule = Gout()
            else:
                food_schedule = Kidney(weight)
            #print(food_schedule)
            GUI(food_schedule)
    
        data_path = os.path.join(os.getcwd(), "data")
        disease = disease_combo.get()
        weight = weight_entry.get()
        
        #try:
        weight = int(weight)
        if weight > 0:
            decision(disease, weight)
            #else:
                #messagebox.showerror("ERROR", "Weight cannot negative number")
        #except TypeError:
            #messagebox.showerror("ERROR", "Numeric Only")

    show_button = Button(main_windows,
                         text='Show plan',
                         font=font_body,
                         command=check)
                         
    show_button.config(fg='black', bg='white')
    show_button.place(x=420, y=50)

    main_windows.mainloop()


UI()
