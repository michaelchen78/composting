import math
import random
import csv

# EDIT PLACES - lns 7-13, 109, 269-270

# we start off with a given carbon and nitrogen mass for the green layer
greenLayerCarbonMass = 5.165

greenLayerNitrogenMass = 0.265

greenLayerTotalMass = 10

totalWaterMass = 8.35

idealMoisture = 0.6


# make a class for brown materials
class material:

    def __init__(self, name, moisturePercentage, carbonPercentage, nitrogenPercentage, aeration, biodegrad, amountValue,
                 possessed):
        # these are like my for big balls equation stuff
        self.name = name
        self.mass = 1
        self.waterMass = 0
        self.moisturePercentage = moisturePercentage
        self.carbonPercentage = carbonPercentage
        self.nitrogenPercentage = nitrogenPercentage

        # under here are rating system stuff
        self.aeration = aeration
        self.biodegrad = biodegrad
        self.amountValue = amountValue
        self.possessed = possessed

        # and these are for the loops and rating system i think and misc. stuff (sorter?)
        self.switch = 0
        self.counter = 0
        self.value = 0
        self.valuePercentage = 0
        self.massPercentage = 0
        self.diff = 0


# okay so here is the dictionary
# if you can't see the order is moisture content, carbon percent, nitro percent, aeration, biodegrad, amountvalue, and then possessed -
# order doesn't actually matter if you declare it, but you still need all of them (and if you don't declare then it does matter)

leaves = material(
    name="leaves",
    moisturePercentage=0.38,
    carbonPercentage=0.40,
    nitrogenPercentage=0.005,
    aeration=2,
    biodegrad=2,
    amountValue=6,
    possessed=3)

paper = material(
    name="paper",
    moisturePercentage=0.19,
    carbonPercentage=0.38125,
    nitrogenPercentage=0.0025,
    biodegrad=4,
    amountValue=2,
    aeration=1.5,
    possessed=10)

cardboard = material(
    name="cardboard",
    moisturePercentage=0.08,
    carbonPercentage=0.563,
    nitrogenPercentage=0.001,
    biodegrad=5,
    aeration=5,
    amountValue=2,
    possessed=7)

trimmings = material(
    name="trimmings",
    moisturePercentage=0.15,
    carbonPercentage=0.53,
    nitrogenPercentage=0.01,
    biodegrad=3,
    aeration=4,
    amountValue=5,
    possessed=7)

# aeration is on scale of 1 -> 10, 1 is very bad aeration (stone) 10 is very good aeration (holes)
# biodegrad is how biodegradable it is (replaced sizespace) and it is time so more is bad
# amountValue is how much is recommened to be put in, again 1 -> 10, 10 is more - isnt this just basically the entire thing
# possessed is how much we have in mass in kg
# all direct like quant .... ratio


aerationValue = 0.1
biodegradValue = 0.1
amountValueValue = 0.2
possessedValue = 0.6

# so these work for the rating system they basically just like they say how much it matters -
# so the rating system works like this - so you first get the aeration from a material and multiply by the corresponding value so this basically gives you the ideal amount relative
# of that material since like so you do that for all of it so for leaves you do that and then you have that and then you add paper and have total value
# and then relative you can figure out how much leaves you want percentage of total and paper etc.


# so this little thing is just what you put the materials you want it to calculate in. you need to put it in the -
# dictionary above before you put it in here though obv
materials = [cardboard, leaves, paper]

# ___________________________________________________


# okay so this is like the real start of the big stuff
materialsDictionary = {}
numMaterials = len(materials)

# okay this for loop stores the objects in the list called materials into the dictionary called materialsDictionary

for i in range(numMaterials):
    materialsDictionary["material{0}".format(i)] = materials[i]
# print(materialsDictionary)
# print(materialsDictionary['material2'].aeration)


# this set of for loops sets up the rating system

