import random

# Basic character info for use in text prompts and gameplay purposes
character = {"Name": "", "Gender": "", "Tenacity": 0, "Willpower": 0, "Luck": 0}

# Locations and their modifiers.
# Location modifiers affect chance of events occurring, finding items
# and whether or not a location contains a character.
locations = {"Castle Entrance": ["rare", "empty", "Lost Spirit"],
             "Graveyard": ["uncommon", "haunted", "null"],
             "Abandoned Villa": ["common", "far", "Scrapper"],
             }
currentLocation = "Castle Entrance"
actualLocation = locations[currentLocation]
# If hunger level reaches 0, game ends
hunger_level = 5
# If sanity level reaches 0, game ends. Sanity level changes main ending
sanity = 3
# Characters inventory, InvSpace is how many items the character can carry at once
inventory = {"Rations": 0,
             "Sanity Pills": 0,
             "invSpace": 4,
             "Backpack": False,
             }

# Story conditions
stepStory = 0
move = 0

print("Welcome to GraveKeeper!")
character["Name"] = input("Input Name:").title()
while True:
    genderInput = input("Input Male or Female:")
    if genderInput == "Male":
        character["Gender"] = "his"
        break
    elif genderInput == "Female":
        character["Gender"] = "her"
        break

print("\nYou have four points to spend on %s's stats."%(character["Name"]))
print("\nType \"Tenacity\" to increase your character's resilience to hunger.")
print("Type \"Willpower\" to increase your character's mental resilience.")
print("Type \"Luck\" to increase your character's chance of finding items.")

stats = 4


# Functions for events and using items


def inventoryCheck():
    global hunger_level
    global sanity
    print("You have {} rations!".format(inventory["Rations"]))
    print("You have {} sanity pills!".format(inventory["Sanity Pills"]))
    if inventory["Backpack"] == True:
        print("You have a backpack!")
    else:
        print("You have no backpack!")
    inventoryChoice = input("Press 1 to use rations. Press 2 to use sanity pills. Press 3 to return to menu.")
    if inventoryChoice == "1":
        if inventory["Rations"] > 0:
            print("{} eats a Ration. It tastes like stale bread and gelatinous protein. Delicious!".format(character["Name"]))
            hunger_level += 2
            inventory["Rations"] -= 1
            return
        else:
            print("{} has no rations. Better starve then.".format(character["Name"]))
            return
    if inventoryChoice == "2":
        if inventory["Sanity Pills"] > 0:
            print("{} pops some sanity pills in his mouth. He feels ravenously hungry, but more stable.".format(character["Name"]))
            hunger_level -= 1
            sanity += 1
            inventory["Sanity Pills"] -= 1
            return
        else:
            print("{} has no sanity pills. You can still pretend to take them though, maybe that'll help.".format(character["Name"]))
            return
    if inventoryChoice == "3":
        return

def scavenge():
    global inventory
    global sanity
    global hunger_level
    hungercheck = random.randint(0, 10) + character["Luck"] / 2 + character["Willpower"]
    if hungercheck < 6.5:
        print("\nScavenging is hungry business! {} grows malnourished.".format(character["Name"]))
        hunger_level -= 1
    if actualLocation[1] == "haunted":
        print("\nScavenging in this place was a horrible idea. The very shadows of this place eat at {}'s mind.".format(character["Name"]))
        sanity -= 1
    if actualLocation[0] == "rare":
        scavengeCheck = random.randint(0, 7) + character["Luck"] / 2
        if scavengeCheck > 6.5:
            print("\nWhether it be the guiding hand of God or insatiable luck, {} somehow manages to find something!".format(character["Name"]))
            outcome = [foundSomething(), sanity, hunger_level]
            return outcome
        else:
            print("\n What did {} expect to find? There's nothing here but lingering regrets, and a culminating desire to drink.".format(character["Name"]))
            return
    if actualLocation[0] == "uncommon":
        scavengeCheck = random.randint(0, 7) + character["Luck"] / 2
        if scavengeCheck > 6.5:
            print("\nToday is {}'s lucky day! Something has been found!".format(character["Name"]))
            outcome = [foundSomething(), sanity, hunger_level]
            return outcome
        else:
            print("\n Better luck next time. Nothing's here.")
            return
    if actualLocation[0] == "common":
        scavengeCheck = random.randint(0, 7) + character["Luck"] / 2
        if scavengeCheck > 4.5:
            print("\nIt's hard to miss good loot here. {} finds something!".format(character["Name"]))
            outcome = [foundSomething(), sanity, hunger_level]
            return outcome
        else:
            print("\nDespite initial appearances, this place is truly devoid of anything of value. Unlucky!")
            return
    print()

