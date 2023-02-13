from itertools import islice
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

RATING_VARIABLES = {"aeration": 0.2, "biodegradability": 0.2, "possessed": 0.6}  # Keys: variable str, values: weights
IDEAL_MOISTURE = 0.6


# Declare the class BrownMaterial, the instances of which represent brown materials.
class BrownMaterial:
    def __init__(self, name, carbon_percentage, nitrogen_percentage, moisture_percentage, aeration, biodegradability,
                 possessed):
        self.name = name
        self.weight = None

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


# Declare the class GoodCombination, each of which represents a combination within the defined range of C/N = 30
class GoodCombination:
    def __init__(self, materials, cn_ratio, weights, needed_water_weight, combo_num, rating):
        self.materials = materials
        self.cn_ratio = cn_ratio
        self.weights = weights  # Weights are based on the order of materials
        self.needed_water_weight = needed_water_weight
        self.combo_num = combo_num
        self.rating = rating

    def __str__(self):
        material_strings = [material.name for material in self.materials]
        materials_string = ""
        for idx, material_string in enumerate(material_strings):
            materials_string = materials_string + material_string + " weight: " + str(self.weights[idx]) + "; "
        materials_string = materials_string[:-2]

        string = "GoodCombination object; " + \
                 "C:N ratio: " + str(self.cn_ratio) + "; " + \
                 materials_string + "; " + \
                 "Water weight needed: " + str(self.needed_water_weight) + "; " + \
                 "Combination number: " + str(self.combo_num) + "; " + \
                 "Rating: " + str(self.rating) + "|\n"
        return string


# Fill a list `all_materials` with a list of BrownMaterial objects by pulling from the browns.dat data file, and  create
# a corollary dictionary
def read_browns_data():
    # Create a DataFrame from the data file
    column_names = ["name", "carbon_percentage", "nitrogen_percentage", "moisture_percentage"] + \
                   list(RATING_VARIABLES.keys())
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
    # Create the corollary dictionary
    all_materials_dictionary = {}
    for material in all_materials:
        all_materials_dictionary[material.name] = material

    return all_materials, all_materials_dictionary


# Search and fill `good_combos` with GoodCombinations, no optimization. Returns the # of iterations and plotting data.
def alg1_search(combo, combo_nums, materials, green_layer_data, upper_range, lower_range, max_weight, d_weight,
                init_weight, optimization=None):
    # Initialize variables
    big_o = 0  # Number of iterations
    good_combos = []  # `combo`s which are within the defined range of C/N = 30. List of GoodCombinations.
    # [FOR PLOTTING]
    x_combo_num = []  # The x-coordinate, the combination num
    y_cn_ratios = []  # The y-coordinate, C:N ratio of the corresponding combination num (w/ same idx in `combo_nums`)

    # Search and fill `good_combos` with GoodCombinations
    for combo_num in combo_nums:
        big_o += 1

        # Generate `combo` as a num_materials-long list of numbers, each number representing the weight of the
        # material with the same index in the list `materials` (each iteration of the for loop modifies `combo`)
        iterate_combo(combo, 0, max_weight, d_weight, init_weight)

        # Assign the materials their weights, according to the scheme in the last comment
        for idx, material in enumerate(materials):
            material.weight = combo[idx]

        # First determine the properties of this particular brown layer and then determine the C:N ratio and total
        # weight of this particular brown layer combination combined with the given green layer.
        b_total, cn_ratio, t_weight = calc_cn_ratio(green_layer_data, materials)

        # For plotting
        x_combo_num.append(combo_num)
        y_cn_ratios.append(cn_ratio)

        # Check if the combination is a good combination, if so add it to `good_combos`
        if 30 + upper_range >= cn_ratio >= 30 + lower_range:
            # Determine the water that needs to be added for the combination
            t_water = green_layer_data["W"]  # Total water weight
            for material in materials:
                water_weight = material.weight * material.moisture_percentage
                t_water += water_weight
            water_weight_needed = (IDEAL_MOISTURE * t_weight) - t_water

            # Assign rating to the combination
            total_rating = 0
            for material in materials:
                weight_percentage = material.weight / b_total
                rating = 1 / (abs(weight_percentage - material.ideal_percentage))
                total_rating += rating

            good_combos.append(
                GoodCombination(materials, cn_ratio, tuple(combo), water_weight_needed, combo_num, total_rating))

        # [OPTIMIZATION] implement Algorithm 2
        if optimization:
            # Check and set which places contain a minimum
            num_materials = len(materials)
            at_minimum = [False] * num_materials
            for idx, place_value in enumerate(combo):
                if place_value == init_weight:
                    at_minimum[idx] = True
            # Alg 2
            if cn_ratio > 30 + upper_range:
                skip_place = 0
                for switch in at_minimum:
                    if switch:
                        skip_place += 1
                    else:
                        break

                steps = int(float((max_weight - init_weight) / d_weight + 1))
                to_skip = (((max_weight - combo[skip_place]) + 1) * (steps ** skip_place)) - 1
                # Skips the nums (how the for loop is iterating)
                next(islice(combo_nums, to_skip, to_skip), None)

                # Cases in which the last place has been MAXED OUT
                # This is simply in place to end the entire search in the case that the rest of the search is bad
                if skip_place == num_materials - 1 or (skip_place == num_materials - 2 and combo[skip_place + 1]
                                                       == max_weight):
                    break
                else:
                    iterate_combo(combo, skip_place + 1, max_weight, d_weight, init_weight)
                # Makes combo into the iteration to be started on.
                for idx in range(skip_place, -1, -1):
                    combo[idx] = init_weight
                combo[0] = init_weight - d_weight

    # Sort good_combos
    good_combos.sort(key=lambda o: o.rating, reverse=True)

    return good_combos, big_o, x_combo_num, y_cn_ratios


