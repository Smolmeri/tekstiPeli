"""
Created on Tue Apr 24 11:36:23 2018

@author: otto, oona, tom


"""
import mysql.connector
import sys
import time

#look-command fully functional
def look(loc):
    cur = db.cursor()
    sql = "SELECT Description FROM Location WHERE LocationID ="+ str(loc)    
    cur.execute(sql)
    result = cur.fetchall()
    for row in result:
        my_print(row[0])
    return

#look for move-command (gets name from Location)
def move_look(loc):
    cur = db.cursor()
    sql = "SELECT Name FROM Location WHERE LocationID ="+ str(loc)    
    cur.execute(sql)
    result = cur.fetchall()
    for row in result:
        my_print(row[0])
    return    

#show-command
def show_objects(loc):
        cur = db.cursor()
        sql = "SELECT Name FROM Item WHERE LocationID ="+ str(loc) + " ORDER BY NAME"
        cur.execute(sql)
        #check if more than one item available
        result = cur.fetchall()
        if len(result) > 0:
            my_print("You see the following:")
            for row in result:
                my_print(" - " + row[0])
        else:
            my_print("Nothing here.")
        return
    
#move
#move
def move(loc, direction):
    destination = loc
    cur = db.cursor()
    sql = "SELECT Destination FROM Movement WHERE Direction='" + str(direction) + "' AND Source='" + str(loc) +"' AND Locked = 0;"
    cur.execute(sql)
    if cur.rowcount>=1:
        for row in cur.fetchall():
            destination = row[0]
        if destination==7 or destination==17:
            none(destination)
            
    else:
        destination = loc; #movement not possible, restore location
    return destination

#check inventory
def inventory():
    cur = db.cursor()
    sql = "SELECT Name FROM item WHERE PlayerID=1"
    cur.execute(sql)
    if cur.rowcount>=1:
        my_print("You carry the following items:")
        for row in cur.fetchall():
            my_print(" - " + row[0])
    else:
        my_print("You don't carry anything.")
    return

#take
def take_all(loc):
    cur = db.cursor()
    sql = "SELECT Item.Name FROM Item WHERE LocationId = " + str(loc) +" ORDER BY Name"
    cur.execute(sql)
    if cur.rowcount > 0:
        my_print("You looted:")
        for row in cur.fetchall():
            my_print(" - " + row[0])
        sql = "UPDATE Item SET PlayerID = 1, LocationID = NULL WHERE LocationId = " + str(loc) +" "
        cur.execute(sql)
        #if loc=12 (treasure) update desc
        if loc == 12:
            sql = "UPDATE Location SET Description=\"There's a beam of sunlight shining to a corner.\" WHERE LocationID=12;"
            cur.execute(sql)
        #if loc=5 (cargo hold) update desc
        elif loc == 5:
            sql = "UPDATE Location SET Description=\"You are in the cargo hold. It's dark.\" WHERE LocationID=5;"
            cur.execute(sql)
        #if loc=4 (deck) update desc
        elif loc == 4:
            sql = "UPDATE Location SET Description=\"You are on the deck of the shipwreck. The old floor feels quite unstable beneath you. There's a door to the cargo hold below you.\" WHERE LocationID=4;"
            cur.execute(sql)
    else:
        my_print("Nothing to loot here.")
    return

# take only one item
def take(target, loc, action):
    cur = db.cursor()
    sql = "SELECT Name FROM Item WHERE LocationID = " + str(loc) +" AND Name = '" + str(target) + "'"
    cur.execute(sql)
    if cur.rowcount == 1:
        my_print("You took " + str(target))
        sql = "UPDATE Item SET PlayerId = 1, LocationId = NULL WHERE Name = '" + str(target) + "'"
        cur.execute(sql)
    elif cur.rowcount > 1:
        my_print("You took:")
        for row in cur.fetchall():
            my_print(" - " + row[0])    
        sql = "UPDATE Item SET PlayerId = 1, LocationId = NULL WHERE Name = '" + str(target) + "'"
        cur.execute(sql)
    else:
        my_print("You can't " + str(action) + " " + str(target) + ".")
        
