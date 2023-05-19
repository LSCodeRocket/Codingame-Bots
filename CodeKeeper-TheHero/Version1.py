import sys
import numpy as np
from enum import Enum

DEBUG_FLAG = True 

def DebugLog(log):
    if(not DEBUG_FLAG):
        return
    print(log, file=sys.stderr)

class EnemyKeyData:
    def __init__(self, view_range, attack_range, damage):
        self.view_range = view_range
        self.attack_range = attack_range
        self.damage = damage

MapEntityType = Enum("MapEntityType", ['EXIT', 'OBSTACLE'])
ItemType = Enum('ItemType', ['TREASURE', "POTION", "HAMMER", "SCYTHE", "BOW"])
MonsterType = Enum('MonsterType', ['BOX', "SKELETON", "GARGOYLE", "ORC", "VAMPIRE"])

MonsterKeyData = {
    MonsterType.BOX : EnemyKeyData(0, 0, 0),
    MonsterType.SKELETON : EnemyKeyData(1, 1, 1),
    MonsterType.GARGOYLE : EnemyKeyData(2, 1, 1),
    MonsterType.ORC : EnemyKeyData(2, 2, 1),
    MonsterType.VAMPIRE : EnemyKeyData(3, 1, 3)
}



class PlayerStatus:
    def __init__(self, x, y, health, score, hammer_charges, scythe_charges, bow_charges):
        self.x = x
        self.y = y
        self.health = health
        self.score = score
        self.hammer_charges = hammer_charges
        self.scythe_charges = scythe_charges
        self.bow_charges = bow_charges
    
    def displayPlayerInformation(self):
        DebugLog("-" * 4 + "PLAYER INFORMATION" + "-" * 4)
        DebugLog(f"X : {self.x}, Y : {self.y}, 💗 : {self.health}, $ : {self.score}")
        DebugLog(f"🔨 : {self.hammer_charges}, 🔪 : {self.scythe_charges}, 🏹 : {self.bow_charges}")



class EnemyStatus:
    def __init__(self, x, y, health, view_range = 0, attack_range = 0, damage = 0):
        self.x = x
        self.y = y
        self.health = health
        self.view_range = view_range
        self.attack_range = attack_range
        self.damage = damage
    
    def displayEnemyInformation(self):
        DebugLog("-" * 4 + "ENEMY INFORMATION" + "-" * 4)
        DebugLog(f"X : {self.x}, Y : {self.y}, 💗 : {self.health}")
        DebugLog(f"👁️ : {self.view_range}, 🥊 : {self.attack_range}, ⚔️ : {self.damage}")

    def LoadKeyData(self, view_range, attack_range, damage):
        self.view_range = view_range
        self.attack_range = attack_range
        self.damage = damage
    
    def LoadKeyData(self, key_data):
        self.view_range = key_data.view_range
        self.attack_range = key_data.attack_range
        self.damage = key_data.damage

class ItemStatus:
    def __init__(self, x, y, item_type, value):
        self.x = x
        self.y = y
        self.item_type = item_type
        self.value = value
    
    def displayItemInformation(self):
        DebugLog("-" * 4 + "ITEM INFORMATION" + "-" * 4)
        DebugLog(f"X : {self.x}, Y : {self.y}")
        DebugLog(f"$ : {self.value}, 📦 : {self.item_type.name}")

class EntityContainer:
    # Types of Items + 2 values ( x, y )
    ITEM_VECTOR_SIZE = len(ItemType) + 2 

    # 3 ( view_range, attack_range, damage ) + 
    # 2 ( x and y )
    # 1 ( health )
    ENEMY_VECTOR_SIZE = 3 + 2 + 1 
    
    def __init__(self, enemy_list, item_list):
        self.enemy_list = enemy_list
        self.item_list = item_list
        self.enemy_matrix = None
        self.item_matrix = None

    def itemsToMatrix(self):
        _items_matrix = np.zeros(shape = (self.ITEM_VECTOR_SIZE, len(self.item_list))).T

        for i in range(len(self.item_list)):
            item = self.item_list[i]

            x = item.x
            y = item.y
            item_type = item.item_type
            value = item.value
            
            item_vector = np.array([x, y, 0, 0, 0, 0, 0])
            item_vector[2+item_type.value] = value
            _items_matrix[i] = item_vector
        
        self.item_matrix = _items_matrix.T
        return _items_matrix.T
    

    def monstersToMatrix(self):
        _monsters_matrix = np.zeros(shape = (self.ENEMY_VECTOR_SIZE, len(self.enemy_list))).T

        for i in range(len(self.enemy_list)):
            enemy = self.enemy_list[i]

            x = enemy.x
            y = enemy.y
            health = enemy.health
            view_range = enemy.view_range
            attack_range = enemy.attack_range
            damage = enemy.damage
            
            _monsters_matrix[i] = np.array([x, y, health, view_range, attack_range, damage])
        
        self.enemy_matrix = _monsters_matrix.T
        return _monsters_matrix.T
    
    def addEnemy(self, enemy):
        self.enemy_list.append(enemy)
    
    def addItem(self, item):
        self.item_list.append(item)
        
    def itemsAndMonstersToMatrix(self):
        self.monstersToMatrix()
        self.itemsToMatrix()

def pushBackEntity(entity_list, x, y, etype, value):
    if etype <= 1:
        return
    if etype >= 2 and etype <= 6:
        entity_list.addItem(ItemStatus(x, y, ItemType(etype), value))
        return
    if etype >= 7 and etype <= 11:
        E = EnemyStatus(x, y, value)
        E.LoadKeyData(MonsterKeyData[MonsterType(etype - 6)])
        entity_list.addEnemy(E)
        return
    
    DebugLog("Severely Undefined Behavior. To be Honest, I didn't think this was possible.")

def getVisibleEntityData(entity_list):
    visible_entities = int(input())  # the number of visible entities

    for i in range(visible_entities):
        ex, ey, etype, evalue = [int(j) for j in input().split()]
        pushBackEntity(entity_list, ex, ey, etype, evalue)

while True:
    x, y, health, score, charges_hammer, charges_scythe, charges_bow = [int(i) for i in input().split()]
    
    playerInfo = PlayerStatus(x, y, health, score, charges_hammer, charges_scythe, charges_bow)

    entity_list = EntityContainer([], [])
    
    getVisibleEntityData(entity_list)
    
    DebugLog(entity_list)

    print("MOVE 6 8 Let's go!")