# Iterates the combo using Algorithm 1, used by alg1_search
def iterate_combo(combo, init_place, max_weight, d_weight, init_weight):
    added_to_right_place = False
    place = init_place
    while not added_to_right_place:
        if combo[place] != max_weight:
            added_to_right_place = True
            combo[place] += d_weight
            for j in range(place - 1, -1, -1):
                combo[j] = init_weight
        else:
            place += 1
    return combo


# Helper method for  alg1_search, calculates the C:N ratio of a combination of brown and green layer. Also returns the
# total weight of the aforementioned combination, and the total weight of the brown layer.
def calc_cn_ratio(green_layer_data, materials):
    b_carbon = 0  # Brown layer carbon weight
    b_nitrogen = 0  # Brown layer nitrogen weight
    b_total = 0  # Brown layer total weight
    # Assign brown layer carbon, nitrogen, and total weight
    for material in materials:
        b_total += material.weight
        b_carbon += (material.weight * material.dry_percentage) * material.carbon_percentage  # (dry weight)*c_percent
        b_nitrogen += (material.weight * material.dry_percentage) * material.nitrogen_percentage  # (dry w)*n_percent
    t_carbon = green_layer_data["C"] + b_carbon  # Total carbon weight
    t_nitrogen = green_layer_data["N"] + b_nitrogen  # Total nitrogen weight
    cn_ratio = t_carbon / t_nitrogen  # Carbon:Nitrogen ratio
    assert cn_ratio > 0
    t_weight = b_total + green_layer_data["T"]  # Total weight
    return b_total, cn_ratio, t_weight


