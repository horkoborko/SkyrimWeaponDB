import sqlite3

# Welcome to the Skyrim Weapon Database!
# The purpose of this database is to store, insert, delete, and update
# the weaponry from Skyrim (2011).
# I started this project right around the time when I was bitten by
# the Skyrim bug, adding hundreds of mods to the game and playing
# for hours on end. It was a great source of inspiration for this
# database. I kept everything as true to the gameplay as possible, with
# minor exceptions for the sake of SQL simplicity.
# SOME NOTES:
#	- The data creation for materials is specified by types. This is intentional
#	  as material uniquely defines the weight, damage, and value (and speed)
#	  for each weapon type without any recognizeable pattern. Thus, material
#	  must be created for each type.
#	- The LOC for this file is less than 1000 LOC, the reason being is that
#	  the majority of the code is reused with functions in order to improve
#	  readability, reduce code repition, and process all of the data easier.
#	  I have satisfied all of the requirements and have tried my best to reach
#	  1000 LOC with comment documentation and various deletion, insertion,
#	  modification, and query functions.

# HOW TO RUN:
#	Simply open your command line shell, navigate to the directory that this
#	file is located in, and run "python3 SQL.py".
#	This will produce output within the shell as well as the creation of
#	a new file, called SkyrimWeaponsDB.db
# 	=======================================================================
#	IN ORDER TO RUN AGAIN, THE DATABASE FILE MUST BE DELETED,
#	AS TRYING TO RUN THE PYTHON SCRIPT AGAIN WILL CAUSE AN UNIQUE ID ERROR.
#	THIS IS A KNOWN BUG
#	=======================================================================

# Creating the database and establishing the cursor
connect = sqlite3.connect("SkyrimWeaponsDB.db")
c = connect.cursor()

# TABLE CREATION

# The "Weapon" table is the 'main' table of the database.
# ID is the primary key of this database because in Skyrim,
# IDs are used as the unique identifiers for every object in
# the game.
# Beyond an ID, each weapon consists of a type and a material.
# These aspects are made into their own separate tables, as seen below.
# ======================================================
# THIS TABLE SATISFIES:
#     1. Total participation constraint
#		An ID cannot exist without a weapon and a weapon
#		cannot exist without an ID.
#     2. Foreign key
#		Both Type and Material are foreign keys.
#     3. Non-M:N cardinality restraint
#		The relation of Weapon to Type and Material is 1:N,
#		Since there can only be one Type/Material to a weapon,
#		But the options are more than one.
#	  4. First relation type (weapon HAS type AND material)
c.execute('''CREATE TABLE IF NOT EXISTS "Weapon" (
	"ID"	TEXT NOT NULL UNIQUE,
	"Name"  TEXT NOT NULL,
	"Type"	TEXT NOT NULL,
	"Material"	TEXT NOT NULL,
	PRIMARY KEY("ID"),
	FOREIGN KEY("Type") REFERENCES "Type"("Name"),
	FOREIGN KEY("Material") REFERENCES "Material"("Name")
	);''')

# The "Type" table defines what the weapon is (sword, battleaxe, etc),
# Its handedness (one-handed, two-handed, archery),
# and the values inherent to type
# NOTE: Melee and archery handedness are defined by different variables
# i.e. melee --> speed, stagger, reach
#      archery -->  stagger
# Hence, only "Name" and "Stagger" are NOT NULL
# ======================================================
# THIS TABLE SATISFIES:
#     1. First entity type
c.execute('''CREATE TABLE IF NOT EXISTS "Type" (
	"Name"	TEXT NOT NULL,
	"Speed"	INTEGER,
	"Stagger"	INTEGER NOT NULL,
	"Reach"	INTEGER
	);''')

# The "Material" table defines the material the weapon is made out of
# and the values that modify each weapon, including its type.
# NOTE: Archery adds "Speed" as a material modifier on top of "Weight",
# "Damage", and "Value".
# This "Speed" value is DIFFERENT to the type table's "Speed"
# ======================================================
# THIS TABLE SATISFIES:
#     1. Second entity type
c.execute('''CREATE TABLE IF NOT EXISTS "Material" (
	"Name"	TEXT NOT NULL,
	"Weight"	REAL NOT NULL,
	"Damage"	INTEGER NOT NULL,
	"Value"	INTEGER NOT NULL,
	"Speed"	REAL,
	"Forgeability"	TEXT,
	FOREIGN KEY("Forgeability") REFERENCES "Forgeability"("Perk Name")
	);''')

# The "Forgeability" table defines the perk required to create and temper
# weapons by material in the game. The availability of this perk is based
# on the character's level.
# ======================================================
# THIS TABLE SATISFIES:
#     1. Composite attribute
#		The value of "Forgeability" in "Material" consists of two different
#		types of values, "Level" and "Perk Name"
c.execute('''CREATE TABLE IF NOT EXISTS "Forgeability" (
	"Level"	INTEGER,
	"Perk_Name"	TEXT
	);''')

# The "Enchanting" table defines the types of enchants available
# for each weapon and its type.
# ======================================================
# THIS TABLE SATISFIES:
#     1. Multivalued attribute
#		Multiple similar enchantment values are available to weapons
#		as an attribute.
c.execute('''CREATE TABLE IF NOT EXISTS "Enchanting" (
	"Name"	TEXT,
	"Effect"	TEXT,
	"Weapon"	TEXT
	);''')

# The "Enchanted With" table defines the relationship between a weapon
# and an enchantment, using the ID and enchantment name.
# ======================================================
# THIS TABLE SATISFIES:
#     1. Second relation type (weapon CAN BE enchanted)
c.execute('''CREATE TABLE IF NOT EXISTS "EnchantedWith" (
	"ID"	TEXT,
	"EnchantmentName"	TEXT,
	FOREIGN KEY("ID") REFERENCES "Weapon"("ID")
	FOREIGN KEY("EnchantmentName") REFERENCES "Enchanting"("Name")
	);''')

# DATA CREATION METHODS
def createWeapon(connect, weapon):
	SQL = '''INSERT INTO Weapon(ID, Name, Type, Material)
			 VALUES(?, ?, ?, ?)'''
	cursor = connect.cursor()
	cursor.execute(SQL, weapon)
	connect.commit()
	return cursor.lastrowid
def createType(connect, type):
	SQL = '''INSERT INTO Type(Name, Speed, Stagger, Reach)
			 VALUES(?, ?, ?, ?)'''
	cursor = connect.cursor()
	cursor.execute(SQL, type)
	connect.commit()
	return cursor.lastrowid
