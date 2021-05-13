import pandas as pd
import numpy as np
import random as rd

# get table of food
def get_food_df(main_df, dessert_df, food_list):
  '''นำข้อมูลเมนูอาหารในแต่ละเมนูมาใส่เป็นตารางจำนวน 7 ตาราง ซึ่ง'''
  food_df = []
  for day in food_list:
      main = main_df.loc[day[:-1]]  # เก็บ 3 เมนูหลักไว้ในตัวแปร main
      # ตรวจสอบว่ามีของหวานหรือไม่
      if day[-1] == '-':
        dest = None
      else:
        dest = dessert_df.loc[[day[-1]]]
      main = pd.concat([main, dest])
      main.reset_index(drop=True, inplace=True)
      food_df.append(main)
  return food_df

# find all results
def diff_food_per_day(food_list):
  '''ทำการจัดเมนูอาหารไม่ให้ซ้ำกันอย่างน้อย 3 วันและไม่เกิน 7 วัน'''
  all_schedule_food = []
  for menu_day1 in food_list:
    schedule_food = [menu_day1]

    for menu_day2 in food_list:
      temp_schedule_food = np.array([k[:-1] for k in schedule_food])
      temp_schedule_food = temp_schedule_food.flatten()
      not_in_schedule = []
      for menu in menu_day2[:-1]:
        not_in_schedule.append(menu not in temp_schedule_food)

      if all(not_in_schedule):
        schedule_food.append(menu_day2)
    if len(schedule_food) >= 3 and len(schedule_food) <=7:
      all_schedule_food.append(schedule_food)
    if len(all_schedule_food) > 20:
      return all_schedule_food
  return all_schedule_food

# get snack to menu
def add_snack(data, sum_energy, sum_protein,
              sum_carbohydrate, sum_fat,
              energy_min, energy_max,
              protein_min, protein_max,
              carbohydrate_min, carbohydrate_max,
              fat_min, fat_max):
  '''หาเมนูของหวานทั้งหมดที่เมื่อรับประทานแล้วจะทำให้สารอาหารครบตามเงื่อนไข'''
  df = data.copy()

  df['Energy'] += sum_energy
  df['Protein'] += sum_protein
  df['Carbohydrate'] += sum_carbohydrate
  df['Fat'] += sum_fat

  energy_const = (df['Energy'] >= energy_min) & (df['Energy'] <= energy_max)
  protein_const = (df['Protein'] >= protein_min) & (df['Protein'] <= protein_max)
  carbo_const = (df['Carbohydrate'] >= carbohydrate_min) & (df['Carbohydrate'] <= carbohydrate_max)
  fat_const = (df['Fat'] >= fat_min) & (df['Fat'] <= fat_max)
  
  cons = energy_const & protein_const & carbo_const & fat_const
  results = df.loc[cons]
  return results

# find food from constraint
def food_constraint(main_df, dessert_df, 
               energy_min=0, energy_max=None,
               protein_min=0, protein_max=None, 
               carbohydrate_min=0, carbohydrate_max=None, 
               fat_min=0, fat_max=None,
               except_food=None):
  '''หาเมนู 3 เมนูที่เป็นไปตามเงื่อนไขของปริมาณสารอาหารในแต่ละโรค'''
  # get number of food
  num_main = len(main_df)
  num_dessert = len(dessert_df)
  
  # get max from dessert
  max_energy_dessert = dessert_df['Energy'].max()
  max_protein_dessert = dessert_df['Protein'].max()
  max_carbohydrate_dessert = dessert_df['Carbohydrate'].max()
  max_fat_dessert = dessert_df['Fat'].max()

  food_used = list()
  food_list = list()

  # find result
  for menu_i in range(num_main):
    for menu_j in range(num_main):
      if (menu_j == menu_i):
        continue

      for menu_k in range(num_main):
        if (menu_k == menu_i) or (menu_k == menu_j):
          continue
        
        sorted_food = sorted([menu_i, menu_j, menu_k])
        if sorted_food in food_used:
          continue

        sum_energy = 0
        sum_protein = 0
        sum_carbohydrate = 0
        sum_fat = 0

        for menu in sorted_food:
          sum_energy += main_df.loc[menu, 'Energy']
          sum_protein += main_df.loc[menu, 'Protein']
          sum_carbohydrate += main_df.loc[menu, 'Carbohydrate']
          sum_fat += main_df.loc[menu, 'Fat']
        
        # constraint 1
        energy_cons1 = (energy_min-max_energy_dessert <= sum_energy < energy_max)
        protein_cons1 = (protein_min-max_protein_dessert <= sum_protein < protein_max)
        carbo_cons1 = (carbohydrate_min-max_carbohydrate_dessert <= sum_carbohydrate < carbohydrate_max)
        fat_cons1 = (fat_min-max_fat_dessert <= sum_fat < fat_max)

        # constraint 2
        energy_cons2 = (energy_min <= sum_energy <= energy_max)
        protein_cons2 = (protein_min <= sum_protein <= protein_max)
        carbo_cons2 = (carbohydrate_min <= sum_carbohydrate <= carbohydrate_max)
        fat_cons2 = (fat_min <= sum_fat <= fat_max)

        # print(sum_energy, sum_protein, sum_carbohydrate, sum_fat)
        if energy_cons1 and protein_cons1 and carbo_cons1 and fat_cons1:
          
          results_snack_df = add_snack(dessert_df, sum_energy, sum_protein,
                            sum_carbohydrate, sum_fat,
                            energy_min, energy_max,
                            protein_min, protein_max,
                            carbohydrate_min, carbohydrate_max,
                            fat_min, fat_max)
          # print(results_snack_df)
          # if don't have any snack -> continue
          if len(results_snack_df) == 0:
            continue
          results = results_snack_df.index.values
          snack = [rd.choice(results)]
          food_used.append(sorted_food)
          food_list.append(sorted_food+snack)

        if energy_cons2 and protein_cons2 and carbo_cons2 and fat_cons2:
          snack = ['-']
          food_used.append(sorted_food)
          food_list.append(sorted_food+snack)
        
  return food_list