def foundSomething():
    global inventory
    global sanity
    global hunger_level

    if inventory["Backpack"] == False:
        scavengeCheck = random.randint(0, 7)
        if scavengeCheck <= 3:
            print("{} finds a ration pack!".format(character["Name"]))
            inventory["Rations"] += 1
            return
        elif scavengeCheck <= 6:
            print("{} finds some sanity pills!".format(character["Name"]))
            inventory["Sanity Pills"] += 1
            return
        else:
            print("{} finds a backpack! Inventory space up!".format(character["Name"]))
            inventory["Backpack"] = True
            inventory["invSpace"] += 3
            return
    elif inventory["Backpack"] == True:
        scavengeCheck = random.randint(0, 1)
        if scavengeCheck <= 0:
            print("{} finds a ration pack!".format(character["Name"]))
            inventory["Rations"] += 1
            return
        if scavengeCheck <= 1:
            print("{} finds some sanity pills!".format(character["Name"]))
            inventory["Sanity Pills"] += 1
            return

def locationHungerCheck():
    global hunger_level
    actualLocation = locations[currentLocation]
    if actualLocation[1] != "far":
        hungercheck = random.randint(1, 10) + character["Tenacity"]
        if hungercheck < 3:
            print(
                "\nThe journey siphons {}'s vitae, {} is now hungrier.".format(character["Name"], character["Gender"]))
            hunger_level -= 1
    else:
        hungercheck = random.randint(1, 10) + character["Tenacity"]
        if hungercheck < 6:
            print("\nThe far journey to the stow-away locale has starved {}'s essences, {} is now far hungrier.".format(
                character["Name"], character["Gender"]))
            hunger_level -= 2
        else:
            print(
                "\nThe far journey to the stow-away locale should have starved {}'s essences, but {} tenaciously clings to life.".format(
                    character["Name"], character["Name"]))
    return

def locationSanityCheck():
    global sanity
    actualLocation = locations[currentLocation]
    if actualLocation[1] != "haunted":
        sanitycheck = random.randint(1, 22) + character["Willpower"] * 2
        if sanitycheck < 3:
            print(
                "\n The callous and stifling journey has undone {}'s frail, enfeebled mind, {} sanity is now one step closer to the gaping abyss.".format(
                    character["Name"], character["Gender"]))
            sanity -= 1
    else:
        sanitycheck = random.randint(1, 22) + character["Willpower"] * 2
        if sanitycheck < 12:
            print(
                "\n Something horrific in this place stirs the precipice of {}'s mind, {} sanity is now one step closer to the gaping abyss.".format(
                    character["Name"], character["Gender"]))
            sanity -= 1
        elif sanitycheck < 6:
            print("\n Some sights are never forgotten. {}'s sanity is now two steps closer to the gaping abyss.".format(character["Name"]))
            sanity -= 2
    return


# Inputs character's starting statistics
while stats > 0:
    print("\n%s has %s stat points left."%(character["Name"], stats))
    statInput = input("Input stat to increase:")
    if statInput == "Tenacity":
        character["Tenacity"] += 1
        stats -= 1
        print("%s's Tenacity is now %s"%(character["Name"], character["Tenacity"]))
    elif statInput == "Willpower":
        character["Willpower"] += 1
        stats -= 1
        print("%s's Willpower is now %s"%(character["Name"], character["Willpower"]))
    elif statInput == "Luck":
        character["Luck"] += 1
        stats -= 1
        print("%s's Luck is now %s"%(character["Name"], character["Luck"]))