def createMaterial(connect, material):
	SQL = '''INSERT INTO Material(Name, Weight, Damage, Value, Speed, Forgeability)
			 VALUES(?, ?, ?, ?, ?, ?)'''
	cursor = connect.cursor()
	cursor.execute(SQL, material)
	connect.commit()
	return cursor.lastrowid
def createForgeability(connect, forgeability):
	SQL = '''INSERT INTO Forgeability(Level, Perk_Name)
			 VALUES(?, ?)'''
	cursor = connect.cursor()
	cursor.execute(SQL, forgeability)
	connect.commit()
	return cursor.lastrowid
def createEnchanting(connect, enchanting):
	SQL = '''INSERT INTO Enchanting(Name, Effect, Weapon)
			 VALUES(?, ?, ?)'''
	cursor = connect.cursor()
	cursor.execute(SQL, enchanting)
	connect.commit()
	return cursor.lastrowid
def createEnchantedWith(connect, enchantedwith):
	SQL = '''INSERT INTO EnchantedWith(ID, EnchantmentName)
			 VALUES(?, ?)'''
	cursor = connect.cursor()
	cursor.execute(SQL, enchantedwith)
	connect.commit()
	return cursor.lastrowid

# DATA CREATION
# TYPES
type_onehand_sword = ("One-Handed Sword", 1, 0.75, 1)
createType(connect, type_onehand_sword)
type_onehand_axe = ("One-Handed Axe", 0.9, 0.85, 1)
createType(connect, type_onehand_axe)
type_onehand_mace = ("One-Handed Mace", 0.8, 1, 1)
createType(connect, type_onehand_mace)
type_onehand_dagger = ("One-Handed Dagger", 1.3, 0, 0.7)
createType(connect, type_onehand_dagger)
# ===Update Speed to 0.75===========================================================================
type_twohand_sword = ("Two-Handed Sword", 0.7, 1.1, 1.3)
createType(connect, type_twohand_sword)
# ==================================================================================================
type_twohand_axe = ("Two-Handed Axe", 0.7, 1.15, 1.3)
createType(connect, type_twohand_axe)
type_twohand_mace = ("Two-Handed Mace", 0.6, 1.25, 1.3)
createType(connect, type_twohand_mace)
type_bow = ("Bow", None, 0, None)
createType(connect, type_bow)
# MATERIALS
# Iron
material_iron_onehand_sword = ("Iron", 9, 7, 25, None, None)
createMaterial(connect, material_iron_onehand_sword)
material_iron_onehand_axe = ("Iron", 11, 8, 30, None, None)
createMaterial(connect, material_iron_onehand_axe)
material_iron_onehand_mace = ("Iron", 13, 9, 35, None, None)
createMaterial(connect, material_iron_onehand_mace)
material_iron_onehand_dagger = ("Iron", 2, 4, 10, None, None)
createMaterial(connect, material_iron_onehand_dagger)
material_iron_twohand_sword = ("Iron", 16, 15, 50, None, None)
createMaterial(connect, material_iron_twohand_sword)
material_iron_twohand_axe = ("Iron", 20, 16, 55, None, None)
createMaterial(connect, material_iron_twohand_axe)
material_iron_twohand_mace = ("Iron", 24, 18, 60, None, None)
createMaterial(connect, material_iron_twohand_mace)
# Steel
material_steel_onehand_sword = ("Steel", 10, 8, 45, None, "Steel Smithing")
createMaterial(connect, material_steel_onehand_sword)
material_steel_onehand_axe = ("Steel", 12, 9, 55, None, "Steel Smithing")
createMaterial(connect, material_steel_onehand_axe)
material_steel_onehand_mace = ("Steel", 14, 10, 65, None, "Steel Smithing")
createMaterial(connect, material_steel_onehand_mace)
material_steel_onehand_dagger = ("Steel", 2, 4, 10, None, "Steel Smithing")
createMaterial(connect, material_steel_onehand_dagger)
material_steel_twohand_sword = ("Steel", 17, 17, 90, None, "Steel Smithing")
createMaterial(connect, material_steel_twohand_sword)
material_steel_twohand_axe = ("Steel", 21, 18, 100, None, "Steel Smithing")
createMaterial(connect, material_steel_twohand_axe)
material_steel_twohand_mace = ("Steel", 25, 20, 110, None, "Steel Smithing")
createMaterial(connect, material_steel_twohand_mace)
# Orcish
material_orcish_onehand_sword = ("Orcish", 11, 9, 75, None, "Orcish Smithing")
createMaterial(connect, material_orcish_onehand_sword)
material_orcish_onehand_axe = ("Orcish", 13, 10, 90, None, "Orcish Smithing")
createMaterial(connect, material_orcish_onehand_axe)
material_orcish_onehand_mace = ("Orcish", 15, 11, 105, None, "Orcish Smithing")
createMaterial(connect, material_orcish_onehand_mace)
material_orcish_onehand_dagger = ("Orcish", 3, 6, 30, None, "Orcish Smithing")
createMaterial(connect, material_orcish_onehand_dagger)
material_orcish_twohand_sword = ("Orcish", 18, 18, 75, None, "Orcish Smithing")
createMaterial(connect, material_orcish_twohand_sword)
material_orcish_twohand_axe = ("Orcish", 25, 19, 165, None, "Orcish Smithing")
createMaterial(connect, material_orcish_twohand_axe)
material_orcish_twohand_mace = ("Orcish", 26, 21, 180, None, "Orcish Smithing")
createMaterial(connect, material_orcish_twohand_mace)
material_orcish_bow = ("Orcish", 9, 10, 150, 0.8125, "Orcish Smithing")
createMaterial(connect, material_orcish_bow)
# Dwarven
material_dwarven_onehand_sword = ("Dwarven", 12, 10, 150, None, "Dwarven Smithing")
createMaterial(connect, material_dwarven_onehand_sword)
material_dwarven_onehand_axe = ("Dwarven", 14, 11, 165, None, "Dwarven Smithing")
createMaterial(connect, material_dwarven_onehand_axe)
material_dwarven_onehand_mace = ("Dwarven", 16, 12, 190, None, "Dwarven Smithing")
createMaterial(connect, material_dwarven_onehand_mace)
material_dwarven_onehand_dagger = ("Dwarven", 3.5, 7, 55, None, "Dwarven Smithing")
createMaterial(connect, material_dwarven_onehand_dagger)
material_dwarven_twohand_sword = ("Dwarven", 19, 19, 270, None, "Dwarven Smithing")
createMaterial(connect, material_dwarven_twohand_sword)
material_dwarven_twohand_axe = ("Dwarven", 23, 20, 300, None, "Dwarven Smithing")
createMaterial(connect, material_dwarven_twohand_axe)
material_dwarven_twohand_mace = ("Dwarven", 27, 22, 325, None, "Dwarven Smithing")
createMaterial(connect, material_dwarven_twohand_mace)
material_dwarven_bow =  ("Dwarven", 10, 12, 270, 0.75, "Dwarven Smithing")
createMaterial(connect, material_dwarven_bow)
# Elven
material_elven_onehand_sword = ("Elven", 13, 11, 235, None, "Elven Smithing")
createMaterial(connect, material_elven_onehand_sword)
material_elven_onehand_axe = ("Elven", 15, 12, 280, None, "Elven Smithing")
createMaterial(connect, material_elven_onehand_axe)
material_elven_onehand_mace = ("Elven", 17, 13, 330, None, "Elven Smithing")
createMaterial(connect, material_elven_onehand_mace)
material_elven_onehand_dagger = ("Elven", 4, 8, 95, None, "Elven Smithing")
createMaterial(connect, material_elven_onehand_dagger)
material_elven_twohand_sword = ("Elven", 20, 20, 470, None, "Elven Smithing")
createMaterial(connect, material_elven_twohand_sword)
material_elven_twohand_axe = ("Elven", 24, 21, 520, None, "Elven Smithing")
createMaterial(connect, material_elven_twohand_axe)
material_elven_twohand_mace = ("Elven", 28, 23, 565, None, "Elven Smithing")
createMaterial(connect, material_elven_twohand_mace)
material_elven_bow = ("Elven", 12, 13, 470, 0.6875, "Elven Smithing")
createMaterial(connect, material_elven_bow)
# Glass
material_glass_onehand_sword = ("Glass", 14, 12, 410, None, "Glass Smithing")
createMaterial(connect, material_glass_onehand_sword)
material_glass_onehand_axe = ("Glass", 16, 13, 490, None, "Glass Smithing")
createMaterial(connect, material_glass_onehand_axe)
material_glass_onehand_mace = ("Glass", 18, 14, 575, None, "Glass Smithing")
createMaterial(connect, material_glass_onehand_mace)
material_glass_onehand_dagger = ("Glass", 4.5, 9, 165, None, "Glass Smithing")
createMaterial(connect, material_glass_onehand_dagger)
material_glass_twohand_sword = ("Glass", 22, 21, 820, None, "Glass Smithing")
createMaterial(connect, material_glass_twohand_sword)
material_glass_twohand_axe = ("Glass", 25, 22, 900, None, "Glass Smithing")
createMaterial(connect, material_glass_twohand_axe)
material_glass_twohand_mace = ("Glass", 29, 24, 985, None, "Glass Smithing")
createMaterial(connect, material_glass_twohand_mace)
material_glass_bow = ("Glass", 14, 15, 820, 0.625, "Glass Smithing")
createMaterial(connect, material_glass_bow)
# Ebony
material_ebony_onehand_sword = ("Ebony", 15, 13, 720, None, "Ebony Smithing")
createMaterial(connect, material_ebony_onehand_sword)
# ===Update Damage to 14============================================================================
material_ebony_onehand_axe = ("Ebony", 17, 15, 865, None, "Ebony Smithing")
createMaterial(connect, material_ebony_onehand_axe)
# ==================================================================================================
# ===Update Damage to 15============================================================================
material_ebony_onehand_mace = ("Ebony", 19, 16, 1000, None, "Ebony Smithing")
createMaterial(connect, material_ebony_onehand_mace)
# ==================================================================================================
material_ebony_onehand_dagger = ("Ebony", 5, 10, 290, None, "Ebony Smithing")
createMaterial(connect, material_ebony_onehand_dagger)
material_ebony_twohand_sword = ("Ebony", 22, 22, 1440, None, "Ebony Smithing")
createMaterial(connect, material_ebony_twohand_sword)
material_ebony_twohand_axe = ("Ebony", 26, 23, 1585, None, "Ebony Smithing")
createMaterial(connect, material_ebony_twohand_axe)
material_ebony_twohand_mace = ("Ebony", 30, 25, 1725, None, "Ebony Smithing")
createMaterial(connect, material_ebony_twohand_mace)
material_ebony_bow = ("Ebony", 16, 17, 1800, 0.5625, "Ebony Smithing")
createMaterial(connect, material_ebony_bow)
# Daedric
material_daedric_onehand_sword = ("Daedric", 16, 14, 1250, None, "Daedric Smithing")
createMaterial(connect, material_daedric_onehand_sword)
material_daedric_onehand_axe = ("Daedric", 18, 15, 1500, None, "Daedric Smithing")
createMaterial(connect, material_daedric_onehand_axe)
material_daedric_onehand_mace = ("Daedric", 20, 16, 1750, None, "Daedric Smithing")
createMaterial(connect, material_daedric_onehand_mace)
material_daedric_onehand_dagger = ("Daedric", 6, 11, 500, None, "Daedric Smithing")
createMaterial(connect, material_daedric_onehand_dagger)
material_daedric_twohand_sword = ("Daedric", 23, 24, 2500, None, "Daedric Smithing")
createMaterial(connect, material_daedric_twohand_sword)
material_daedric_twohand_axe = ("Daedric", 27, 25, 2750, None, "Daedric Smithing")
createMaterial(connect, material_daedric_twohand_axe)
material_daedric_twohand_mace = ("Daedric", 31, 27, 4000, None, "Daedric Smithing")
createMaterial(connect, material_daedric_twohand_mace)
material_daedric_bow = ("Daedric", 18, 19, 2500, 0.5, "Daedric Smithing")
createMaterial(connect, material_daedric_bow)
# Miscenalleous Archery-Special Materials
material_long_bow = ("Long", 5, 6, 30, 1, None)
createMaterial(connect, material_long_bow)
material_hunting_bow = ("Hunting", 7, 7, 50, 0.9375, None)
createMaterial(connect, material_hunting_bow)

