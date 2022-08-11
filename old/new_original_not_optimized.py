import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


RATING_VARIABLES = ["aeration", "biodegradability", "possessed"]
IDEAL_MOISTURE = 0.6


# Green Layer input data
g_carbon = 5.165  # Green layer carbon weight
g_nitrogen = 0.265  # Green layer nitrogen weight
g_total = 10  # Green layer total weight
g_water = 8.35  # Green layer water weight

UPPER_RANGE = 0.1
LOWER_RANGE = -0.1
max_weight = 100
d_weight = 1
init_weight = 1

steps = float((max_weight-init_weight) / d_weight + 1)  # this includes the first step (hence, + 1)
assert steps.is_integer()
steps = int(steps)


# Declare the class BrownMaterial, the instances of which represent brown materials.
class BrownMaterial:
    def __init__(self, name, carbon_percentage, nitrogen_percentage, moisture_percentage, aeration, biodegradability,
                 possessed):
        self.name = name
        self.weight = init_weight

        # BrownMaterial data
        self.carbon_percentage = carbon_percentage
        self.nitrogen_percentage = nitrogen_percentage
        self.moisture_percentage = moisture_percentage
        self.dry_percentage = 1 - self.moisture_percentage

        # Rating system data
        self.aeration = aeration
        self.biodegradability = biodegradability
        self.possessed = possessed

        # Rating system variables
        self.ideal_percentage = None

    def __str__(self):
        string = "BrownMaterial object; " + \
            "Name: " + self.name + "; " + \
            "Carbon Percentage: " + str(self.carbon_percentage) + "; " + \
            "Nitrogen Percentage: " + str(self.nitrogen_percentage) + "; " + \
            "Moisture Percentage: " + str(self.moisture_percentage) + "; " + \
            "Aeration: " + str(self.aeration) + "; " + \
            "Biodegradability: " + str(self.biodegradability) + "; " + \
            "Possessed: " + str(self.possessed) + "|\n"
        return string


# Fill a list `all_materials` with a list of BrownMaterial objects by pulling from the browns.dat data file, and create
# a corollary dictionary
# Create a DataFrame from the data file
column_names = ["name", "carbon_percentage", "nitrogen_percentage", "moisture_percentage"] + RATING_VARIABLES
data = pd.read_csv("browns.dat", sep=" ", skiprows=1, names=column_names)
# Create and fill `all_materials` by using the DataFrame
all_materials = []
for idx, row in enumerate(data["name"]):
    name = row
    carbon_percentage = data["carbon_percentage"][idx]
    nitrogen_percentage = data["nitrogen_percentage"][idx]
    moisture_percentage = data["moisture_percentage"][idx]
    aeration = data["aeration"][idx]
    biodegradability = data["biodegradability"][idx]
    possessed = data["possessed"][idx]
    all_materials.append(BrownMaterial(name, carbon_percentage, nitrogen_percentage, moisture_percentage, aeration,
                                       biodegradability, possessed))
print("Data file materials: \n", *all_materials)
# Create the corollary dictionary
all_materials_dictionary = {}
for material in all_materials:
    all_materials_dictionary[material.name] = material


MATERIALS_STRINGS = ["paper", "leaves", "cardboard"]
MATERIALS = [all_materials_dictionary[string_name] for string_name in MATERIALS_STRINGS]
print("Used materials: \n", *MATERIALS)

num_materials = len(MATERIALS)


# Declare the class GoodCombination, each of which represents a combination within the defined range of C/N = 30
class GoodCombination:
    def __init__(self, c_n_ratio, weights, needed_water_weight, combo_num, rating):
        self.c_n_ratio = c_n_ratio
        self.weights = weights  # Weights are based on the order of materials
        self.needed_water_weight = needed_water_weight
        self.combo_num = combo_num
        self.rating = rating

    def __str__(self):
        material_strings = [material.name for material in MATERIALS]
        materials_string = ""
        for idx, material_string in enumerate(material_strings):
            materials_string = materials_string + material_string + " weight: " + str(self.weights[idx])+ "; "
        materials_string = materials_string[:-2]

        string = "GoodCombination object; " + \
                 "C:N ratio: " + str(self.c_n_ratio) + "; " + \
                 materials_string + "; " + \
                 "Water weight needed: " + str(self.needed_water_weight) + "; " + \
                 "Combination number: " + str(self.combo_num) + "; " + \
                 "Rating: " + str(self.rating) + "|\n"
        return string

