DROP DATABASE IF EXISTS Lostbase;
CREATE DATABASE Lostbase;
USE Lostbase;

CREATE TABLE Location
(
  LocationID INT NOT NULL,
  Name VARCHAR(250) NOT NULL,
  Description VARCHAR(250),
  PRIMARY KEY (LocationID)
);

CREATE TABLE NPC
(
  NPCID INT NOT NULL,
  Name VARCHAR(40) NOT NULL,
  Description VARCHAR(250),
  Health INT,
  LocationID INT NOT NULL,
  PRIMARY KEY (NPCID),
  FOREIGN KEY (LocationID) REFERENCES Location(LocationID)
);

CREATE TABLE Direction (
	DirectionID VARCHAR(10) NOT NULL,
	Description VARCHAR(40),
	PRIMARY KEY (DirectionID)
);

CREATE TABLE Movement
(
  #Compass VARCHAR(40) NOT NULL,
  #LocationID_1 INT NOT NULL,
  #MovementLocationID_2 INT NOT NULL,
  
  MovementID VARCHAR(10) NOT NULL,
  Source INT,
  Destination INT,
  Direction VARCHAR(10),
  Locked BOOL,
  Locknote VARCHAR(40),
  PRIMARY KEY (MovementID),
  FOREIGN KEY (Source) REFERENCES Location(LocationID),
  FOREIGN KEY (Destination) REFERENCES Location(LocationID),
  FOREIGN KEY (Direction) REFERENCES Direction(DirectionID)
  #NOT IN ERDPLUS!
);



CREATE TABLE Player
(
  PlayerID INT NOT NULL,
  LocationID INT NOT NULL,
  PRIMARY KEY (PlayerID),
  FOREIGN KEY (LocationID) REFERENCES Location(LocationID)
);

CREATE TABLE Item
(
  ItemID INT NOT NULL,
  Name VARCHAR(40) NOT NULL,
  Description VARCHAR(250),
  PlayerID INT,
  LocationID INT,
  PRIMARY KEY (ItemID),
  FOREIGN KEY (PlayerID) REFERENCES Player(PlayerID),
  FOREIGN KEY (LocationID) REFERENCES Location(LocationID)
);

CREATE TABLE KillWeapon
(
  ItemID INT NOT NULL,
  NPCID INT NOT NULL,
  PRIMARY KEY (ItemID, NPCID),
  FOREIGN KEY (ItemID) REFERENCES Item(ItemID),
  FOREIGN KEY (NPCID) REFERENCES NPC(NPCID)
);