# WEAPONS
# Iron Melee
weapon_iron_onehand_sword = ("00012eb7", "Iron Sword", "One-Handed Sword", "Iron")
createWeapon(connect, weapon_iron_onehand_sword)
weapon_iron_onehand_axe = ("00013790", "Iron War Axe", "One-Handed Axe", "Iron")
createWeapon(connect, weapon_iron_onehand_axe)
weapon_iron_onehand_mace = ("00013982", "Iron Mace", "One-Handed Mace", "Iron")
createWeapon(connect, weapon_iron_onehand_mace)
weapon_iron_onehand_dagger = ("0001397e", "Iron Dagger", "One-Handed Dagger", "Iron")
createWeapon(connect, weapon_iron_onehand_dagger)
weapon_iron_twohand_sword = ("0001359d", "Iron Greatsword", "Two-Handed Sword", "Iron")
createWeapon(connect, weapon_iron_twohand_sword)
weapon_iron_twohand_axe = ("00013980", "Iron Battleaxe", "Two-Handed Axe", "Iron")
createWeapon(connect, weapon_iron_twohand_axe)
weapon_iron_twohand_mace = ("00013981", "Iron Warhammer", "Two-Handed Mace", "Iron")
createWeapon(connect, weapon_iron_twohand_mace)
# Steel Melee
weapon_steel_onehand_sword = ("00013989", "Steel Sword", "One-Handed Sword", "Steel")
createWeapon(connect, weapon_steel_onehand_sword)
weapon_steel_onehand_axe = ("00013983", "Steel War Axe", "One-Handed Axe", "Steel")
createWeapon(connect, weapon_steel_onehand_axe)
weapon_steel_onehand_mace = ("00013988", "Steel Mace", "One-Handed Mace", "Steel")
createWeapon(connect, weapon_steel_onehand_mace)
weapon_steel_onehand_dagger = ("00013986", "Steel Dagger", "One-Handed Dagger", "Steel")
createWeapon(connect, weapon_steel_onehand_dagger)
weapon_steel_twohand_sword = ("00013987", "Steel Greatsword", "Two-Handed Sword", "Steel")
createWeapon(connect, weapon_steel_twohand_sword)
weapon_steel_twohand_axe = ("00013984", "Steel Battleaxe", "Two-Handed Axe", "Steel")
createWeapon(connect, weapon_steel_twohand_axe)
weapon_steel_twohand_mace = ("0001398a", "Steel Warhammer", "Two-Handed Mace", "Steel")
createWeapon(connect, weapon_steel_twohand_mace)
# Orcish Melee
weapon_orcish_onehand_sword = ("00013991", "Orcish Sword", "One-Handed Sword", "Orcish")
createWeapon(connect, weapon_orcish_onehand_sword)
weapon_orcish_onehand_axe = ("0001398b", "Orcish War Axe", "One-Handed Axe", "Orcish")
createWeapon(connect, weapon_orcish_onehand_axe)
weapon_orcish_onehand_mace = ("00013990", "Orcish Mace", "One-Handed Mace", "Orcish")
createWeapon(connect, weapon_orcish_onehand_mace)
weapon_orcish_onehand_dagger = ("0001398e", "Orcish Dagger", "One-Handed Dagger", "Orcish")
createWeapon(connect, weapon_orcish_onehand_dagger)
weapon_orcish_twohand_sword = ("0001398f", "Orcish Greatsword", "Two-Handed Sword", "Orcish")
createWeapon(connect, weapon_orcish_twohand_sword)
weapon_orcish_twohand_axe = ("0001398c", "Orcish Battleaxe", "Two-Handed Axe", "Orcish")
createWeapon(connect, weapon_orcish_twohand_axe)
weapon_orcish_twohand_mace = ("00013992", "Orcish Warhammer", "Two-Handed Mace", "Orcish")
createWeapon(connect, weapon_orcish_twohand_mace)
# Dwarven Melee
weapon_dwarven_onehand_sword = ("00013999", "Dwarven Sword", "One-Handed Sword", "Dwarven")
createWeapon(connect, weapon_dwarven_onehand_sword)
weapon_dwarven_onehand_axe = ("00013993", "Dwarven War Axe", "One-Handed Axe", "Dwarven")
createWeapon(connect, weapon_dwarven_onehand_axe)
weapon_dwarven_onehand_mace = ("00013998", "Dwarven Mace", "One-Handed Mace", "Dwarven")
createWeapon(connect, weapon_dwarven_onehand_mace)
weapon_dwarven_onehand_dagger = ("00013996", "Dwarven Dagger", "One-Handed Dagger", "Dwarven")
createWeapon(connect, weapon_dwarven_onehand_dagger)
weapon_dwarven_twohand_sword = ("00013997", "Dwarven Greatsword", "Two-Handed Sword", "Dwarven")
createWeapon(connect, weapon_dwarven_twohand_sword)
weapon_dwarven_twohand_axe = ("00013994", "Dwarven Battleaxe", "Two-Handed Axe", "Dwarven")
createWeapon(connect, weapon_dwarven_twohand_axe)
weapon_dwarven_twohand_mace = ("0001399a", "Dwarven Warhammer", "Two-Handed Mace", "Dwarven")
createWeapon(connect, weapon_dwarven_twohand_mace)
# Elven Melee
weapon_elven_onehand_sword = ("000139a1", "Elven Sword", "One-Handed Sword", "Elven")
createWeapon(connect, weapon_elven_onehand_sword)
weapon_elven_onehand_axe = ("0001399b", "Elven War Axe", "One-Handed Axe", "Elven")
createWeapon(connect, weapon_elven_onehand_axe)
weapon_elven_onehand_mace = ("000139a0", "Elven Mace", "One-Handed Mace", "Elven")
createWeapon(connect, weapon_elven_onehand_mace)
weapon_elven_onehand_dagger = ("0001399e", "Elven Dagger", "One-Handed Dagger", "Elven")
createWeapon(connect, weapon_elven_onehand_dagger)
weapon_elven_twohand_sword = ("0001399f", "Elven Greatsword", "Two-Handed Sword", "Elven")
createWeapon(connect, weapon_elven_twohand_sword)
weapon_elven_twohand_axe = ("0001399c", "Elven Battleaxe", "Two-Handed Axe", "Elven")
createWeapon(connect, weapon_elven_twohand_axe)
weapon_elven_twohand_mace = ("000139a2", "Elven Warhammer", "Two-Handed Mace", "Elven")
createWeapon(connect, weapon_elven_twohand_mace)
# Glass Melee
weapon_glass_onehand_sword = ("000139a9", "Glass Sword", "One-Handed Sword", "Glass")
createWeapon(connect, weapon_glass_onehand_sword)
weapon_glass_onehand_axe = ("000139a3", "Glass War Axe", "One-Handed Axe", "Glass")
createWeapon(connect, weapon_glass_onehand_axe)
weapon_glass_onehand_mace = ("000139a8", "Glass Mace", "One-Handed Mace", "Glass")
createWeapon(connect, weapon_glass_onehand_mace)
weapon_glass_onehand_dagger = ("000139a6", "Glass Dagger", "One-Handed Dagger", "Glass")
createWeapon(connect, weapon_glass_onehand_dagger)
weapon_glass_twohand_sword = ("000139a7", "Glass Greatsword", "Two-Handed Sword", "Glass")
createWeapon(connect, weapon_glass_twohand_sword)
weapon_glass_twohand_axe = ("000139a4", "Glass Battleaxe", "Two-Handed Axe", "Glass")
createWeapon(connect, weapon_glass_twohand_axe)
weapon_glass_twohand_mace = ("000139aa", "Glass Warhammer", "Two-Handed Mace", "Glass")
createWeapon(connect, weapon_glass_twohand_mace)
# Ebony Melee
weapon_ebony_onehand_sword = ("000139b1", "Ebony Sword", "One-Handed Sword", "Ebony")
createWeapon(connect, weapon_ebony_onehand_sword)
weapon_ebony_onehand_axe = ("000139ab", "Ebony War Axe", "One-Handed Axe", "Ebony")
createWeapon(connect, weapon_ebony_onehand_axe)
weapon_ebony_onehand_mace = ("000139b0", "Ebony Mace", "One-Handed Mace", "Ebony")
createWeapon(connect, weapon_ebony_onehand_mace)
weapon_ebony_onehand_dagger = ("000139ae", "Ebony Dagger", "One-Handed Dagger", "Ebony")
createWeapon(connect, weapon_ebony_onehand_dagger)
weapon_ebony_twohand_sword = ("000139af", "Ebony Greatsword", "Two-Handed Sword", "Ebony")
createWeapon(connect, weapon_ebony_twohand_sword)
weapon_ebony_twohand_axe = ("000139ac", "Ebony Battleaxe", "Two-Handed Axe", "Ebony")
createWeapon(connect, weapon_ebony_twohand_axe)
weapon_ebony_twohand_mace = ("000139b2", "Ebony Warhammer", "Two-Handed Mace", "Ebony")
createWeapon(connect, weapon_ebony_twohand_mace)
# Daedric Melee
weapon_daedric_onehand_sword = ("000139b9", "Daedric Sword", "One-Handed Sword", "Daedric")
createWeapon(connect, weapon_daedric_onehand_sword)
weapon_daedric_onehand_axe = ("000139b3", "Daedric War Axe", "One-Handed Axe", "Daedric")
createWeapon(connect, weapon_daedric_onehand_axe)
weapon_daedric_onehand_mace = ("000139b8", "Daedric Mace", "One-Handed Axe", "Daedric")
createWeapon(connect, weapon_daedric_onehand_mace)
weapon_daedric_onehand_dagger = ("000139b6", "Daedric Dagger", "One-Handed Dagger", "Daedric")
createWeapon(connect, weapon_daedric_onehand_dagger)
weapon_daedric_twohand_sword = ("000139b7", "Daedric Greatsword", "Two-Handed Sword", "Daedric")
createWeapon(connect, weapon_daedric_twohand_sword)
weapon_daedric_twohand_axe = ("000139b4", "Daedric Battleaxe", "Two-Handed Axe", "Daedric")
createWeapon(connect, weapon_daedric_twohand_axe)
weapon_daedric_twohand_mace = ("000139ba", "Daedric Warhammer", "Two-Handed Mace", "Daedric")
createWeapon(connect, weapon_daedric_twohand_mace)
# Bows
weapon_long_bow = ("0003b562", "Long Bow", "Archery", "Long")
createWeapon(connect, weapon_long_bow)
weapon_hunting_bow = ("00013985", "Hunting Bow", "Archery", "Hunting")
createWeapon(connect, weapon_hunting_bow)
# ===Delete=========================================================================================
weapon_iron_bow = ("00000000", "Iron Bow", "Archery", "Iron")
createWeapon(connect, weapon_iron_bow)
weapon_steel_bow = ("01010101", "Steel Bow", "Archery", "Steel")
createWeapon(connect, weapon_steel_bow)
# ==================================================================================================
weapon_orcish_bow = ("0001398d", "Orcish Bow", "Archery", "Orcish")
createWeapon(connect, weapon_orcish_bow)
weapon_dwarven_bow = ("00013995", "Dwarven Bow", "Archery", "Dwarven")
createWeapon(connect, weapon_dwarven_bow)
weapon_elven_bow = ("0001399d", "Elven Bow", "Archery", "Elven")
createWeapon(connect, weapon_elven_bow)
weapon_glass_bow = ("000139a5", "Glass Bow", "Archery", "Glass")
createWeapon(connect, weapon_glass_bow)
weapon_ebony_bow = ("000139ad", "Ebony Bow", "Archery", "Ebony")
createWeapon(connect, weapon_ebony_bow)
weapon_daedric_bow = ("000139b5", "Daedric Bow", "Archery", "Daedric")
createWeapon(connect, weapon_daedric_bow)

