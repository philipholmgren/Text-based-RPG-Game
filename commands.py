import fight
import library
from world_creator import *
from character_class import Character
from merchant_class import Merchant
from account_handler import *

""" Contains commands available through the input loop. """

_HELP = "help"
_WIELD_ITEM = "wield"
_UNWIELD_ITEM = "unwield"
_TAKE_ITEM = "take"
_DROP_ITEM = "drop"
_EQUIP_ITEM = "equip"
_UNEQUIP_ITEM = "unequip"
_INVENTORY = "inventory"
_LOOT = "loot"
_STATUS = "status"
_CONSUME_ITEM = "consume"
_EXAMINE = "examine"
_LIGHT = "light"
_EXTINGUISH = "extinguish"
_GO = "go"
_BUY = "buy"
_SELL = "sell"
_ATTACK = "attack"
_QUIT = "quit"
_SAVE = "save"
_OPEN = "open"


_PLAYER_COMMANDS = [
    _HELP,
    _WIELD_ITEM,
    _UNWIELD_ITEM,
    _TAKE_ITEM,
    _DROP_ITEM,
    _EQUIP_ITEM,
    _UNEQUIP_ITEM,
    _INVENTORY,
    _LOOT,
    _STATUS,
    _CONSUME_ITEM, 
    _EXAMINE,
    _LIGHT, 
    _EXTINGUISH, 
    _GO,
    _BUY,
    _SELL,
    _ATTACK, 
    _QUIT, 
    _SAVE,
    _OPEN
]   

def displayHelpMenu():
    """Displays available commands."""
    print(18 * "*", "AVAILABLE COMMANDS", 18 * "*")
    print("- HELP: Shows this menu.")
    print("- ATTACK <ENEMY>: Attack someone! Or something!")
    print("- STATUS: Display information about yourself.")
    print("- WIELD <ITEM>: Wield a weapon from your inventory.")
    print("- UNWIELD <ITEM>: Unwield your wielded weapon.")
    print("- TAKE <ITEM>: Add an item to your inventory.")
    print("- DROP <ITEM>: Discard of an item in your inventory.")
    print("- EQUIP <ITEM>: Equip an item, such as a helmet.")
    print("- UNEQUIP <ITEM>: Remove an equipped item.")
    print("- INVENTORY: List all the items your are carrying.")
    print("- LOOT <TARGET>: Loot a slain enemy.")
    print("- CONSUME <ITEM>: Drink a potion, or eat a biscuit.")
    print("- EXAMINE <ITEM>: Examine a thing or a room.")
    print("- LIGHT <ITEM>: Light a fire.")
    print("- EXTINGUISH <ITEM>: Put a fire out.")
    print("- GO <DIRECTION>: Go somewhere and do something.")
    print("- BUY <ITEM>: Buys an item from the shop.")
    print("- SELL <ITEM>: Sells an item to the shop.")
    print("- SAVE: Save your progress.")
    print("- QUIT: Leave the game, for some reason.")
    print(56 * "*")

def playerStatus():

    print(18 * "*", "THIS IS YOU", 18 * "*" )
    print(f"*\tPlayer Level: {player.getLevel()} \t XP: {player.getXP()}/{player.getLevel() * 200}")
    print(f"*\tPlayer Health: {player.getHP()} \t Armor: {player.getArmor()}")
    print(f"*\tStrength: {player.getStr()} \t\t Dexterity: {player.getDex()}")
    print(f"*\tCoins: {int(player.getCoin())}\t\t Weight: {player.getTotalWeight()}")
    print(49 * "*")

    
def movePlayer(userMovement, currentRoom):
    """Checks if exit exists and moves the player if true."""
    if userMovement == "west":
        if currentRoom.getExitWest():
            return currentRoom.getExitWest()
        else: 
            print("You run into a wall.")
    elif userMovement == "east":
        if currentRoom.getExitEast():
            return currentRoom.getExitEast()
        else: 
            print("You run into a wall.")
    elif userMovement == "north":
        if currentRoom.getExitNorth():
            return currentRoom.getExitNorth()
        else: 
            print("You run into a wall.")
    elif userMovement == "south":
        if currentRoom.getExitSouth():
            return currentRoom.getExitSouth()
        else: 
            print("You run into a wall.")
    else:
        print("You can't go there.")


def attack(target, currentRoom):
    """Checks if target is in room and if true calls the letsFight() function."""
    if library.canPlayerSee(currentRoom):
        for object in currentRoom.getObjects():
            if object.getType().lower() == target.lower() and object.getObjectType() == "monster":
                fight.letsFight(player, object)
                return True
       
def consume(item_to_consume, item_number=None):
    """Checks what potion you want to drink and alters stats accordingly."""
    
    if item_number:
        try:
            item_number = int(item_number)
            potion_list = []
            for item in player.getInventory():
                if item.getObjectType() == "potion" and item_to_consume.lower() == "potion":
                    potion_list.append(item)
            if item_number > len(potion_list) or item_number == 0:
                return False
            else:
                potion_list[item_number-1].setPotionEffect(player)
            return True
        except ValueError:
            return False
    
    else:
        for item in player.getInventory():
            if item.getObjectType() == "potion" and item_to_consume.lower() == "potion":
                item.setPotionEffect(player)
            return True

    

def examineMonster(monster):
    """Prints the description and inventory of target monster."""
    print(monster.getDesc())
    print("It's carrying: ")
    for item in monster.getInventory():
        print(item.getType())