#LOCATION
INSERT INTO `location` (`LocationID`, `Name`, `Description`) VALUES
	(1, 'You are at the beach.', 'There\'s beautiful golden sand under your feet.'),
	(2, 'This is a dead end.', 'There\'s nothing interesting over here.'),
	(3, 'You are at the beach standing next to a shipwreck.', 'You are standing at the beach with an old shipwreck next to you (E). To the north there is a huge and dark forest.'),
	(4, 'You are on the deck of the ship.', 'You are on the deck of the shipwreck. The old floor feels quite unstable beneath you. There\'s a door to the cargo hold below you. You can see an old Zippo lighter on the floor.'),
	(5, 'You are in the cargo hold of the ship.', 'You are in the cargo hold. It\'s dark but you can see some items scattered around the hold.'),
	(6, 'You are in the forest.', 'You are in the forest. There\'s a polished statue of a deer that looks almost too clean from moss and vines. There\'s is something mysterious about the statue.'),
	(7, 'A wild Python appears! It starts to strangle you and you are unable to move. What will you do?', 'The sun reflects from the slimy skin of the Python. You are starting to lose your breath!'),
	(8, 'You are in the forest.', 'There are vines and monkey poo everywhere.'),
	(9, 'You are in the forest.', 'A huge tree is growing here. You can see and hear unfamiliar birds chirping. They must be nesting in the tree.'),
	(10, 'You are in the forest.', 'You can see more trees and vines. Looks like there is an old gate behind the bushes.'),
	(11, 'You are in the forest.', 'Sunshine is coming through the treetops. And you can feel a cooling breeze joined my a peculiar smell.'),
	(12, 'You enter an old temple.', 'There\'s a beam of sunlight shining on to a pile of gold! There\'s also a black sail in the corner.'),
	(13, 'You are in a field.', 'There\'s a path to the north to the mountain. You noticed another similar deer statue as before.'),
	(14, 'You are on a steep mountain path, there\'s a figure in the distance.', 'It\'s a large deer stag with majestic antlers. The antlers might come in handy, if only there was a way to get them... There\'s a path to the tip of the mountain to the west and another path to the east.'),
	(15, 'You reached the top of the mountain.', 'Nothing but some pebbles and wasted dreams up here. The horizon is beautiful but there\'s no land visible in any direction.'),
	(16, 'You are at a cave entrance.', 'It\'s so dark you cannot proceed without some light. You can hear some growling echoing from the cave.'),
	(17, 'A wild and very very angry bear appears from the shadows! It starts to charge towards you! What will you do?', 'The bear is full of scars that look man-made, no wonder it is angry!'),
	(18, 'You are standing on a muddy path with many footprints. You are not the first person here.', 'You can see smoke rising from a village to the south and the dark cave to the west.'),
	(19, 'An important looking man is standing in the middle of the village square. There is a hut to the west and one to the east. To the south you can see a small beach.', 'He is smiling and waving towards you, dressed in beautiful ceremonial clothes.'),
	(20, 'You are in someone\'s house.', 'It\'s made of some wood and hay. You can see pile of hay and a campfire with a small pile of wood next to it.'),
	(21, 'You are in someone\'s house.', 'It\'s made of mud and hay. You can see a dead campfire with a small pile of wood next to it. There\'s a door to the east with a unpleasant odor coming from behind the it.'),
	(22, 'This is the out house.', 'There\'s rat on the floor with a funky smell. The toilet seat looks very inviting though.'),
	(23, 'You are at a small beach.', 'It\'s sunny and the water looks warm and calm. You can see a wreck of some old raft. You wonder if you could repair it. Then again there is probably a ship lane close by, why not try and swim for it?.');


#DIRECTIONS
INSERT INTO `direction` (`DirectionID`, `Description`) VALUES
	('D', 'Down'),
	('E', 'East'),
	('N', 'North'),
	('S', 'South'),
	('U', 'Up'),
	('W', 'West');
	
#ITEMS
INSERT INTO `item` (`ItemID`, `Name`, `Description`, `PlayerID`, `LocationID`) VALUES
	(1, 'Gun', 'It\s an old Luger but it doesn\'t seem broken.', NULL, 5),
	(2, 'Machete', 'It\'s a machete. It\'s so sharp you could cut a stone with it.', NULL, 5),
	(3, 'Bullet', '7.65 caliber bullets, perfect for the Luger.', NULL, 5),
	(4, 'Bullet', '7.65 caliber bullets, perfect for the Luger.', NULL, 5),
	(5, 'Wood', 'Wood from the islands forrest.', NULL, 20),
	(6, 'Wood', 'Wood from the islands forrest.', NULL, 21),
	(7, 'Treasure', 'Treasure chest full of gold items with precious gemstones. And one stone.', NULL, 12),
	(8, 'Rope', 'Some old rope.', NULL, 5),
	(9, 'Key', 'Shiny key. It\'s says Abloy on it.', NULL, 5),
	(10, 'Lighter', 'An old Zippo lighter.', NULL, 4),
	(11, 'Sail', 'A black sail, looks like something a pirate would use.', NULL, 12),
	(12, 'Antlers', 'Huge antlers from a majestic beast.', NULL, NULL),
	(13, 'Claws', 'Long and sharp claws from the mighty beast, these will look amazing as earings!', NULL, NULL),
	(14, 'Note', 'Don\'t jump! I hear the creators of the game are working on a sequel.', NULL, 15),
	(15, 'Magazine', 'Looks like an old Donald Duck -magazine. The pages are slightly water damaged. It\'s still readable though.', NULL, 22);
	