# FORGEABILITY
steel_forgeability = (2, "Steel Smithing")
createForgeability(connect, steel_forgeability)
orcish_forgeability = (6, "Orcish Smithing")
createForgeability(connect, orcish_forgeability)
dwarven_forgeability = (12, "Dwarven Smithing")
createForgeability(connect, dwarven_forgeability)
elven_forgeability = (19, "Elven Smithing")
createForgeability(connect, elven_forgeability)
glass_forgeability = (27, "Glass Smithing")
createForgeability(connect, glass_forgeability)
ebony_forgeability = (36, "Ebony Smithing")
createForgeability(connect, ebony_forgeability)
daedric_forgeability = (46, "Daedric Smithing")
createForgeability(connect, daedric_forgeability)

# ENCHANTMENTS
banish_enchantment = ("Banish", "Sends conjured Daedra back to Oblivion", "One-Handed Sword")
createEnchanting(connect, banish_enchantment)
chaos_enchantment = ("Chaos", "Randomized frost, fire, sparks damage", "One-Handed Axe")
createEnchanting(connect, chaos_enchantment)
frost_enchantment = ("Frost", "Frost damage and drain stamina", "One-Handed Mace")
createEnchanting(connect, frost_enchantment)
fear_enchantment = ("Fear", "People/creatures at a certain level flee", "One-Handed Dagger")
createEnchanting(connect, fear_enchantment)
fire_enchantment = ("Fire", "Fire damage and setting targets on fire", "Two-Handed Sword")
createEnchanting(connect, fire_enchantment)
paralyze_enchantment = ("Paralyze", "Paralyzes people/creatures for a certain time", "Two-Handed Axe")
createEnchanting(connect, paralyze_enchantment)
shock_enchantment = ("Shock", "Shock damage and drain magicka", "Two-Handed Mace")
createEnchanting(connect, shock_enchantment)
water_enchantment = ("Water", "Water damage and draining magicka", "Bow")
createEnchanting(connect, water_enchantment)
health_drain_enchantment = ("HealthDrain", "Drains health from people/creatures at a certain rate", "One-Handed Sword")
createEnchanting(connect, health_drain_enchantment)
stamina_drain_enchantment = ("StaminaDrain", "Drains stamina from people/creatures at a certain rate", "One-Handed Axe")
createEnchanting(connect, stamina_drain_enchantment)
magicka_drain_enchantment = ("MagickaDrain", "Drains magicka from people/creatures at a certain rate", "One-Handed Mace")
createEnchanting(connect, magicka_drain_enchantment)
soul_trap_enchantment = ("SoulTrap", "Upon death, the persons/creatures soul is absorbed into a soul gem", "One-Handed Dagger")
createEnchanting(connect, soul_trap_enchantment)