#drop
def drop(target, loc):
    cur = db.cursor()
    sql = "UPDATE Item SET PlayerID = NULL, LocationID = " + str(loc) + " WHERE Name='" + str(target) + "'" 
    cur.execute(sql)
    sql = "SELECT Name FROM ITEM WHERE PlayerID = 1 ORDER BY Name"
    cur.execute(sql)
    if cur.rowcount > 0:
        my_print("You are carrying:")
        for row in cur.fetchall():
            my_print(" - " + row[0])
    else:
        my_print("You don't carry anything.")
    return cur.rowcount

#use key to open chest passage
def usekey(loc):
    cur = db.cursor()
    sql = "SELECT Item.Name FROM Player INNER JOIN Item ON Player.PlayerID = Item.PlayerID AND ItemID = 9;"
    cur.execute(sql)
    result = cur.fetchall()
    if cur.rowcount > 0 and loc == 10:
        sql = "SELECT Locked FROM Movement WHERE MovementID='F10Tr' AND Locked = 1"
        cur.execute(sql)
        result = cur.fetchall()
        if len(result) > 0:
            sql = "UPDATE Movement SET Locked = 0 WHERE MovementID='F10Tr' AND Locked=1"
            cur.execute(sql)
            my_print("The gate to the mysterious treasure is now unlocked!")
        else:
           my_print("The gate is already open! Go west young man!")
            
            
    elif cur.rowcount > 0 and loc!= 10:
        my_print("There's nothing to open here.")
    elif cur.rowcount == 0 and loc == 10:
        my_print("The gate is too rigid to open without the key!")
    else:
        my_print("I don't have anything to open.")
    return

#use light to open cave
def ignite():
    cur = db.cursor()
    sql = "SELECT Item.Name FROM Player INNER JOIN Item ON Player.PlayerID = Item.PlayerID AND ItemID = 10;"
    cur.execute(sql)
    result = cur.fetchall()
    if cur.rowcount > 0 and loc == 16:
        sql = "SELECT Locked FROM Movement WHERE MovementID='CeCa' AND Locked = 1"
        cur.execute(sql)
        result = cur.fetchall()
        if len(result) > 0:
            sql = "UPDATE Movement SET Locked = 0 WHERE MovementID='CeCa' AND Locked=1"
            cur.execute(sql)
            my_print("The light hits the walls of the moist cave and you can see your steps.")
        else:
            my_print("The lighter is already ignited! Watch your fingers!")
    elif cur.rowcount > 0 and loc!= 16:
        my_print("There's nothing to ignite here.")
    elif cur.rowcount == 0 and loc == 16:
        my_print("You don't have anything to ignite! Maybe a lighter would help.")
    else:
        my_print("I don't have anything to ignite.")
    return
    
#inspect item
def inspect(target):
    cur = db.cursor()
    sql = "SELECT Description FROM Item WHERE Name = '" + str(target) + "' "
    cur.execute(sql)
    if cur.rowcount == 0:
        my_print("You don't have " + str(target) + ".")
    else:
        for row in cur.fetchall():
            my_print(row[0])

#use machete, location 7
def machete():
    #testataan onko pelaajalla machete
    cur = db.cursor()
    sql = "SELECT PlayerId FROM Item WHERE ITEMID=2;"
    cur.execute(sql)
    for row in cur.fetchall():
        #jos on machete, tarkistetaan onko python elossa
        if row[0]==1:
            cur = db.cursor()
            sql = "SELECT Health FROM Npc WHERE NPCId=1;"
            cur.execute(sql)
            for row in cur.fetchall():
                #Tapetaan python
                if row[0]==1:
                    cur = db.cursor()
                    sql = "UPDATE NPC SET Health=0 WHERE NPCID=1;"
                    cur.execute(sql)
                    sql = "UPDATE LOCATION SET Description = 'There is just a dead python here, it sure is big.' WHERE LocationID=7;"
                    cur.execute(sql)
                    #update location name
                    sql = "UPDATE Location SET Name=\"You are in the forest. This is where you killed the python.\" WHERE LocationID=7;"
                    cur.execute(sql)
                    my_print("You killed the python!")
                    #avataan poispääsy ruudusta 7
                    cur = db.cursor()
                    sql = "UPDATE Movement SET Locked=0 WHERE MovementId='F7F6'"
                    cur.execute(sql)

                else:
                    my_print("There's nothing you can do with it.")
                
        else:
            my_print("You don't have a machete!")
            die()