#takes user input and prints info about it
def examine(toLookAt, currentRoom):

    if toLookAt == "room":
        library.printInterface(currentRoom)
    
    else :
        for object in currentRoom.getObjects():
            if object.getType().lower() == toLookAt.lower():
                if object.getObjectType() == "monster":
                    examineMonster(object)
                elif object.getObjectType() in ("item", "potion"):
                    print(object.getDesc())
                elif object.getObjectType() == "merchant":
                    print("He has these items for sale: ")
                    for item in object.getInventory():
                        print(f"{item.getType().title()} for {int(item.getValue() * 1.2)} coins.")

        for object in player.getInventory():
            if object.getType().lower() == toLookAt.lower():
                if object.getObjectType() == "monster":
                    examineMonster(object)
                elif object.getObjectType() in ("item", "potion"):
                    print(object.getDesc())       

 
            
def manageEquipment(command, item):
    """Check if you have armor in your inventory to equip and if you are wearing
       any armor, then sets armor status to equipped accordingly."""
    for armor in player.getInventory():
        if armor.getItemType() == "armor" and armor.getType().lower() == item.lower():  
            if command == "equip" and not player.isEquipped(item):
                player.setEquipArmor(item)
                player.setArmor(armor.getDamageMitigation())
                return True      
            elif command == "unequip" and player.isEquipped(item):
                player.setUnequipArmor(item)
                player.setArmor(-armor.getDamageMitigation())
                return True
        else:
            print("You don't have that item.")
    
def manageWeapons(command, item):
    """Checks if you have weapon in inventory, if it is a weapon and if all 
       true changes wielded status accordingly."""
    for weapon in player.getInventory():
        if weapon.getType().lower() == item.lower() and weapon.getItemType() == "weapon":
            if command == "wield" and not player.getWielded():
                player.setWielded(weapon)
                return True
            elif command == "unwield" and weapon == player.getWielded():
                player.setUnwield(weapon)
                return True
        else: 
            print("I can't do that.")
            return False
    else:
        print("I don't have that item.")    
        

def trade(arg, object):
    """Trading items with the merchant!"""
    if arg.lower() == "buy":
        for item in merchant.getInventory():
            if item.getType().lower() == object.lower() and player.getCoin() >= item.getValue():
                merchant.sell(item)
                merchant.setCoin(int(item.getValue() * 1.2))
                player.buy(item)
                player.setCoin(int(-item.getValue() * 1.2))
                player.getInventory().append(item)
                merchant.getInventory().remove(item)
                print(f"You purchased {item.getType()} for {int(item.getValue() * 1.2)} coins.")
                return True
            else:
                print("The Merchant says: 'You can´t afford that.'")
                return False
        else:
            print("The Merchant says: 'I dont have that.'")
    elif arg.lower() == "sell":
        for item in player.getInventory():
            if item.getType().lower() == object.lower() and merchant.getCoin() >= item.getValue():
                if item.getItemType() == "weapon":
                    manageWeapons("unwield", object)
                elif item.getItemType() == "armor":
                    manageEquipment("unequip", object)
                player.sell(item)
                player.setCoin(int(item.getValue() * 0.8))
                merchant.buy(item)
                merchant.setCoin(int(-item.getValue() * 0.8))
                print(f"You sold {item.getType()} for {int(item.getValue() * 0.8)} coins.")
                return True
            else:
                print("The Merchant says: 'I can't afford to buy that item from you, sorry!'")
                return False
        else:
            print("The Merchant says: 'You can't sell stuff you dont have!'")
            return False
    else:
        print("The Merchant says: 'Can't do that, sorry!'")


def takeItem(item_to_take, currentRoom):
    """If item in room inventory, remove from room and add to player inventory."""
    for item in currentRoom.getObjects():
        if item.getObjectType() in ("item", "potion"):
            if item.getType().lower() == item_to_take.lower() and library.checkWeight(item):
                currentRoom.getObjects().remove(item)
                player.getInventory().append(item)
                player.setTotalWeight(item.getWeight())
                return True
            

def dropItem(item_to_drop, currentRoom):
    """If item's in inventory, remove from inventory and add it to room inventory."""
    for item in player.getInventory():
        if item.getType().lower() == item_to_drop.lower():
            if item == player.getWielded():
                manageWeapons("unwield",item_to_drop)
            elif player.isEquipped(item_to_drop):
                manageEquipment("unequip", item_to_drop)
            elif item_to_drop == "torch":
                item.setOnOff(False)
                player.setIlluminated(False)
            currentRoom.getObjects().append(item)
            player.getInventory().remove(item)
            player.setTotalWeight(-item.getWeight())
            return True


def checkInventory():
    """Prints player inventory."""
    print("You're carrying the following items:")
    for item in player.getInventory():
        print(item.getType().title())



def loot(currentRoom, itemToLoot):
    """Checks if monsters are dead and adds their inventory to player inventory."""
    for object in currentRoom.getObjects():
        if object.getObjectType() == "monster" and object.getIsAlive() == False and object.getInventory():
            while object.getInventory():
                loot = object.getInventory().pop()
                player.getInventory().append(loot)
            return True


def light(item):
    """Checks if you have torch in inventory, lights it if true."""
    for object in player.getInventory():
        if object.getType().lower() == item.lower() and item.lower() == "torch":
            if object.getOn() != True:
                object.setOnOff(True)
                player.setIlluminated(True)
                return True
            else:
                print("The torch is already lit.")
                return False
        else:
            print("You can't light that.")
            return False
    else:
        print("I don´t have that.")

def extinguish(item):
    """Checks if torch is in player inventory and extinguishes if its lit."""
    for object in player.getInventory():
        if object.getType().lower() == item.lower() and object.getType() == "torch" and object.getOn():
            object.setOnOff(False)
            player.setIlluminated(False)
            return True

def open():
    for item in player.getInventory():
        if item.getDesc() == "key":
            