# ENCHANTED WEAPONS
iron_sword_of_drain_health = ("00012eb7", "HealthDrain")
createEnchantedWith(connect, iron_sword_of_drain_health)
orcish_bow_of_water = ("0001398d", "Water")
createEnchantedWith(connect, orcish_bow_of_water)

# DATA INSERTION, UPDATES, AND DELETIONS
# INSERTIONS
# Adding the weaponry and associated material and forgeability perk
# from the Dragonborn DLC.
def addDragonbornDLC():
	# MATERIALS
	# Nordic
	material_nordic_onehand_sword = ("Nordic", 12, 11, 290, None, "Advanced Armors")
	createMaterial(connect, material_nordic_onehand_sword)
	material_nordic_onehand_axe = ("Nordic", 14, 12, 350, None, "Advanced Armors")
	createMaterial(connect, material_nordic_onehand_axe)
	material_nordic_onehand_mace = ("Nordic", 16, 13, 410, None, "Advanced Armors")
	createMaterial(connect, material_nordic_onehand_mace)
	material_nordic_onehand_dagger = ("Nordic", 3.5, 8, 115, None, "Advanced Armors")
	createMaterial(connect, material_nordic_onehand_dagger)
	material_nordic_twohand_sword = ("Nordic", 19, 20, 585, None, "Advanced Armors")
	createMaterial(connect, material_nordic_twohand_sword)
	material_nordic_twohand_axe = ("Nordic", 23, 21, 650, None, "Advanced Armors")
	createMaterial(connect, material_nordic_twohand_axe)
	material_nordic_twohand_mace = ("Nordic", 27, 23, 700, None, "Advanced Armors")
	createMaterial(connect, material_nordic_twohand_mace)
	material_nordic_bow = ("Nordic", 11, 13, 580, 0.6875, "Advanced Armors")
	createMaterial(connect, material_nordic_bow)
	# Stalhrim
	material_stalhrim_onehand_sword = ("Stalhrim", 14, 13, 985, None, "Ebony Smithing")
	createMaterial(connect, material_stalhrim_onehand_sword)
	material_stalhrim_onehand_axe = ("Stalhrim", 16, 15, 1180, None, "Ebony Smithing")
	createMaterial(connect, material_stalhrim_onehand_axe)
	material_stalhrim_onehand_mace = ("Stalhrim", 18, 16, 1375, None, "Ebony Smithing")
	createMaterial(connect, material_stalhrim_onehand_mace)
	material_stalhrim_onehand_dagger = ("Stalhrim", 4.5, 10, 395, None, "Ebony Smithing")
	createMaterial(connect, material_stalhrim_onehand_dagger)
	material_stalhrim_twohand_sword = ("Stalhrim", 21, 23, 1970, None, "Ebony Smithing")
	createMaterial(connect, material_stalhrim_twohand_sword)
	material_stalhrim_twohand_axe = ("Stalhrim", 25, 24, 2150, None, "Ebony Smithing")
	createMaterial(connect, material_stalhrim_twohand_axe)
	material_stalhrim_twohand_mace = ("Stalhrim", 29, 26, 2850, None, "Ebony Smithing")
	createMaterial(connect, material_stalhrim_twohand_mace)
	material_stalhrim_bow = ("Stalhrim", 15, 17, 1800, 0.5625, "Ebony Smithing")
	createMaterial(connect, material_stalhrim_bow)

	# WEAPONS
	# Nordic
	weapon_nordic_onehand_sword = ("xx01cdb1", "Nordic Sword", "One-Handed Sword", "Nordic")
	createWeapon(connect, weapon_nordic_onehand_sword)
	weapon_nordic_onehand_axe = ("xx01cdb2", "Nordic War Axe", "One-Handed Axe", "Nordic")
	createWeapon(connect, weapon_nordic_onehand_axe)
	weapon_nordic_onehand_mace = ("xx01cdb0", "Nordic Mace", "One-Handed Mace", "Nordic")
	createWeapon(connect, weapon_nordic_onehand_mace)
	weapon_nordic_onehand_dagger = ("xx01cdae", "Nordic Dagger", "One-Handed Dagger", "Nordic")
	createWeapon(connect, weapon_nordic_onehand_dagger)
	weapon_nordic_twohand_sword = ("xx01cdaf", "Nordic Greatsword", "Two-Handed Sword", "Nordic")
	createWeapon(connect, weapon_nordic_twohand_sword)
	weapon_nordic_twohand_axe = ("xx01cdad", "Nordic Battleaxe", "Two-Handed Axe", "Nordic")
	createWeapon(connect, weapon_nordic_twohand_axe)
	weapon_nordic_twohand_mace = ("xx01cdb3", "Nordic Warhammer", "Two-Handed Mace", "Nordic")
	createWeapon(connect, weapon_nordic_twohand_mace)
	weapon_nordic_bow = ("xx026232", "Nordic Bow", "Archery", "Nordic")
	createWeapon(connect, weapon_nordic_bow)
	# Stalhrim
	weapon_stalhrim_onehand_sword = ("xx01cdb8", "Stalhrim Sword", "One-Handed Sword", "Stalhrim")
	createWeapon(connect, weapon_stalhrim_onehand_sword)
	weapon_stalhrim_onehand_axe = ("xx01cdb9", "Stalhrim War Axe", "One-Handed Axe", "Stalhrim")
	createWeapon(connect, weapon_stalhrim_onehand_axe)
	weapon_stalhrim_onehand_mace = ("xx01cdb7", "Stalhrim Mace", "One-Handed Mace", "Stalhrim")
	createWeapon(connect, weapon_stalhrim_onehand_mace)
	weapon_stalhrim_onehand_dagger = ("xx01cdb5", "Stalhrim Dagger", "One-Handed Dagger", "Stalhrim")
	createWeapon(connect, weapon_stalhrim_onehand_dagger)
	weapon_stalhrim_twohand_sword = ("xx01cdb6", "Stalhrim Greatsword", "Two-Handed Sword", "Stalhrim")
	createWeapon(connect, weapon_stalhrim_twohand_sword)
	weapon_stalhrim_twohand_axe = ("xx01cdb4", "Stalhrim Battleaxe", "Two-Handed Axe", "Stalhrim")
	createWeapon(connect, weapon_stalhrim_twohand_axe)
	weapon_stalhrim_twohand_mace = ("xx01cdba", "Stalhrim Warhammer", "Two-Handed Mace", "Stalhrim")
	createWeapon(connect, weapon_stalhrim_twohand_mace)
	weapon_stalhrim_bow = ("xx026231", "Stalhrim Bow", "Archery", "Stalhrim")
	createWeapon(connect, weapon_stalhrim_bow)

	# FORGEABILITY
	advanced_armors_forgeability = (18, "Advanced Armors")
	createForgeability(connect, advanced_armors_forgeability)

