# composting

```search.py``` contains the script that implements Algorithms 1 and 2.
The method ```main()``` executes everything. The method ```search(all_materials_dictionary, g_carbon,...)``` runs the search; the last parameter of this method is ```search_function```. Either ```no_optimized_search_function(combo, combo_nums,..)``` or ```optimized_search_function(combo, combo_nums,..)``` should be passed for this argument.

```browns.dat``` contains the brown materials data.



Edit on January 13, 2023:
# Explanation of the 3-part criteria used
Each BrownMaterial is assigned a rating from 1 to 10 for three different criteria: aeration, biodegradability, and amount of the material possessed. Next, each of the three criteria is assigned a weighting. For example, the current implementation has aeration as 0.2, biodegradability as 0.2, and possessed as 0.6. For each material, the sum is taken over all 3 criteria of the product of the rating and criteria weighting. For example, from ```browns.dat``` the brown material '''leaves'''