#python w empty inv
def none(destination):
    cur = db.cursor()
    sql = "SELECT ItemID FROM Item WHERE PlayerID=1;"
    cur.execute(sql)
    if cur.rowcount ==0:
        move_look(destination)
        print("You don't have any weapons!")
        die()

#location 7, use rope
def python_rope():
    #testataan onko rope
    cur = db.cursor()
    sql = "SELECT PlayerId FROM Item WHERE ITEMID=8;"
    cur.execute(sql)
    for row in cur.fetchall():
        #jos on, pelaaja kuolee
        if row[0]==1:
            my_print("You try to strangle the python with the rope. Suddenly the python strangles you!")
            die()
        else:
            my_print("You don't have a rope!")
    return

#location 7, use gun
def python_gun():
    #testataan onko rope
    cur = db.cursor()
    sql = "SELECT PlayerId FROM Item WHERE ITEMID=1;"
    cur.execute(sql)
    for row in cur.fetchall():
        #jos on, pelaaja kuolee
        if row[0]==1:
            my_print("You missed the shot. Suddenly the python strangles you!")
            die()
        else:
            my_print("You don't have a gun! Hurry!")
    return

#kill deer w gun, loc 14
def deer_gun():
    cur = db.cursor()
    sql = "SELECT PlayerId FROM Item WHERE ITEMID=1;"
    cur.execute(sql)
    if cur.rowcount > 0: #check if plauer has gun        
        sql = "SELECT PlayerId FROM Item WHERE ITEMID=3 AND PlayerId = 1 OR ITEMID=4 AND PlayerId = 1;"
        cur.execute(sql)
        if cur.rowcount > 0: #check if player has bullets
            sql = "SELECT Health FROM NPC WHERE NPCID=2 AND Health = 1;"
            cur.execute(sql)
            if cur.rowcount > 0: #check if the deer is alive
                sql = "UPDATE NPC SET Health=0 WHERE NPCID=2" #mark deer as dead
                cur.execute(sql)
                sql = "SELECT Name FROM Item WHERE ItemID = 3"
                cur.execute(sql)
                if cur.rowcount > 0:
                    sql = "UPDATE Item SET PlayerId=NULL WHERE ItemID = 3"
                    cur.execute(sql)
                else:
                    sql = "SELECT Name FROM Item WHERE ItemID = 4"
                    cur.execute(sql)
                    if cur.rowcount > 0:
                        sql = "UPDATE Item SET PlayerId=NULL WHERE ItemID = 4"
                        cur.execute(sql)    
                sql = "UPDATE Item SET PlayerID=1, LocationId = NULL WHERE ItemID=12" #loot antlers
                cur.execute(sql)
                my_print("You shot the deer and took its antlers!")
                #update description and name
                sql = "UPDATE Location SET Description=\"There's the deer you shot. It's starting to smell.\" WHERE LocationID=14;"
                cur.execute(sql)
                sql = "UPDATE Location SET Name=\"You are on a steep mountain path.\" WHERE LOCATIONId=14;"
                cur.execute(sql)
                
                # update chieftain
                sql = "UPDATE Location SET Name=\"Tribe chief is attacking! He spotted the holy antlers you have in your backpack!\" WHERE LocationID=19"
                cur.execute(sql)
                sql = "UPDATE Location SET Description=\"He's attacking you with a spear!\" WHERE LocationId=19"
                cur.execute(sql)
                sql = "UPDATE Movement SET Locked=1 WHERE MovementId='SqBe'"
                cur.execute(sql)
                sql = "UPDATE Movement SET Locked=1 WHERE MovementId='SqH1'"
                cur.execute(sql)
                sql = "UPDATE Movement SET Locked=1 WHERE MovementId='SqH2'"
                cur.execute(sql)
                sql = "UPDATE Movement SET Locked=1 WHERE MovementId='SqVi'"
                cur.execute(sql)
            else:
               my_print("The deer is already dead.")                  
        else:
           my_print("You don't have bullets.")
    else:
        my_print("You don't have a gun.")
    return