# Adding the weaponry and associated material and forgeability perk
# from the Dawnguard DLC.
def addDawngaurdDLC():
	# MATERIAL
	material_dragonbone_onehand_sword = ("Dragonbone", 19, 15, 1500, None, "Dragon Armor")
	createMaterial(connect, material_dragonbone_onehand_sword)
	material_dragonbone_onehand_axe = ("Dragonbone", 21, 16, 1700, None, "Dragon Armor")
	createMaterial(connect, material_dragonbone_onehand_axe)
	material_dragonbone_onehand_mace = ("Dragonbone", 22, 17, 2000, None, "Dragon Armor")
	createMaterial(connect, material_dragonbone_onehand_mace)
	material_dragonbone_onehand_dagger = ("Dragonbone", 6.5, 12, 600, None, "Dragon Armor")
	createMaterial(connect, material_dragonbone_onehand_dagger)
	material_dragonbone_twohand_sword = ("Dragonbone", 27, 25, 2725, None, "Dragon Armor")
	createMaterial(connect, material_dragonbone_twohand_sword)
	material_dragonbone_twohand_axe = ("Dragonbone", 30, 26, 3000, None, "Dragon Armor")
	createMaterial(connect, material_dragonbone_twohand_axe)
	material_dragonbone_twohand_mace = ("Dragonbone", 33, 28, 4275, None, "Dragon Armor")
	createMaterial(connect, material_dragonbone_twohand_mace)
	material_dragonbone_bow = ("Dragonbone", 20, 20, 2760, 0.75, "Dragon Armor")
	createMaterial(connect, material_dragonbone_bow)

	# WEAPON
	weapon_dragonbone_onehand_sword = ("xx014fce", "Dragonbone Sword", "One-Handed Sword", "Dragonbone")
	createWeapon(connect, weapon_dragonbone_onehand_sword)
	weapon_dragonbone_onehand_axe = ("xx014fcf", "Dragonbone War Axe", "One-Handed Axe", "Dragonbone")
	createWeapon(connect, weapon_dragonbone_onehand_axe)
	weapon_dragonbone_onehand_mace = ("xx014fcd", "Dragonbone Mace", "One-Handed Mace", "Dragonbone")
	createWeapon(connect, weapon_dragonbone_onehand_mace)
	weapon_dragonbone_onehand_dagger = ("xx014fcb", "Dragonbone Dagger", "One-Handed Dagger", "Dragonbone")
	createWeapon(connect, weapon_dragonbone_onehand_dagger)
	weapon_dragonbone_twohand_sword = ("xx014fcc", "Dragonbone Greatsword", "Two-Handed Sword", "Dragonbone")
	createWeapon(connect, weapon_dragonbone_twohand_sword)
	weapon_dragonbone_twohand_axe = ("xx014fc3", "Dragonbone Battleaxe", "Two-Handed Axe", "Dragonbone")
	createWeapon(connect, weapon_dragonbone_twohand_axe)
	weapon_dragonbone_twohand_mace = ("xx014fd0", "Dragonbone Warhammer", "Two-Handed Mace", "Dragonbone")
	createWeapon(connect, weapon_dragonbone_twohand_mace)
	weapon_dragonbone_bow = ("xx0176f1", "Dragonbone Bow", "Archery", "Dragonbone")
	createWeapon(connect, weapon_dragonbone_bow)

	# FORGEABILITY
	dragon_armor_forgeability = (100, "Dragon Armor")
	createForgeability(connect, dragon_armor_forgeability)