# get data except except_food
def clean_data(df, except_food):
  '''ทำการนำเมนูที่รับประทานไม่ได้ออกจากรายการอาหาร'''
  # ทำให้ชื่อของเมนูที่ต้องยกเว้นเป็นอักษรตัวเล็กทั้งหมด
  except_food = [food.lower() for food in except_food]

  for ex_food in except_food:
    food_name = df['Food Name']  # ชื่อเมนูอาหารใส่ตัวแปร food_name

    for food in food_name:
      lower_food = food.lower()  # preprocessing name of food
      lst_food = lower_food.split()  # tokenize name of food
      two_gram = [" ".join([lst_food[n], lst_food[n+1]]) for n in range(len(lst_food)-1)]
      lst_food += two_gram

      if ex_food in lst_food:
        df = df[df['Food Name'] != food].reset_index(drop=True)
  return df

def food_schedule_number(food_list):
  rd.seed(123)

  # เก็บจำนวนวันของอาหารที่แตกต่างกันในแต่ละชุด
  len_list = np.array([len(schedule_) for schedule_ in food_list])

  # เก็บจำนวนวันที่แตกต่างกันสูงสุด
  max_diff_day = max(len_list)
  
  # หาชุดข้อมูลอาหารที่มีเมนูไม่ซ้ำกันสูงสุด
  max_index = np.where(len_list == max_diff_day)[0]

  for number in range(4):
    num_day = max_diff_day*number
    if num_day > 7:
      k = number
      break

  max_index_choice = rd.choices(max_index, k=k)
  food_number_list = []

  for max_ in max_index_choice:
    for food_per_day in food_list[max_]:
      if len(food_number_list) == 7:
        break
      food_number_list.append(food_per_day)

  return food_number_list

def diseases(main_df, dessert_df, 
             energy_min, energy_max,
             prot_min, prot_max,
             carbo_min, carbo_max,
             fat_min, fat_max,
             except_food):

  # ทำการนำเมนูอาหารที่ทานไม่ได้ออกจากรายการเมนูอาหาร
  main_df = clean_data(main_df, except_food)
  dessert_df = clean_data(dessert_df, except_food)

  # หาเมนู 3 เมนูที่ไม่ซ้ำกันและเป็นไปตามเงื่อนไขของสารอาหารแต่ละโรค
  food_list = food_constraint(main_df, dessert_df,
                    energy_min, energy_max,
                    prot_min, prot_max,
                    carbo_min, carbo_max,
                    fat_min, fat_max,
                    except_food)

  # ทำการหาการจัดเรียงเมนูอาหารในแต่ละวันไม่ให้ซ้ำกันทั้งหมด
  food_list = diff_food_per_day(food_list)

  # นำเมนูอาหารที่จัดมาจัดเรียงให้ได้อาหารครบภายใน 7 วัน ผลลัพธ์ที่ได้มาเป็นตัวเลข
  food_list = food_schedule_number(food_list)

  # นำข้อมูลอาหารมาใส่ตามเมนูที่เป็นตัวเลข
  food_list_table = get_food_df(main_df, dessert_df, food_list)

  return food_list_table