print("\nHere stands {}. Naught but one simple graveswarden, deigned to guard the *man-earth* and little more. Across {} grime-ridden brow, a faint flickering dashes to the looming castle ahead.".format((character["Name"]), character["Gender"], stats))
choice = 0
while True:
    actualLocation = locations[currentLocation]
    #hunger and sanity check
    if move == 1:
        locationHungerCheck()
        locationSanityCheck()
        move = 0

    if hunger_level > 3:
        hungerstatus = "Sated"
    elif hunger_level < 4 and hunger_level > 1:
        hungerstatus = "Hungry"
    elif hunger_level == 1:
        hunger_status = "Starving"
    elif hunger_level < 3:
        print("Ending 1 of 3: Famine's Embrace (Die of starvation!)")
        break

    if sanity == 3:
        sanitystatus = "Sane"
    elif sanity < 3 and sanity > 1:
        sanitystatus = "Paranoid"
    elif sanity == 1:
        sanitystatus = "Psychotic"
    elif sanity < 1:
        print("Ending 2 of 3: The Raving Graveswarden (Lose your mind!)")
        break

    print("\n{} is {} and {}".format(character["Name"], hungerstatus, sanitystatus))
    checktips = random.randint(1, 2)
    if checktips == 2:
        print("TIP: Remember to check your inventory, you need to eat and take your pills to survive!")
    print("\n{} arrives at the {}.".format(character["Name"], currentLocation))
    if actualLocation[2] != "null":
        if actualLocation[2] == "Lost Spirit":
            print("Before {} gutters a hollow vision-being, shifting-shape in the glimmering of the Grand Castle's moonshade.".format(character["Name"]))
        else:
            print("Before {} huddles a lonesome Scrapper. The patchwork of burnt metal and rust-flaked rivets make a gradient of newflesh across the hermit's body.".format(character["Name"]))
            print("Her hair is knotted into a rat's nest and held high by a barrette of broken glass.")
    print("What is there to do?")
    print("1. Go somewhere else")
    print("2. Scavenge")
    print("3. Check inventory")
    if actualLocation[2] != "null":
        print("4. Talk")
    choice = input("Input number to enact your will: ")
    if choice == "1":
        while True:
            print("Choose where to go")
            if currentLocation == "Castle Entrance":
                print("1. Graveyard")
                print("2. Abandoned Villa (far away)")
                locationChoice = input("Input number to enact your will: ")
                if locationChoice == "1":
                    currentLocation = "Graveyard"
                    move = 1
                    break
                else:
                    currentLocation = "Abandoned Villa"
                    move = 1
                    break
            if currentLocation == "Graveyard":
                print("1. Castle Entrance")
                print("2. Abandoned Villa (far away)")
                locationChoice = input("Input number to enact your will: ")
                print(locationChoice)
                if locationChoice == "1":
                    currentLocation = "Castle Entrance"
                    move = 1
                    break
                else:
                    currentLocation = "Abandoned Villa"
                    move = 1
                    break
            if currentLocation == "Abandoned Villa":
                print("1. Castle Entrance")
                print("2. Graveyard")
                locationChoice = input("Input number to enact your will: ")
                if locationChoice == "1":
                    currentLocation = "Castle Entrance"
                    move = 1
                    break
                else:
                    currentLocation = "Graveyard"
                    move = 1
                    break
    elif choice == "2":
        while True:
            if actualLocation[0] == "empty":
                print("\n Nothing here to scavenge.")
                break
            elif inventory["Rations"] + inventory["Sanity Pills"] == 4:
                print("\n Your inventory is full! Try using an item before you scavenge again.")
                break
            print("\n Are you sure? Scavenging may result in consequences. Choose your location wisely.")
            scavengeChoice = input("Press 1 to continue with the scavenge, press 2 to return to menu: ")
            if scavengeChoice == "1":
                scavenge()
                break
            else:
                break
    elif choice == "3":
            inventoryCheck()

    elif choice == "4":
        if actualLocation[2] != "null":
            if actualLocation[2] == "Lost Spirit":
                if stepStory < 2:
                    print("\nThe entity phrases out less than a mere whisper. He speaks only of days long gone by.")
                    print("\nIn his whistling tongue, you make out two words:")
                    print("\nWAITING. INSIDE.")
                    print("\nI suppose we have no better things to do.")
                if stepStory == 0:
                    stepStory = 1
                if stepStory == 2:
                    print("\n Without a trace, the dithering phantom liquefacts into the thin aether.")
                    print("\n The slot traces the lines of the lock. The hammer-key pulls back, and the rust-drenched gate opens to man once more. Yonder to the castle, we go.")
                    print("...")
                    print("\n An all-familiar smell encapsulates your nasal cavity. It's one you cannot forget.")
                    print("\n It's one you've worked your whole life to never forget.")
                    print("\n Arrays 'pon arrays of corpses line the hallways in perfect harmony. Stacked for my pleasure.")
                    print("\n The age-old idiom crawls its way back into your brain-folds: It is not the grave-digger's duty to ask questions.")
                    print("...")
                    print("\n Ending 3 of 3: A Gravedigger's Duty Is Never Done (You don't get paid enough for this.)")
                    break
            else:
                if inventory["Backpack"] == False:
                    print("\nThe scrap-clad hermit screams in a tongue of her own invention.")
                    print("\nShe points to her back. Then to a suspiciously-hammer-shaped key. I think she wants a backpack?")
                    print("\nWe'll have to go looking around, I suppose.")
                else:
                    print("\nShe assails the backpack with thief-like intent, coupled again with her barbaric savoir faire: the unforgettable banshee-bellow.")
                    print("\nFrom the rust-moles of her sun-seared skin, the eye of the prize reveals itself.")
                    print("\nTHE KEY.")
                    print("\nLet us not keep this a secret for long. To the castle!")
                    inventory["Backpack"] = False
                    stepStory = 2