addDragonbornDLC()
addDawngaurdDLC()

# UPDATES
# All updates are from the Unofficial Skyrim Patch
print("UPDATES BELOW")
# Fixes the two-handed speed to be 0.75
def updateTwoHandedSwordSpeed(connect, update):
	cursor = connect.cursor()
	cursor.execute("SELECT * FROM Type WHERE Name = 'Two-Handed Sword'")
	rows = cursor.fetchall()
	print("BEFORE TWO-HANDED SWORD TYPE SPEED UPDATE")
	for row in rows:
		print(row)
	SQL = '''UPDATE Type
			 SET Speed = ?
			 WHERE Name = ?'''
	cursor = connect.cursor()
	cursor.execute(SQL, update)
	connect.commit
	cursor = connect.cursor()
	cursor.execute("SELECT * FROM Type WHERE Name = 'Two-Handed Sword'")
	rows = cursor.fetchall()
	print("AFTER UPDATE")
	for row in rows:
		print(row)
	print()
update = (0.75, "Two-Handed Sword")
updateTwoHandedSwordSpeed(connect, update)

#Fixes the ebony war axe to be 14 damage
def updateEbonyOneHandedAxe(connect, update):
	cursor = connect.cursor()
	cursor.execute("SELECT * FROM Material WHERE Name = 'Ebony' AND Damage = 15")
	rows = cursor.fetchall()
	print("BEFORE EBONY ONE-HANDED AXE MATERIAL DAMAGE UPDATE")
	for row in rows:
		print(row)
	SQL = '''UPDATE material
			 SET Damage = ?
			 WHERE Name = ? AND Damage = ?'''
	cursor = connect.cursor()
	cursor.execute(SQL, update)
	connect.commit
	cursor = connect.cursor()
	cursor.execute("SELECT * FROM Material WHERE Name = 'Ebony' AND Damage = 14")
	rows = cursor.fetchall()
	print("AFTER UPDATE")
	for row in rows:
		print(row)
	print()