# Search with the given materials, data, and settings
# Returns the list of combinations within the range, as well as the number of iterations and combo # w/ CN ratio to plot
def search(all_materials_dictionary, materials_strings, green_layer_data, upper_range, lower_range, max_weight,
           d_weight, init_weight, search_function, optimization=False):
    # Define basic variables
    steps = float((max_weight - init_weight) / d_weight + 1)  # this includes the first step (hence, + 1)
    assert steps.is_integer()
    steps = int(steps)
    materials = [all_materials_dictionary[string_name] for string_name in materials_strings]
    num_materials = len(materials)

    # Set up rating system (find ideal percentage of each material)
    total_value = 0
    material_values = []
    for material in materials:
        material_value = material.aeration * RATING_VARIABLES["aeration"] + material.biodegradability * \
                         RATING_VARIABLES["biodegradability"] + material.possessed * RATING_VARIABLES["possessed"]
        material_values.append(material_value)
        total_value += material_value
    for idx, material in enumerate(materials):
        material.ideal_percentage = material_values[idx] / total_value

    # Initialize variables for search
    combo_nums = iter(list(np.linspace(1, steps ** num_materials, steps ** num_materials)))  # all combination numbers
    combo = [init_weight] * num_materials  # Initial combo
    combo[0] = init_weight - d_weight  # first run will set this to the init_weight

    # Using the specified search function, search and return: the list of `combo`s which are within the defined range of
    # C/N = 30; the number of iterations; and the combo number and corresponding cn ratio for plotting
    return search_function(combo, combo_nums, materials, green_layer_data, upper_range, lower_range, max_weight,
                           d_weight, init_weight, optimization)


# Plot the search
def plot(x_combo_num1, y_cn_ratios1, good_combos1, x_combo_num2, y_cn_ratios2, good_combos2, upper_range,
         lower_range, plot_figures):
    x1 = np.asarray(x_combo_num1)
    y1 = np.asarray(y_cn_ratios1)
    x2 = [good_combo.combo_num for good_combo in good_combos1]
    y2 = [good_combo.cn_ratio for good_combo in good_combos1]

    a1 = np.asarray(x_combo_num2)
    b1 = np.asarray(y_cn_ratios2)
    a2 = [good_combo.combo_num for good_combo in good_combos2]
    b2 = [good_combo.cn_ratio for good_combo in good_combos2]

    '''
    plt.plot(x1, y1, label="No optimization -- checked combinations", color="red", marker="o", linestyle="solid")
    # plt.plot(a1, b1, label="With optimization -- checked combinations", color="blue", marker="o", linestyle="solid")
    plt.plot(x2, y2, "^", label="No optimization -- good combinations", color="green", markersize=12)
    # plt.plot(a2, b2, "*", label="With optimization -- good combinations", color="darkorange")

    plt.fill_between(x1, [30+upper_range]*len(x1), [30+lower_range]*len(x1), color="purple", alpha=0.5,
                     label="Good range")
    plt.xlabel("Iteration number")
    plt.ylabel("C:N Ratio")
    '''

    if 1 in plot_figures:
        plot_figure_1(lower_range, upper_range, x1, x2, y1, y2)
    if 2 in plot_figures:
        plot_figure_2(lower_range, upper_range, x1, x2, y1, y2, a1, b1, a2, b2)
    if 3 in plot_figures:
        plot_figure_3(lower_range, upper_range, x1, x2, y1, y2, a1, b1, a2, b2)


def plot_figure_1(lower_range, upper_range, x1, x2, y1, y2):
    fig, ax = plt.subplots(figsize=[15, 10])
    ax.plot(x1, y1, label="No optimization -- checked combinations", color="red", marker="o", linestyle="solid")
    ax.plot(x2, y2, "^", label="No optimization -- good combinations", color="green", markersize=12)
    ax.fill_between(x1, [30 + upper_range] * len(x1), [30 + lower_range] * len(x1), color="purple", alpha=0.5,
                    label="\'Good\' range")
    ax.set_xlabel("Iteration number", fontsize=20)
    ax.set_ylabel("C:N Ratio", fontsize=20)
    ax.set_ylim(0, 52)
    ax.tick_params(axis='x', labelsize=14)
    ax.tick_params(axis='y', labelsize=14)
    # inset axes....
    axins = ax.inset_axes([0.2, 0.08, 0.6, 0.25])
    axins.plot(x1, y1, label="No optimization -- checked combinations", color="red", marker="o", linestyle="solid")
    axins.plot(x2, y2, "^", label="No optimization -- good combinations", color="green", markersize=12)
    axins.fill_between(x1, [30 + upper_range] * len(x1), [30 + lower_range] * len(x1), color="purple", alpha=0.5,
                       label="\'Good\' range")
    # sub region of the original image
    sx1, sx2, sy1, sy2 = 195, 310, 19, 45
    axins.set_xlim(sx1, sx2)
    axins.set_ylim(sy1, sy2)
    # axins.set_xticklabels([])
    # axins.set_yticklabels([])
    ax.indicate_inset_zoom(axins, edgecolor="black")  # , label="Inset axes")
    plt.legend(loc="upper left")
    plt.savefig("figures/figure1.png", bbox_inches="tight")
    plt.show()