#NPC
INSERT INTO `npc` (`NPCID`, `Name`, `Description`, `Health`, `LocationID`) VALUES
	(1, 'Python', 'It\'s a python! And it\'s gonna attack!', 1, 7),
	(2, 'Deer', 'You can see a majestetic deer. It has pearly white antlers and a soft glowy fur.', 1, 14),
	(3, 'Bear', 'It\'s a bear. He\'s just standing there and looking at you.', 1, 17),
	(4, 'Villager', 'The Chief. He\'s wearing fur from different animals.' , 1, 19);
	

#KILLWEAPON
INSERT INTO `killweapon` (`ItemID`, `NPCID`) VALUES
	(1, 2),
	(1, 3),
	(1, 4),
	(2, 1),
	(2, 3),
	(2, 4);
	

#MOVEMENT
INSERT INTO `movement` (`MovementID`, `Source`, `Destination`, `Direction`, `Locked`, `Locknote`) VALUES
	('BeDe', 1, 2, 'W', 0, NULL),
	('BeSh', 1, 3, 'E', 0, NULL),
	('BeSq', 23, 19, 'N', 0, NULL),
	('CaCe', 17, 16, 'W', 1, NULL),
	('CaDe', 5, 4, 'U', 0, NULL),
	('CaVi', 17, 18, 'E', 1, NULL),
	('CeCa', 16, 17, 'E', 1, 'It\'s too dark to go in'),
	('CeMo', 16, 14, 'W', 0, NULL),
	('DeBe', 2, 1, 'E', 0, NULL),
	('DeCa', 4, 5, 'D', 0, NULL),
	('DeSh', 4, 3, 'W', 0, NULL),
	('F10F9', 10, 9, 'N', 0, NULL),
	('F10Tr', 10, 12, 'W', 1, 'It\'s a locked gate'),
	('F11F10', 11, 10, 'W', 0, NULL),
	('F11F6', 11, 6, 'E', 0, NULL),
	('F11F8', 11, 8, 'N', 0, NULL),
	('F6F7', 6, 7, 'N', 0, NULL),
	('F7F6', 7, 6, 'S', 1, NULL),
	('F7F8', 7, 8, 'E', 1, NULL),
	('F8F11', 8, 11, 'S', 0, NULL),
	('F8F7', 8, 7, 'E', 0, NULL),
	('F8F9', 8, 9, 'W', 0, NULL),
	('F8Fi', 8, 13, 'N', 0, NULL),
	('F9F10', 9, 10, 'S', 0, NULL),
	('FiF8', 13, 8, 'S', 0, NULL),
	('FiMo', 13, 14, 'N', 0, NULL),
	('H1Sq', 20, 19, 'E', 0, NULL),
	('H2Ou', 21, 22, 'E', 0, NULL),
	('H2Sq', 21, 19, 'W', 0, NULL),
	('MoCe', 14, 16, 'E', 0, NULL),
	('MoFi', 14, 13, 'S', 0, NULL),
	('MoTi', 14, 15, 'W', 0, NULL),
	('OuH2', 22, 21, 'W', 0, NULL),
	('ShBe', 3, 1, 'W', 0, NULL),
	('ShDe', 3, 4, 'E', 0, NULL),
	('ShF6', 3, 6, 'N', 0, NULL),
	('SqBe', 19, 23, 'S', 0, NULL),
	('SqH1', 19, 20, 'W', 0, NULL),
	('SqH2', 19, 21, 'E', 0, NULL),
	('SqVi', 19, 18, 'N', 0, NULL),
	('TiMo', 15, 14, 'E', 0, NULL),
	('TrF10', 12, 10, 'E', 0, NULL),
	('ViCa', 18, 17, 'W', 0, NULL),
	('ViSq', 18, 19, 'S', 0, NULL),
	('F6Sh', 6, 3, 'S', 0, NULL),
	('F6F11', 6, 11, 'W', 0, NULL),
	('F10F11', 10, 11, 'E', 0, NULL),
	('F9F8', 9, 8, 'E', 0, NULL);

#PLAYER
INSERT INTO `player` (`PlayerID`, `LocationID`) VALUES
	(1, 1);