update = (14, "Ebony", 15)
updateEbonyOneHandedAxe(connect, update)

#Fixes the ebony mace to be 15 damage
def updateEbonyOneHandedMace(connect, update):
	cursor = connect.cursor()
	cursor.execute("SELECT * FROM Material WHERE Name = 'Ebony' AND Damage = 16")
	rows = cursor.fetchall()
	print("BEFORE EBONY ONE-HANDED MACE MATERIAL DAMAGE UPDATE")
	for row in rows:
		print(row)
	SQL = '''UPDATE material
			 SET Damage = ?
			 WHERE Name = ? AND Damage = ?'''
	cursor = connect.cursor()
	cursor.execute(SQL, update)
	connect.commit
	cursor = connect.cursor()
	cursor.execute("SELECT * FROM Material WHERE Name = 'Ebony' AND Damage = 15")
	rows = cursor.fetchall()
	print("AFTER UPDATE")
	for row in rows:
		print(row)
	print()
update = (15, "Ebony", 16)
updateEbonyOneHandedMace(connect, update)

# DELETIONS
print()
print("DELETIONS BELOW")
def deleteIronBow(connect, deletion):
		cursor = connect.cursor()
		cursor.execute("SELECT * FROM Weapon WHERE Name = 'Iron Bow'")
		rows = cursor.fetchall()
		print("BEFORE IRON BOW DELETIONS")
		for row in rows:
			print(row)
		SQL = '''DELETE FROM weapon
				 WHERE Name = ?'''
		cursor = connect.cursor()
		cursor.execute(SQL, deletion)
		connect.commit
		cursor = connect.cursor()
		cursor.execute("SELECT * FROM Weapon WHERE Name = 'Iron Bow'")
		rows = cursor.fetchall()
		print("AFTER UPDATE")
		for row in rows:
			print(row)
		print()
deletion = (("Iron Bow",))
deleteIronBow(connect, deletion)

def deleteSteelBow(connect, deletion):
		cursor = connect.cursor()
		cursor.execute("SELECT * FROM Weapon WHERE Name = 'Steel Bow'")
		rows = cursor.fetchall()
		print("BEFORE IRON BOW DELETIONS")
		for row in rows:
			print(row)
		SQL = '''DELETE FROM weapon
				 WHERE Name = ?'''
		cursor = connect.cursor()
		cursor.execute(SQL, deletion)
		connect.commit
		cursor = connect.cursor()
		cursor.execute("SELECT * FROM Weapon WHERE Name = 'Steel Bow'")
		rows = cursor.fetchall()
		print("AFTER UPDATE")
		for row in rows:
			print(row)
		print()
deletion = (("Steel Bow",))
deleteSteelBow(connect, deletion)

# QUERIES
# Returns all Iron Weapons
def selectIronWeapons(connect):
	cursor = connect.cursor()
	cursor.execute("SELECT Name FROM Weapon WHERE Material = 'Iron'")
	rows = cursor.fetchall()
	print("List Of All Iron Weapons:")
	for row in rows:
		print(row)
	print()

# Returns all bows that have a type speed of over 0.75
def selectBowsBySpeed(connect):
	cursor = connect.cursor()
	cursor.execute("SELECT Name FROM Material WHERE Speed >= 0.75")
	rows = cursor.fetchall()
	print("List Of All Bows That Have a Speed of 0.75 of Above:")
	for row in rows:
		print(row)
	print()

# Returns all of the weapons with enchantments in the database
def selectEnchantedWeapons(connect):
	cursor = connect.cursor()
	cursor.execute("SELECT * FROM EnchantedWith")
	rows = cursor.fetchall()
	print("List Of All Enchanted Items in the Database:")
	for row in rows:
		print(row)
	print()

# Returns the forgeability perk names that require a higher level than 20
def selectForgeabilityPerkLevel(connect):
		cursor = connect.cursor()
		cursor.execute("SELECT Perk_Name FROM Forgeability WHERE Level > 20")
		rows = cursor.fetchall()
		print("List Of Forging Perks that Require a Level Higher Than 20:")
		for row in rows:
			print(row)
		print()

# Returns the one-handed and two-handed dwarven axes
def selectAllDwarvenAxes(connect):
		cursor = connect.cursor()
		cursor.execute("SELECT Name FROM Weapon WHERE Material = 'Dwarven' AND Type = 'One-Handed Axe'")
		rows = cursor.fetchall()
		print("List Of Dwarven Axes:")
		for row in rows:
			print(row)
		cursor = connect.cursor()
		cursor.execute("SELECT Name FROM Weapon WHERE Material = 'Dwarven' AND Type = 'Two-Handed Axe'")
		rows = cursor.fetchall()
		for row in rows:
			print(row)
		print()

# Returns all available enchantments for Warhammers/Two-Handed Maces
def selectEnchantmentsForWarhammers(connect):
		cursor = connect.cursor()
		cursor.execute("SELECT Name, Effect FROM Enchanting WHERE Weapon = 'Two-Handed Mace'")
		rows = cursor.fetchall()
		print("List Of All Available Enchantments for Warhammers/Two-Handed Maces:")
		for row in rows:
			print(row)
		print()

# Returns all weapons that have a damage higher than 13
def selectHighestDamage(connect):
		cursor = connect.cursor()
		cursor.execute("SELECT Damage, Weight, Name FROM Material WHERE Damage > 13")
		rows = cursor.fetchall()
		print("List Of The Highest Damage Weapons, Alongside Their Weight and Material:")
		for row in rows:
			print(row)
		print()

print()
print("QUERY RESULTS DISPLAYED BELOW")
# Query #1: Every iron weapon
selectIronWeapons(connect)
selectBowsBySpeed(connect)
selectEnchantedWeapons(connect)
selectForgeabilityPerkLevel(connect)
selectAllDwarvenAxes(connect)
selectEnchantmentsForWarhammers(connect)
selectHighestDamage(connect)