def plot_figure_2(lower_range, upper_range, x1, x2, y1, y2, a1, b1, a2, b2):
    fig, ax = plt.subplots(figsize=[15, 10])
    ax.plot(x1, y1, label="No optimization -- checked combinations", color="red", marker="o", linestyle="solid")
    ax.plot(x2, y2, "^", label="No optimization -- good combinations", color="green", markersize=12)
    ax.plot(a1, b1, label="With optimization -- checked combinations", color="blue", marker="o", linestyle="solid")
    ax.plot(a2, b2, "*", label="With optimization -- good combinations", color="darkorange")
    ax.fill_between(x1, [30 + upper_range] * len(x1), [30 + lower_range] * len(x1), color="purple", alpha=0.5,
                    label="\'Good\' range")

    ax.set_xlabel("Iteration number", fontsize=20)
    ax.set_ylabel("C:N Ratio", fontsize=20)
    ax.set_ylim(0, 56)
    ax.tick_params(axis='x', labelsize=14)
    ax.tick_params(axis='y', labelsize=14)

    # inset axes....
    axins = ax.inset_axes([0.15, 0.08, 0.3, 0.25])
    axins.plot(x1, y1, label="No optimization -- checked combinations", color="red", marker="o", linestyle="solid")
    axins.plot(x2, y2, "^", label="No optimization -- good combinations", color="green", markersize=12)
    axins.plot(a1, b1, label="With optimization -- checked combinations", color="blue", marker="o", linestyle="solid")
    axins.plot(a2, b2, "*", label="With optimization -- good combinations", color="darkorange")
    axins.fill_between(x1, [30 + upper_range] * len(x1), [30 + lower_range] * len(x1), color="purple", alpha=0.5,
                       label="\'Good\' range")

    # sub region of the original image
    sx1, sx2, sy1, sy2 = 210, 310, 19, 45
    axins.set_xlim(sx1, sx2)
    axins.set_ylim(sy1, sy2)
    # axins.set_xticklabels([])
    # axins.set_yticklabels([])
    ax.indicate_inset_zoom(axins, edgecolor="black", label="1s-place skip")

    # inset axes....
    axins2 = ax.inset_axes([0.65, 0.08, 0.3, 0.25])
    axins2.plot(x1, y1, label="No optimization -- checked combinations", color="red", marker="o", linestyle="solid")
    axins2.plot(x2, y2, "^", label="No optimization -- good combinations", color="green", markersize=12)
    axins2.plot(a1, b1, label="With optimization -- checked combinations", color="blue", marker="o", linestyle="solid")
    axins2.plot(a2, b2, "*", label="With optimization -- good combinations", color="darkorange")
    axins2.fill_between(x1, [30 + upper_range] * len(x1), [30 + lower_range] * len(x1), color="purple", alpha=0.5,
                        label="\'Good\' range")

    # sub region of the original image
    s2x1, s2x2, s2y1, s2y2 = 740, 840, 21, 47
    axins2.set_xlim(s2x1, s2x2)
    axins2.set_ylim(s2y1, s2y2)
    # axins.set_xticklabels([])
    # axins.set_yticklabels([])
    ax.indicate_inset_zoom(axins2, ls="--", edgecolor="black", label="10s-place skip")

    plt.legend(loc="upper left")
    plt.savefig("figures/figure2.png", bbox_inches="tight")
    plt.show()


