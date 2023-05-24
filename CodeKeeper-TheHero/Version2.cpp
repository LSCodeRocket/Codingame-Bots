#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
using namespace std;

bool DEBUG_FLAG = true;

void DebugLog(string log)
{
    if (!DEBUG_FLAG)
    {
        return;
    }
    cerr << "[DEBUG] " << log << endl;
}

struct PlayerStatus
{
    int x;
    int y;
    int health;
    int score;
    int hammer_charges;
    int scythe_charges;
    int bow_charges;
};

enum MapEntityType
{
    EXIT,
    OBSTACLE
};

enum ItemType
{
    TREASURE,
    POTION,
    HAMMER,
    SCYTHE,
    BOW
};

enum MonsterType
{
    BOX,
    SKELETON,
    GARGOYLE,
    ORC,
    VAMPIRE
};

struct EnemyStatus
{
    int x;
    int y;
    int health;
    int view_range;
    int attack_range;
    int damage;
};
struct EnemyKeyData
{
    int view_range;
    int attack_range;
    int damage;
};

struct ItemStatus
{
    int x;
    int y;
    ItemType item_type;
    int value;
};

struct EntityList
{
    vector<EnemyStatus> enemy_vector;
    vector<ItemStatus> item_vector;
};

PlayerStatus getFramePlayerData()
{

    PlayerStatus player_data;

    cin >> player_data.x >> player_data.y >> player_data.health >> player_data.score >> player_data.hammer_charges >> player_data.scythe_charges >> player_data.bow_charges;

    cin.ignore();
    return player_data;
}

void addItemStatus(EntityList &entity_list, int x, int y, int type, int value)
{

    ItemStatus item_for_push_back;

    item_for_push_back.item_type = static_cast<ItemType>(type - 2);
    item_for_push_back.x = x;
    item_for_push_back.y = y;
    item_for_push_back.value = value;
    entity_list.item_vector.push_back(item_for_push_back);

    DebugLog("ITEM VALUE : " + to_string(value) + " X: " + to_string(x) + " Y: " + to_string(y));
}

EnemyKeyData parseEnemyKeyData(int enemy_type)
{
    EnemyKeyData enemy_data;
    switch (static_cast<MonsterType>(enemy_type))
    {
    case MonsterType::BOX:
        enemy_data.view_range = 0;
        enemy_data.attack_range = 0;
        enemy_data.damage = 0;
        break;
    case MonsterType::SKELETON:
        enemy_data.view_range = 1;
        enemy_data.attack_range = 1;
        enemy_data.damage = 1;
        break;
    case MonsterType::GARGOYLE:
        enemy_data.view_range = 2;
        enemy_data.attack_range = 1;
        enemy_data.damage = 1;
        break;
    case MonsterType::ORC:
        enemy_data.view_range = 2;
        enemy_data.attack_range = 2;
        enemy_data.damage = 1;
        break;
    case MonsterType::VAMPIRE:
        enemy_data.view_range = 3;
        enemy_data.attack_range = 1;
        enemy_data.damage = 3;
    default:
        return enemy_data;
    }
    return enemy_data;
}

void addEnemyStatus(EntityList &entity_list, int x, int y, int type, int value)
{
    EnemyStatus enemy_for_push_back;
    enemy_for_push_back.health = value;
    enemy_for_push_back.x = x;
    enemy_for_push_back.y = y;

    EnemyKeyData current_enemy_data = parseEnemyKeyData(type);
    enemy_for_push_back.view_range = current_enemy_data.view_range;
    enemy_for_push_back.attack_range = current_enemy_data.attack_range;
    enemy_for_push_back.damage = current_enemy_data.damage;

    entity_list.enemy_vector.push_back(enemy_for_push_back);
    DebugLog("ENEMY: Health: " + to_string(value) + " X: " + to_string(x) + " Y: " + to_string(y) + " Type: " + to_string(type));
}

void pushBackEntity(EntityList &entity_list, int x, int y, int type, int value)
{

    if (type <= 1)
    {
        return;
    }
    if (type >= 2 && type <= 6)
    {
        addItemStatus(entity_list, x, y, type, value);
        return;
    }
    if (type >= 7 && type <= 11)
    {
        addEnemyStatus(entity_list, x, y, type, value);
        return;
    }
    DebugLog("Severely Undefined Behavior. To be honest, I didn't think this was possible.");
}

EntityList initializeEntityList()
{
    EntityList entity_list;
    entity_list.enemy_vector = vector<EnemyStatus>();
    entity_list.item_vector = vector<ItemStatus>();
    return entity_list;
}

EntityList getVisibleEntityData()
{

    EntityList visible_entity_list = initializeEntityList();

    int visible_entities; // the number of visible entities
    cin >> visible_entities;
    cin.ignore();

    for (int i = 0; i < visible_entities; i++)
    {

        int ex;     // x position of the entity
        int ey;     // y position of the entity
        int etype;  // the type of the entity
        int evalue; // value associated with the entity

        cin >> ex >> ey >> etype >> evalue;
        cin.ignore();

        pushBackEntity(visible_entity_list, ex, ey, etype, evalue);
    }

    return visible_entity_list;
}

int main()
{

    while (1)
    {
        PlayerStatus player_data = getFramePlayerData();

        EntityList visible_entities = getVisibleEntityData();

        // Write an action using cout. DON'T FORGET THE "<< endl"
        // To debug: cerr << "Debug messages..." << endl;

        cout << "MOVE 6 8 Let's go!" << endl; // MOVE x y [message] | ATTACK weapon x y [message]
    }
}