#kill bear with gun, loc 17
def bear_gun():
    cur = db.cursor()
    sql = "SELECT PlayerId FROM Item WHERE ITEMID=1;"
    cur.execute(sql)
    if cur.rowcount > 0: #check if player has gun        
        sql = "SELECT PlayerId FROM Item WHERE ITEMID=3 AND PlayerId = 1 OR ITEMID=4 AND PlayerId = 1;"
        cur.execute(sql)
        if cur.rowcount > 0: #check if player has bullets
            sql = "SELECT Health FROM NPC WHERE NPCID=3 AND Health = 1;"
            cur.execute(sql)
            if cur.rowcount > 0: #check if the bear is alive
                sql = "UPDATE NPC SET Health=0 WHERE NPCID=3" #mark bear as dead
                cur.execute(sql)
                sql = "SELECT Name FROM Item WHERE ItemID = 3"
                cur.execute(sql)
                if cur.rowcount > 0: #check how many bulltes left
                    sql = "UPDATE Item SET PlayerId=NULL WHERE ItemID = 3" #update bullets
                    cur.execute(sql)
                else:
                    sql = "SELECT Name FROM Item WHERE ItemID = 4"
                    cur.execute(sql)
                    if cur.rowcount > 0:
                        sql = "UPDATE Item SET PlayerId=NULL WHERE ItemID = 4"
                        cur.execute(sql)           
                sql = "UPDATE Item SET PlayerID=1 WHERE ItemID=13" #loot claws
                cur.execute(sql)
                my_print("You shot the bear and took it's claws!")
                #update location description and name
                sql = "UPDATE Location SET Description=\"The dead bear lies in a puddle of blood. Some bats are flying around.\" WHERE LocationID=17;"
                cur.execute(sql)
                sql = "UPDATE Location SET Name=\"You are in the cave.\" WHERE LocationID=17;"
                cur.execute(sql)
                sql = "UPDATE Movement SET Locked=0 WHERE MovementId='CaVi'"
                cur.execute(sql)
                sql = "UPDATE Movement SET Locked=0 WHERE MovementId='CaCe'"
                cur.execute(sql)
            else:
               my_print("The bear is already dead.") 
        else:
            my_print("You don't have bullets.")
    else:
        my_print("You don't have a gun.")
    return  








#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

##chief battle, loc 19
#def angry():
#    # update desc and name
#    cur = db.cursor()
#    sql = "UPDATE Location SET Name=\"Tribe chief is attacking!\" WHERE LocationID=19"
#    cur.execute(sql)
#    sql = "UPDATE Location SET Desc=\"He\'s attacking you with a spear!\" WHERE LocationId=19"
#    cur.execute(sql)
#    sql = "UPDATE Movement SET Locked=1 WHERE MovementId='SqBe'"
#    cur.execute(sql)
#    sql = "UPDATE Movement SET Locked=1 WHERE MovementId='SqH1'"
#    cur.execute(sql)
#    sql = "UPDATE Movement SET Locked=1 WHERE MovementId='SqH2'"
#    cur.execute(sql)
#    sql = "UPDATE Movement SET Locked=1 WHERE MovementId='SqVi'"
#    cur.execute(sql)
#    # movement lock
    
            
#cief battle, loc 19
def chief_fistfight():
    #onko machete
    cur = db.cursor()
    sql = "SELECT Name FROM Npc WHERE NpcId = 4 AND Health = 1;"
    cur.execute(sql)
    if cur.rowcount > 0:        
        sql = "UPDATE NPC SET Health=0 WHERE NPCID=4;"
        cur.execute(sql)
        #desc & name
        sql = "UPDATE Location SET Description=\"There is a hut to the west and one to the east. To the south you can see a small beach.\" WHERE LocationID=19;"
        cur.execute(sql)
        sql = "UPDATE Location SET Name=\"The village square.\" WHERE LocationID=19;"
        cur.execute(sql)
        sql = "UPDATE Movement SET Locked=0 WHERE MovementId='SqBe'"
        cur.execute(sql)
        sql = "UPDATE Movement SET Locked=0 WHERE MovementId='SqH1'"
        cur.execute(sql)
        sql = "UPDATE Movement SET Locked=0 WHERE MovementId='SqH2'"
        cur.execute(sql)
        sql = "UPDATE Movement SET Locked=0 WHERE MovementId='SqVi'"
        cur.execute(sql)
        my_print("You were badly hurt in the fistfight, but the Chieftain is now down. You need to hurry before he wakes up!")
    else:
        my_print("There's nothing to hit to!")

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
















#swim
def swim():
    my_print("You swim away from the island, but a shark bit you and you died. Sad.")
    die()
    sys.exit()

