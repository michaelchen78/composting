# composting

```search.py``` contains the script that implements Algorithms 1 and 2.
The method ```main()``` executes everything. The method ```search(all_materials_dictionary, g_carbon,...)``` runs the search; the last parameter of this method is ```search_function```. Either ```no_optimized_search_function(combo, combo_nums,..)``` or ```optimized_search_function(combo, combo_nums,..)``` should be passed for this argument.

```browns.dat``` contains the brown materials data.



Edit on January 13, 2023:
##### Explanation of the 3-part criteria used
Each BrownMaterial is assigned a rating from 1 to 10 for three different criteria: aeration, biodegradability, and amount of the material possessed. Next, each of the three criteria is assigned a weighting. For example, the current implementation has aeration as 0.2, biodegradability as 0.2, and possessed as 0.6. For each material, the sum is taken over all 3 criteria of the product of the rating and criteria weighting. For example, from ```browns.dat``` the brown material 'leaves' has ratings of 2, 2, 3 for aeration, biodegradability, and possessed, respectively. The sum would then be 2*0.2 + 2*0.2 + 3*0.6 = 2.6. 

This sum represents, relative to the other materials, how desirable it is for the material to be used; we can call it the 'material value'. The last step is to add all the material values together, and then for each material take its material value as a percentage of the sum of the material values. This represents the ideal percentage of that material. Notice that this criteria doesn't simply have us use the best material and lots of it. Instead, it emphasizes a diversity of brown materials (which is beneficial for a compost), and uses a weighing system to favor the better materials.
