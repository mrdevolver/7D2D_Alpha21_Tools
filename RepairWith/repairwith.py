import re
import os

while True:
    # Introduction
    print("7 Days to Repair With What?! v0.1 by mr.devolver\n")

    # Read Localization.txt and store the values in a dictionary
    localization_data = {}
    with open('Localization.txt', 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            if not re.search("Desc", parts[0].strip()):
                key = parts[0].strip()
                value = ','.join(parts[1:]).strip()
                localization_data[key] = value

    # Take user input for the item of interest
    user_input = input("Enter the name of an item of interest (case insensitive, partial names allowed):\n\n")

    # Case insensitive search for user's item of interest in Localization.txt and store the first entry on the line with the found item
    item_id = None
    item_name = None
    for key, value in localization_data.items():
        if re.search(user_input.lower(), value.lower()):
            item_id = key
            item_name = value
            print("Item name:", item_name)
            print("Item ID:", item_id)
            break

    # Read items.xml and find the value from its property named "RepairTools"
    repair_tools_value = None
    if item_id:
        with open('items.xml', 'r') as file:
            content = file.read()
            match = re.search(fr'<item name="{item_id}">(.*?)</item>', content, re.DOTALL)
            if match:
                item_properties = match.group(1)
                repair_tools_match = re.search(r'<property name="RepairTools" value="([^"]+)"', item_properties)
                if repair_tools_match:
                    repair_tools_value = repair_tools_match.group(1)
                    print("ID of the repair item:", repair_tools_value)
                else:
                    print("This item has no RepairTools property. It could mean the item is not meant to be repairable.")
            else:
                print(f"Item ID {item_id} was not found in items.xml of this mod!\nIt could mean that the item ID is not associated with any in-game item.")
    else:
        print(f"I was unable to find the item of interest in Localization.txt of this mod.\nMake sure you're typing the name correctly.\nIf the name is correct and it still cannot be found, it could be a part of a different mod, or a vanilla item!")

    # Search for the extracted value in Localization.txt, extract the second entry on the same line of the match and display it to the user
    if repair_tools_value is not None:
        for key, value in localization_data.items():
            if repair_tools_value.lower() == key.lower():
                print("Repair with:", value)
                break
        else:
            print(f"I was unable to find the name of the repair item for the item of interest in Localization.txt of this mod.\nIt could mean the repair item associated with it is a vanilla item or an item from a different mod!")

    # Finish
    input("\nPress Enter to continue...")
    # Clear the console window
    os.system('cls' if os.name == 'nt' else 'clear')