for i in range(len(materialsDictionary)):
    # print('start of round')
    materialsDictionary["material{0}".format(i)].value = \
        ((materialsDictionary["material{0}".format(i)].aeration) * aerationValue) \
        - ((materialsDictionary["material{0}".format(i)].biodegrad) * biodegradValue) \
        + ((materialsDictionary["material{0}".format(i)].amountValue) * amountValueValue) \
        + ((materialsDictionary["material{0}".format(i)].possessed) * possessedValue) \
 \
        # print(leaves.value, cardboard.value, paper.value)

totalValue = 0
for i in range(len(materialsDictionary)):
    totalValue = totalValue + materialsDictionary["material{0}".format(i)].value

for i in range(len(materialsDictionary)):
    materialsDictionary["material{0}".format(i)].valuePercentage = \
        materialsDictionary["material{0}".format(i)].value / totalValue

    # print(totalValue)
    # print(leaves.valuePercentage, paper.valuePercentage, cardboard.valuePercentage)

# so here is the start of the while loop

# these are to count combos and good combos meaning ones that match the equation
comboList = {}
# CNratios = {}
# graphX = []
# graphY = []
goodComboCounter = 0
totalCombinations = 0
expectedTotalCombo = (100 ** (numMaterials)) + 1  # just to see
# print(expectedTotalCombo)