def initialize(loc):
    # Clear console and print lost
    print("\n"*100)
    print_slow(" **********************************************************")
    print_slow(" *                                                        *")
    print_slow(" *                                                        *")
    print_slow(" *     **           ****      **********  ***********     *")
    print_slow(" *     **         ********    **********  ***********     *")
    print_slow(" *     **        **      **   **              ***         *")
    print_slow(" *     **       **        **  **********      ***         *")
    print_slow(" *     **       **        **  **********      ***         *")
    print_slow(" *     **        **      **           **      ***         *")
    print_slow(" *     ********   ********    **********      ***         *")
    print_slow(" *     ********     ****      **********      ***         *")
    print_slow(" *                                                        *")
    print_slow(" *                                                        *")
    print_slow(" **********************************************************")
    print("\n"*2)
    print_slow("                   --- initializing ---                   ")
    print_load("|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
    print("\n"*3)
    move_look(loc)

#build raft
def build():
    #haetaan wood(5&6), rope & sail playerId arvot (NULL/1)
    cur = db.cursor()
    sql = ("SELECT PlayerId FROM Item  WHERE ItemId=5 AND PlayerId = 1 OR ItemId=6 AND PlayerId = 1 OR ItemId=8 AND PlayerId = 1 OR ItemId=11 AND PlayerId = 1;")
    cur.execute(sql)    
    if cur.rowcount > 3:
        print("\n")
        print_slow(":::   :::  ::::::::  :::    :::     :::       :::  ::::::::  ::::    ::: ")
        print_slow(":+:   :+: :+:    :+: :+:    :+:     :+:       :+: :+:    :+: :+:+:   :+: ")
        print_slow(" +:+ +:+  +:+    +:+ +:+    +:+     +:+       +:+ +:+    +:+ :+:+:+  +:+ ")
        print_slow("  +#++:   +#+    +:+ +#+    +:+     +#+  +:+  +#+ +#+    +:+ +#+ +:+ +#+ ")
        print_slow("   +#+    +#+    +#+ +#+    +#+     +#+ +#+#+ +#+ +#+    +#+ +#+  +#+#+# ")
        print_slow("   #+#    #+#    #+# #+#    #+#      #+#+# #+#+#  #+#    #+# #+#   #+#+# ")
        print_slow("   ###     ########   ########        ###   ###    ########  ###    #### ")
        print("\n"*3)
        my_print("Press ENTER to quit the game.")
        input()
        exit()
    else:
        my_print("You don't have enough material to build a raft!")

#die
def die():
    print("\n")
    my_print_end(" ***************************************************************")
    my_print_end(" *                                                             *")
    my_print_end(" *                                                             *")
    my_print_end(" *      ******         ****       ***       ***  ********      *")
    my_print_end(" *     **             **  **      ** **  **  **  **            *")
    my_print_end(" *     **            **    **     **  ****   **  ********      *")
    my_print_end(" *     **  ****     ** **** **    **         **  ********      *")
    my_print_end(" *     **    **    **        **   **         **  **            *")
    my_print_end(" *      ******    **          **  **         **  ********      *")
    my_print_end(" *                                                             *")
    my_print_end(" *         ******   **         **  ********  ******            *")
    my_print_end(" *        **    **   **       **   **        **    **          *")
    my_print_end(" *        **    **    **     **    ********  ********          *")
    my_print_end(" *        **    **     **   **     ********  ****              *")
    my_print_end(" *        **    **      ** **      **        **  **            *")
    my_print_end(" *         ******        ***       ********  **    **          *")
    my_print_end(" *                                                             *")
    my_print_end(" *                                                             *")     
    my_print_end(" ***************************************************************")
    print("\n"*3)
    my_print("Press ENTER to quit the game.")
    input()
    exit()
#exit
def exit():
    sys.exit()

#-------------------------------------------
#slow print 1
def print_slow(s):
  for c in s + '\n':
    sys.stdout.write(c)
    sys.stdout.flush()
    time.sleep(1./150)
    
#slow print 2
def print_load(s):
  for c in s + '\n':
    sys.stdout.write(c)
    sys.stdout.flush()
    time.sleep(1./15)
    
#slow print 3
def my_print(s):
  for c in s + '\n':
    sys.stdout.write(c)
    sys.stdout.flush()
    time.sleep(1./45)
    
#slow print 4
def my_print_end(s):
  for c in s + '\n':
    sys.stdout.write(c)
    sys.stdout.flush()
    time.sleep(1./300)
    
# print limiter
def my_print_limit(mjono):
    rivin_pituus = 80
    lista = mjono.split()
    kaytetty = 0
    for sana in lista:
        if kaytetty + len(sana) <= rivin_pituus:
            if kaytetty>0:
                my_print(" ",end='')
                kaytetty = kaytetty+1
            my_print(sana, end='')
        else:
            print("")
            kaytetty = 0
            my_print(sana, end='')
        kaytetty = kaytetty + len(sana)
    print("")

# Open DB connection
db = mysql.connector.Connect(host="localhost",
                             user="root",
                             passwd="Metropolia2018",
                             db="Lostbase",
                             buffered=True)

#Initialize player location and format action
loc = 1
action = ""
initialize(loc)

# Main loop
while action!="systemerror" and loc!="EXIT":

    print("")
    input_string=input("Your action? ").split()
    if len(input_string)>=1:
        action = input_string[0].lower()
    else:
        action = ""
    if len(input_string)>=2:
        target = input_string[len(input_string)-1].lower()
    else:
        target = ""
    print("")

    # take one item
    if (action=="get" or action=="take") and target!="":
        take(target, loc, action)

    # drop
    elif action=="drop" and target!="":
        success = drop(target, loc)

    # look
    elif (action=="look" or action=="view"):
        if target=="":
            look(loc)
            
    #show objects
    elif(action=="show" or action=="show objects"):
        show_objects(loc)
    
    # inventory
    elif action=="inventory" or action=="i":
        inventory()
        
    # ignite
    elif(action=="ignite" or action=="light"):
        ignite()

    # take
    elif(action=="take all" or action=="loot"):
        take_all(loc)

    # inpect inventory item
    elif action=="inspect" or action=="examine":
        if target=="":
            my_print("I don't know what to " + str(action) +".")
        else:
            inspect(target)

    #help
    elif action=="help":
        my_print("Here's some useful commands:\n- Inventory\n- Look\n- Loot\n- Inspect\n- Build\n- Ignite\n- Poop\n- Hit\n- Swim\n- Light\n- Open\- Show\n- Use\n- Kill\n- S\n- E\n- W\n- N\n- Shoot")
    
    # swim
    elif action=="swim":
        if (loc==1 or loc==2 or loc==3 or loc==23):
            swim()
        else:
            my_print("I can't swim here.")
        
    # use
    elif action=="use":
        if target=="":
            print("I don't know what to use.")

        #location 7, python battle
        elif loc==7 and target=="machete":
            machete();
        elif loc==7 and target=="rope":
            python_rope();
        elif loc==7 and target=="gun":
            python_gun()
        #location 14 deer
        elif loc==14 and target=="gun":
            deer_gun();
        elif loc==17 and target=="gun":
            bear_gun();
        
        else:
            my_print("You can't do that.")

    #location 19, chief
    elif loc==19 and action=="hit":
        chief_fistfight()
        
    #kill 
    elif action=="kill":
        if target=="":
            my_print("How can I do that?")
            
        elif (target=="deer" or target=="python" or target=="bear"):
            my_print("I wonder which weapon should I use...")
        
    #shoot
    elif action=="shoot":
        if target=="":
            my_print("I don't know what to shoot")

        elif target=="deer" and loc==14:
            deer_gun()
        
        else:
            my_print("No.")

    #build raft
    elif action=="build":
        if target=="":
            my_print("I don't know what to build.")

        elif loc==23 and (target=="raft" or target=="boat"):
            build()
     
    #usekey
    elif(action == "use key" or action == "usekey" or action == "open"):
        usekey(loc)
 
    # move
    elif action=="n" or action=="e" or action=="s" or action=="w" or action=="north" or action=="east" or action=="south" or action=="west" or action=="u" or action=="up" or action=="d" or action=="down":
        newloc = move(loc,action)
        if loc==newloc:
            my_print("You can't move to that direction.");
        else:
            loc = newloc
                
            move_look(loc)

    
    # easter eggs!!!**********
    elif action == "poop" or action == "poo" and loc == 22:
        my_print("Feels good man.")
     
    # quit game
    elif action == "quit" or action == "suicide":
        die()
        
    elif action!="quit" and action!="":
        my_print("I don't know how to " + action)

if (loc=="EXIT"):
    print("Well done!")
else:
    print("Bye!")
db.rollback()

db.close()