# Set up rating system
aeration_weighting = 0.2
biodegradability_weighting = 0.2
possessed_weighting = 0.6
total_value = 0
material_values = []
for material in MATERIALS:
    material_value = material.aeration * aeration_weighting + material.biodegradability * biodegradability_weighting\
        + material.possessed * possessed_weighting
    material_values.append(material_value)
    total_value += material_value
for idx, material in enumerate(MATERIALS):
    material.ideal_percentage = material_values[idx] / total_value


# For graphing
# The x-coordinate, the combination number
combo_nums = list(np.linspace(1, steps**num_materials, steps**num_materials))[:-1]
# The y-coordinate, the C:N ratio of the corresponding combination number (w/ same idx in `combo_nums`)
c_n_ratios = []

# Initialize variables for search
combo = [init_weight] * num_materials  # Initial combo
combo[0] = init_weight-d_weight
good_combos = []  # `combo`s which are within the defined range of C/N = 30. List of GoodCombinations

# Search and fill `good_combos` with GoodCombinations
for combo_num in combo_nums:
    # Generate `combo` as a num_materials-long list of numbers, each number corresponding to the weight of the material
    # with the same index in the list `materials` as the aforementioned number's index in `combo`
    added_to_right_place = False
    place = 0
    while not added_to_right_place:
        if combo[place] != max_weight:
            added_to_right_place = True
            combo[place] += d_weight
            for j in range(place-1, -1, -1):
                combo[j] = init_weight
        else:
            place += 1
    print(combo_num, " ", combo)
    # Assign the materials their weights, according to the scheme in the last comment
    for idx, material in enumerate(MATERIALS):
        material.weight = combo[idx]

    # Determine the C:N ratio of this particular brown layer combination combined with the given green layer
    b_carbon = 0  # Brown layer carbon weight
    b_nitrogen = 0  # Brown layer nitrogen weight
    b_total = 0  # Brown layer total weight
    # Assign brown layer carbon, nitrogen, and total weight
    for material in MATERIALS:
        b_total += material.weight
        b_carbon += (material.weight * material.dry_percentage)*material.carbon_percentage  # (dry weight)*c_percent
        b_nitrogen += (material.weight * material.dry_percentage)*material.nitrogen_percentage  # (dry weight)*n_percent
    t_carbon = g_carbon + b_carbon  # Total carbon weight
    t_nitrogen = g_nitrogen + b_nitrogen  # Total nitrogen weight
    c_n_ratio = t_carbon / t_nitrogen  # Carbon:Nitrogen ratio
    t_weight = b_total + g_total  # Total weight
    # For graphing
    c_n_ratios.append(t_carbon / t_nitrogen)

    if 30 + UPPER_RANGE >= abs(t_carbon / t_nitrogen) >= 30 + LOWER_RANGE:
        # Determine the water that needs to be added for the combination
        t_water = g_water  # Total water weight
        for material in MATERIALS:
            water_weight = material.weight * material.moisture_percentage
            t_water += water_weight
        # Water weight that needs to be added is the (ideal water weight) - water weight already added
        water_weight_needed = (IDEAL_MOISTURE * t_weight) - t_water

        # Assign rating to each combination
        total_rating = 0
        for material in MATERIALS:
            weight_percentage = material.weight / b_total
            rating = 1 / (abs(weight_percentage - material.ideal_percentage))
            total_rating += rating
        good_combos.append(GoodCombination(c_n_ratio, tuple(combo), water_weight_needed, combo_num, total_rating))


# Sort good_combos
good_combos.sort(key=lambda o: o.rating, reverse=True)
print(*good_combos)


# PLOTTING
figure = plt.figure()
x1 = np.asarray(combo_nums)
y1 = np.asarray(c_n_ratios)
plt.plot(x1, y1, label="line", color="red")
x2 = [good_combo.combo_num for good_combo in good_combos]
y2 = [good_combo.c_n_ratio for good_combo in good_combos]
plt.plot(x2, y2, "o", label="hit", color="green")
plt.show()