while totalCombinations < expectedTotalCombo:

    # all of this below is just to stop the while loop
    # print(totalCombinations)
    totalCombinations += 1

    # total combinations should be the total + 1 since theres a 0, but then - 1 off of the final since 001 i think
    # well starts with 000 the first time actually so yea...first run gets 001....?
    if totalCombinations > expectedTotalCombo:
        print("total runs:", totalCombinations)

    # if totalCombinations == math.floor(0.5 * expectedTotalCombo):
    #  print('halfway there!')

    for i in range(10):
        if totalCombinations == math.floor((i / 10) * expectedTotalCombo):
            print(i * 10)

    # _____________________________________________________________________
    # and these are just the while loop stuff

    # this first section is for the first material
    if materialsDictionary["material0"].switch == 2:
        materialsDictionary["material0"].mass += 1
        materialsDictionary["material0"].counter += 1

    if materialsDictionary["material0"].switch == 0:
        materialsDictionary["material0"].switch = 2

    if materialsDictionary["material0"].counter == 100:
        # cardboard.switch = 1  # turns off

        materialsDictionary["material0"].counter = 0
        materialsDictionary["material0"].mass = materialsDictionary["material0"].mass - 100
        materialsDictionary["material1"].switch = 1

    else:
        materialsDictionary["material0"].switch = 2
        materialsDictionary["material1"].switch = 0

    # ________________________________________________________________

    # this second section is materials 1 through second to last
    for i in range(len(materialsDictionary) - 2):
        if materialsDictionary["material{0}".format(i + 1)].switch == 1:
            materialsDictionary["material{0}".format(i + 1)].mass += 1
            materialsDictionary["material{0}".format(i + 1)].counter += 1

        if materialsDictionary["material{0}".format(i + 1)].counter == 100:
            materialsDictionary["material{0}".format(i + 1)].mass -= 100
            materialsDictionary["material{0}".format(i + 1)].counter = 0

            materialsDictionary["material{0}".format(i + 2)].switch = 1
        else:
            materialsDictionary["material{0}".format(i + 2)].switch = 0

    # ________________________________________________________________

    # last section is for last materials
    if materialsDictionary["material{0}".format(len(materialsDictionary) - 1)].switch == 1:
        materialsDictionary["material{0}".format(len(materialsDictionary) - 1)].mass += 1
        materialsDictionary["material{0}".format(len(materialsDictionary) - 1)].counter += 1

    if materialsDictionary["material{0}".format(len(materialsDictionary) - 1)].counter == 100:
        materialsDictionary["material{0}".format(len(materialsDictionary) - 1)].mass -= 100
        materialsDictionary["material{0}".format(len(materialsDictionary) - 1)].counter = 0

    # now here is where the math gun begins

    brownLayerCarbonMass = 0
    brownLayerNitrogenMass = 0
    brownLayerTotalMass = 0

    for i in range(len(materialsDictionary)):
        brownLayerTotalMass = brownLayerTotalMass + materialsDictionary['material{0}'.format(i)].weight

    for i in range(len(materialsDictionary)):
        brownLayerCarbonMass = brownLayerCarbonMass + \
                               (
                                       (materialsDictionary["material{0}".format(i)].mass) * \
                                       (1 - (materialsDictionary["material{0}".format(i)].moisturePercentage))
                               ) * materialsDictionary["material{0}".format(i)].carbonPercentage

    for i in range(len(materialsDictionary)):
        brownLayerNitrogenMass = brownLayerNitrogenMass + \
                                 (
                                         (materialsDictionary["material{0}".format(i)].mass) * \
                                         (1 - (materialsDictionary["material{0}".format(i)].moisturePercentage))
                                 ) * materialsDictionary["material{0}".format(i)].nitrogenPercentage

    # so now I have this great if statement that is basically like if you follow the equation then you are a good combo

    # these are just for range in case nothing is found

    upperRange = 0.1
    lowerRange = -0.1  # it's negative since its a plus below

    totalCarbonMass = greenLayerCarbonMass + brownLayerCarbonMass
    totalNitrogenMass = greenLayerNitrogenMass + brownLayerNitrogenMass
    # print(totalCarbonMass)
    # print(totalNitrogenMass)

    # print(totalCarbonMass / totalNitrogenMass)

    # CSV shit

    # CNratios["number{0}".format(totalCombinations)] = {}

    # for i in range(len(materialsDictionary)):
    # CNratios["number{0}".format(totalCombinations)]["mass{0}".format(i)] = materialsDictionary[
    # "material{0}".format(i)].mass

    # CNratios["number{0}".format(totalCombinations)]["CNRatio"] = (totalCarbonMass / totalNitrogenMass)

    # print(CNratios["number{0}".format(totalCombinations)])

    if abs(totalCarbonMass / totalNitrogenMass) <= 30 + upperRange \
            and abs(totalCarbonMass / totalNitrogenMass) >= 30 + lowerRange:
        # print('reached')

        # okay now all of this is just for rating system again
        for i in range(len(materialsDictionary)):
            materialsDictionary["material{0}".format(i)].massPercentage = \
                (materialsDictionary["material{0}".format(i)].mass) / brownLayerTotalMass

        for i in range(len(materialsDictionary)):
            materialsDictionary["material{0}".format(i)].diff = \
                abs((materialsDictionary["material{0}".format(i)].valuePercentage) \
                    - (materialsDictionary["material{0}".format(i)].massPercentage))

        totalDiff = 0
        for i in range(len(materialsDictionary)):
            totalDiff = totalDiff + materialsDictionary["material{0}".format(i)].diff

        # moisture

        for i in range(len(materialsDictionary)):
            materialsDictionary["material{0}".format(i)].waterMass = \
                materialsDictionary["material{0}".format(i)].moisturePercentage * \
                materialsDictionary["material{0}".format(i)].mass

        for i in range(len(materialsDictionary)):
            totalWaterMass = totalWaterMass + materialsDictionary["material{0}".format(i)].water_weight

        totalMass = greenLayerTotalMass + brownLayerTotalMass
        waterMassNeeded = ((idealMoisture) * totalMass) - totalWaterMass

        comboList["combo{0}".format(goodComboCounter)] = {}

        comboList["combo{0}".format(goodComboCounter)]["comboNum{0}".format(goodComboCounter)] = goodComboCounter
        for i in range(len(materialsDictionary)):
            # comboList["combo{0}".format(goodComboCounter)]["material{0}Mass".format(i)] = materialsDictionary["material{0}".format(i)].mass
            comboList["combo{0}".format(goodComboCounter)][materialsDictionary["material{0}".format(i)].name + "Mass"] = \
            materialsDictionary["material{0}".format(i)].weight

        # comboList["combo{0}".format(goodComboCounter)]["leavesMass{0}".format(goodComboCounter)] = leaves.mass
        # comboList["combo{0}".format(goodComboCounter)]["paperMass{0}".format(goodComboCounter)] = paper.mass
        # comboList["combo{0}".format(goodComboCounter)]["cardboardMass{0}".format(goodComboCounter)] = cardboard.mass
        # comboList["combo{0}".format(goodComboCounter)]["trimmingsMass{0}".format(goodComboCounter)] = trimmings.mass
        # comboList["combo{0}".format(goodComboCounter)]["totalComboNum{0}".format(goodComboCounter)] = totalCombinations

        comboList["combo{0}".format(goodComboCounter)]["totalDiff{0}".format(goodComboCounter)] = totalDiff
        comboList["combo{0}".format(goodComboCounter)]["waterNeeded{0}".format(goodComboCounter)] = waterMassNeeded

        goodComboCounter += 1

    # print("c:", cardboard.mass)
    # print("p:", paper.mass)
    # print("l:", leaves.mass)

    # graphX.append(totalCombinations)
    # graphY.append(totalCarbonMass / totalNitrogenMass)