def plot_figure_3(lower_range, upper_range, x1, x2, y1, y2, a1, b1, a2, b2):
    fig, ax = plt.subplots(figsize=[15, 10])
    ax.plot(x1, y1, label="No optimization -- checked combinations", color="red", marker="o", linestyle="solid")
    ax.plot(x2, y2, "^", label="No optimization -- good combinations", color="green", markersize=12)
    ax.plot(a1, b1, label="With optimization -- checked combinations", color="blue", marker="o", linestyle="solid")
    ax.plot(a2, b2, "*", label="With optimization -- good combinations", color="darkorange")
    ax.fill_between(x1, [30 + upper_range] * len(x1), [30 + lower_range] * len(x1), color="purple", alpha=0.5,
                    label="\'Good\' range")

    ax.set_xlabel("Iteration number", fontsize=20)
    ax.set_ylabel("C:N Ratio", fontsize=20)
    ax.set_ylim(0, 56)
    ax.tick_params(axis='x', labelsize=14)
    ax.tick_params(axis='y', labelsize=14)

    # inset axes....
    axins = ax.inset_axes([0.1, 0.08, 0.8, 0.25])
    axins.plot(x1, y1, label="No optimization -- checked combinations", color="red", marker="o", linestyle="solid")
    axins.plot(x2, y2, "^", label="No optimization -- good combinations", color="green", markersize=12)
    axins.plot(a1, b1, label="With optimization -- checked combinations", color="blue", marker="o", linestyle="solid")
    axins.plot(a2, b2, "*", label="With optimization -- good combinations", color="darkorange")
    axins.fill_between(x1, [30 + upper_range] * len(x1), [30 + lower_range] * len(x1), color="purple", alpha=0.5,
                       label="\'Good\' range")

    # sub region of the original image
    sx1, sx2, sy1, sy2 = 7680, 8020, 24, 48
    axins.set_xlim(sx1, sx2)
    axins.set_ylim(sy1, sy2)
    # axins.set_xticklabels([])
    # axins.set_yticklabels([])
    ax.indicate_inset_zoom(axins, edgecolor="black", label="100s-place skip")

    plt.legend(loc="upper left")
    plt.savefig("figures/figure3.png", bbox_inches="tight")
    plt.show()


def main():
    # Read browns.dat to create a list and dictionary of BrownMaterial objects
    all_materials, all_materials_dictionary = read_browns_data()
    print("All materials from data file:\n", *all_materials)

    # Green Layer input data
    g_carbon = 5.165  # Green layer carbon weight
    g_nitrogen = 0.265  # Green layer nitrogen weight
    g_total = 10  # Green layer total weight
    g_water = 8.35  # Green layer water weight
    green_layer_data = {"C": g_carbon, "N": g_nitrogen, "T": g_total, "W": g_water}

    # SETTINGS for search
    upper_range = 0.01
    lower_range = -0.01
    max_weight = 9
    d_weight = 1
    init_weight = 0

    # Materials used (strings)
    materials_strings = ["trimmings", "cardboard", "paper", "leaves", ]

    # Not optimized search
    good_combos1, big_o1, x_combo_num1, y_cn_ratios1 = search(all_materials_dictionary, materials_strings,
                                                              green_layer_data, upper_range, lower_range, max_weight,
                                                              d_weight, init_weight, alg1_search)
    # Optimized search
    good_combos2, big_o2, x_combo_num2, y_cn_ratios2 = search(all_materials_dictionary, materials_strings,
                                                              green_layer_data, upper_range, lower_range, max_weight,
                                                              d_weight, init_weight, alg1_search, optimization=True)

    print("\nNOT OPTIMIZED:")
    print(*good_combos1)
    print("Times entered for loop (Big O): ", big_o1)

    print("\n\nOPTIMIZED:")
    print(*good_combos2)
    print("Times entered for loop (Big O): ", big_o2)

    plot_figures = [1, 2, 3]
    plot(x_combo_num1, y_cn_ratios1, good_combos1, x_combo_num2, y_cn_ratios2, good_combos2, upper_range, lower_range
         , plot_figures)


if __name__ == "__main__":
    main()