print(comboList)

# okay now for some sorting fun

diffs = []
for pp in range(len(comboList)):
    diffs.append(comboList["combo{0}".format(pp)]["totalDiff{0}".format(pp)])
# print(diffs)

diffsLength = len(diffs)
sortedDiffs = []

x = 0
while x < diffsLength:
    minValue = 100000000000000

    for i in range(len(diffs)):
        if diffs[i] < minValue:
            minValue = diffs[i]

    diffs.remove(minValue)
    sortedDiffs.append(minValue)

    x += 1

#  print(diffs)
# print(sortedDiffs)

comboListListified = []

for i in range(len(comboList)):
    comboListListified.append(comboList["combo{0}".format(i)])

ultiCounter = 0
while ultiCounter < (len(sortedDiffs)):
    # print('pp',len(sortedDiffs))
    for i in range(0, (len(sortedDiffs))):
        # print(i)
        # print(comboListListified[i])
        # print(sortedDiffs[ultiCounter])
        # print(i)
        if comboListListified[i]["totalDiff{0}".format(i)] == sortedDiffs[ultiCounter]:
            sortedDiffs.insert(ultiCounter, comboListListified[i])
            sortedDiffs.remove(comboListListified[i]["totalDiff{0}".format(i)])

    #   print(sortedDiffs)

    # print('for loop done')
    ultiCounter += 1

print('final', sortedDiffs)

# print(CNratios)

# with open('C:\PyCharm Community Edition 2019.3.3\PycharmProjects\cp1\outputshellyea\compostcombinations.csv',
#         mode='w') as csv_file:
#  fieldnames = ['number', 'CNratio']
# writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

#  writer.writeheader()

# for i in range(totalCombinations):

#    if i == 0:
#       continue;

#  writer.writerow({'number': i,
#              #'mass1': CNratios["number{0}".format(i)]['mass1'],
# 'mass2': CNratios["number{0}".format(totalCombinations)]['mass2'],
#             'CNratio': CNratios["number{0}".format(i)]["CNRatio"]})
'''
goodComboTotalNumbers = []

for i in range(goodComboCounter):
    goodComboTotalNumbers.append(comboList["combo{0}".format(i)]["totalComboNum{0}".format(i)])

print(goodComboTotalNumbers)
'''

# for i in range(totalCombinations):
#   if i == 0:
#      i = 1

# graphX.append(i)


# for i in range(len(CNratios)):
#   if i == 0:
#      i = 1
# graphY.append(CNratios["number{0}".format(i)]["CNRatio"])

'''
import matplotlib.pyplot as plt 

# x-axis values 
x = graphX
# y-axis values 
y = graphY

# plotting points as a scatter plot 
plt.scatter(x, y, label= "stars", color= "green",  marker= "*", s=30) 

# x-axis label 
plt.xlabel('x - axis') 
# frequency label 
plt.ylabel('y - axis') 
# plot title 
plt.title('My scatter plot!') 
# showing legend 
plt.legend() 

# function to show the plot 
plt.show()
'''
