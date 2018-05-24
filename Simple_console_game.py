
#singular, plural inv print
#better drop system
#
#get class type name
#item_check = str(item)
#item_name = item_check[10:len(item_check) - 22]
#
#
import pickle
import random
import sys
import time
import os
import win32gui

hwnd = win32gui.GetForegroundWindow()
win32gui.MoveWindow(hwnd, 0, 0, 1000, 400, True)
os.system("mode con cols=120 lines=30")

class Console:

    def clear():
        os.system('cls' if os.name=='nt' else 'clear')

    def combat_screen(next_action, enemy, extra_text = None):
        Console.clear()
        if not extra_text == None:
           lines_in = extra_text.split("\n")
        else:
             lines_in = []
        print("horse")

        for i in range(len(lines_in),31):
            lines_in.append("")

        line_1 = lines_in[0]
        line_2 = lines_in[1]
        line_3 = lines_in[2]
        line_4 = lines_in[3]
        line_5 = lines_in[4]
        line_6 = lines_in[5]
        line_7 = lines_in[6]
        line_8 = lines_in[7]
        line_9 = lines_in[8]
        line_10 = lines_in[9]
        line_11 = lines_in[11]
        line_12 = lines_in[12]
        line_13 = lines_in[13]
        line_14 = lines_in[14]
        line_15 = lines_in[15]
        line_16 = lines_in[16]
        line_17 = lines_in[17]
        line_18 = lines_in[18]
        line_19 = lines_in[19]
        line_20 = lines_in[20]
        line_21 = lines_in[21]
        line_22 = lines_in[22]
        line_23 = lines_in[23]
        line_24 = lines_in[24]
        line_25 = lines_in[25]
        line_26 = lines_in[26]
        line_27 = lines_in[27]
        line_28 = lines_in[28]
        line_29 = lines_in[29]

        standing_line = chr(124)
        block = chr(9608)
        top_line = chr(175)

        any_bot_healthbar = " " + top_line * 10

        player_top_healthbar = " " + "_" * 10 + player.name
        enemy_top_healthbar = " " + "_" * 10 + enemy.name

        player_hp = int((player.current_hp / player.max_hp)* 10)
        enemy_hp = int((enemy.current_hp / enemy.max_hp) * 10)

        player_mid_healthbar = standing_line + \
        block * player_hp + " " * (10 - player_hp) + standing_line + \
        "{}/{} hp".format(player.current_hp, player.max_hp)

        enemy_mid_healthbar = standing_line + \
        block * enemy_hp + " " * (10 - enemy_hp) + standing_line + \
        "{}/{} hp".format(enemy.current_hp, enemy.max_hp)


        log_lines = 4
        max_spacing = max(list(len(GameMaster.action_log[len(GameMaster.action_log) - (i + 1)]) for i in range(log_lines)))
        spacing_1 = " " * (max_spacing - len(GameMaster.action_log[len(GameMaster.action_log) - 1]))
        spacing_2 = " " * (max_spacing - len(GameMaster.action_log[len(GameMaster.action_log) - 2]))
        spacing_3 = " " * (max_spacing - len(GameMaster.action_log[len(GameMaster.action_log) - 3]))
        spacing_4 = " " * (max_spacing - len(GameMaster.action_log[len(GameMaster.action_log) - 4]))


        action_log_mid_1 = standing_line +\
        GameMaster.action_log[len(GameMaster.action_log) - 1]\
        + spacing_1 + standing_line

        action_log_mid_2 = standing_line +\
        GameMaster.action_log[len(GameMaster.action_log) - 2]\
        + spacing_2 + standing_line

        action_log_mid_3 = standing_line +\
        GameMaster.action_log[len(GameMaster.action_log) - 3]\
        + spacing_3 + standing_line

        action_log_mid_4 = standing_line +\
        GameMaster.action_log[len(GameMaster.action_log) - 4]\
        + spacing_4 + standing_line


        action_log_top = " " +\
        "_" * (max(len(GameMaster.action_log[len(GameMaster.action_log) - 1]), len(GameMaster.action_log[len(GameMaster.action_log) - 2]))) + "Action log"
        action_log_bot = " " +\
        top_line * (max(len(GameMaster.action_log[len(GameMaster.action_log) - 1]), len(GameMaster.action_log[len(GameMaster.action_log) - 2])))


        lines = {0: line_1, 1: line_2, 2: line_3, 3: line_4, 4: line_5,\
        5: line_6 + ' ' * (80 - len(line_6)) + enemy_top_healthbar,\
        6: line_7 + ' ' * (80 - len(line_7)) + enemy_mid_healthbar,\
        7: line_8 + ' ' * (80 - len(line_8)) + any_bot_healthbar,\
        8: line_9, 9: line_10, 10: line_11,\
        11: line_12, 12: line_13, 13: line_14, 14: line_15, 15: line_16,\
        16: line_17, 17: line_18, 18: line_19, 19: line_20, 20: line_21,\
        21: line_22 + ' ' * (30 - len(line_22)) + player_top_healthbar\
        + ' ' * (22 - len(player_top_healthbar)) + action_log_top,\
        22: line_23 + ' ' * (30 - len(line_23)) + player_mid_healthbar\
        + ' ' * (22 - len(player_mid_healthbar)) + action_log_mid_1,\
        23: line_24 + ' ' * (30 - len(line_24)) + any_bot_healthbar\
        + ' ' * (22 - len(any_bot_healthbar)) + action_log_mid_2,\
        24: line_25 + ' ' * (52 - len(line_25)) + action_log_mid_3,\
        25: line_26 + ' ' * (52 - len(line_26)) + action_log_mid_4,\
        26: line_27 + ' ' * (52 - len(line_27)) + action_log_bot,\
        27: line_28, 28: next_action,}

        for i in range(0, 29):
            print(eval("lines[i]"))


class statuses:

    def apply_on_fire(target):
        damage_taken = (int((target.current_hp * 0.1)))
        if target == player:
            player.new_awareness('specific', 20)
        return damage_taken

    def apply_frozen(original_speed):
        slowed_speed = (int(original_speed * 0.5))
        return slowed_speed

    def apply_weak(original_damage):
        weakened_damage = int(original_damage * 0.5)
        return weakened_damage

    def apply_blead(target):
        damage_taken = (int(target.max_hp * 0.15))
        return damage_taken



supported_statuses = {
        statuses.apply_on_fire:
        {
            'apply_type': 'start_dot', 'type': 'fire',
            'description': 'on fire',
            'on_apply_message_player': 'Hot! You panic and take',
            'on_apply_message_enemy': 'Hot! '
        },
        statuses.apply_frozen:
        {
            'apply_type': 'weaker_speed', 'type': 'ice',
            'description': 'frozen',
            'on_apply_message_player': '',
            'on_apply_message_enemy': ''
        },
        statuses.apply_blead:
        {
            'apply_type': 'start_dot', 'type': 'bleeding',
            'description': 'bleeding',
            'on_apply_message_player': 'You better stop this bleeding soon... You take',
            'on_apply_message_enemy': 'Blood spills forth as the enemy takes'
        },
        statuses.apply_weak:
        {
            'apply_type': 'weaker_damage', 'type': None,
            'description': 'weak',
            'help': 'Halves the damage of the targets incoming attacks',
            'on_apply_message_player': 'Your attacked is weakend and deals',
            'on_apply_message_enemy': 'The enemys attack is weakened and deals'
        }

    }

class moves:

    def calming_heal(target):
        amount_healed = int((target.current_hp / 5) + (target.max_hp / 10))
        target.current_hp += amount_healed
        if target.current_hp >= target.max_hp:
            target.current_hp = target.max_hp
        if target == player:
            player.new_awareness('decrease', 1)#revert
            return_string = "You heal for {} hp and feel a bit calmer".format(amount_healed)
            return return_string
        else:
            return_string = "The enemy heals for {} hp".format(amount_healed)
            return return_string

    def intense_heal(target):
        amount_healed = int((target.current_hp / 3) + (target.max_hp / 4))
        target.current_hp += amount_healed
        if target.current_hp >= target.max_hp:
            target.current_hp = target.max_hp
        if target == player:
            return_string = "You heal for {} hp".format(amount_healed)
            return return_string
        else:
            return_string = "The enemy heals for {} hp".format(amount_healed)
            return return_string


supported_moves = {
        moves.calming_heal:
        {
        'type': 'heal'
        },
        moves.intense_heal:
        {
        'type': 'heal'
        }

    }


class ArmorEffect:
    pass

armor_effects = {

    }

class WeaponEffect:
    pass

weapon_effects = {

    }

class Item:
    def __init__(self, name, weight, value, item_type, item_id, description, rarity):
        if rarity == "very common":
            droprate = 0.40
        elif rarity == "common":
            droprate = 0.2
        elif rarity == "uncommon":
            droprate = 0.1
        elif rarity == "rare":
            droprate = 0.05
        elif rarity == "legendary":
            droprate = 0.02
        else:
            print("Error: unknown rarity")

        self.name = name
        self.weight = weight
        self.value = value
        self.type = item_type
        self.id = item_id
        self.description = description
        self.rarity = droprate
    def inspect(self):
        if str(self.item_type)[0] in GameMaster.vowels:
            a_or_an = "an"
        else:
            a_or_an = "a"
        print("{}.It is worth {} gold and weighs {}. It is {} {} that is {}".format(\
        self.description, self.value, self.weight, a_or_an,self.item_type, self.rarity))


class Wearable(Item):
    def __init__(self, name, weight, value, item_type, item_id, description, rarity, \
    armor_weight, defense, armor_effect = None):
        Item.__init__(self, name, weight, value, item_type, item_id, description, rarity)
        self.armor_weight = armor_weight
        self.defense = defense
        self.armor_effect = armor_effect
    def inspect(self):
        if str(self.item_type)[0] in GameMaster.vowels:
            a_or_an = "an"
        else:
            a_or_an = "a"
        if hasattr(Wearable, "self.special_effect"):
            special_effect_text = (". {}".format(armor_effects[self.special_effect]['description']))
        else:
            special_effect_text = ""
        print("{}.It is worth {} gold and weighs {}. It is {} {} that is {}{}".format(\
        self.description, self.value, self.weight, a_or_an,self.item_type, self.rarity, special_effect_text))


class Weapon(Item):
    def __init__(self, name, weight, value, item_type, item_id, description, rarity, \
                weapon_damage, special_effect = None, effect_rate = 0):
        Item.__init__(self, name, weight, value, item_type, item_id, description, rarity)
        if effect_rate > 0:
            if effect_rate == "very likely":
                effect_rate = 0.8
            elif effect_rate == "likely":
                effect_rate = 0.6
            elif effect_rate == "unlikely":
                effect_rate = 0.4
            elif effect_rate == "very unlikely":
                effect_rate = 0.2
        self.weapon_damage = weapon_damage
        self. special_effect = special_effect
        self.effect_rate = effect_rate
        def inspect(self):
            if str(self.item_type)[0] in GameMaster.vowels:
                a_or_an = "an"
            else:
                a_or_an = "a"
            if hasattr(Wearable, "self.special_effect"):
                if self.effect_rate == 0.8:
                    likelyness = "is very likely to"
                elif self.effect_rate == 0.6:
                    likelyness = "has a decent chance"
                elif self.effect_rate == 0.4:
                    likelyness = "will maybe"
                elif self.effect_rate == 0.2:
                    likelyness = "will probably not"
                special_effect_text = (". {} and {} affect the enemy".format(armor_effects[self.special_effect]['description']), likelyness)
            else:
                special_effect_text = ""
            print("{}.It is worth {} gold and weighs {}. It is {} {} that is {}{}".format(\
            self.description, self.value, self.weight, a_or_an,self.item_type, self.rarity, special_effect_text))


#blueprint
#item_name = Itemtype('name', weight, value, 'item_type', item_id,
#                       'description', 'rarity' + """optional if other""")
#
#optional if other
#
#wearable
#(..., armor_weight, defense, 'special_effect')
#
#weapon
#(..., weapon_damage, 'special_effect', 'effect_rate')
#
#likelynesses:
#very likely = 0.8
#likely = 0.6
#unlikely = 0.4
#very unlikely = 0.2
#
#
#rarities
#very common = 0.4
#common = 0.2
#uncommon = 0.1
#rare = 0.05
#legendary = 0.02

##feather = Item('feather', 1, 10, 'material', 1, 'A feather from a hen', 'common')
##radish = Item('radish', 1, 20, 'food', 2, 'Fresh from The earth!', 'uncommon')
##
##feather.inspect()






class GameMaster:
    last_damage_player = ""
    vowels = ["a", "o", "u", "e", "i"]
    action_log = ['               ',  '               ',  '               ',  '               ']
    game_state = {}
    statistics = {}

class Character:
    def dealdmg(self, attacker, enemy, damage):
        enemy.current_hp = enemy.current_hp - damage
        if enemy.current_hp <= 0:
            if enemy == player:
                player.dead(attacker)
            else:
                loot_drop(enemy)
        else:
            print("{} has {} hp left".format(enemy.name, enemy.current_hp))

    def apply_effect(self, effect, duration):
        if effect in supported_statuses:
            if effect in self.statuses:
               self.statuses[effect] += duration
            else:
               self.statuses[effect] = duration
        else:
            print("Error: Unknown Effect: {}".format(effect))


class Player(Character):
    unlocked_moves = {}
    statuses = {}
    awareness = 90
    speed = 80
    strength = random.randint(5, 8)
    max_hp = random.randint(25, 30)
    current_hp = max_hp
    current_equips = {'head': 'bare', 'chest': 'bare', 'legs': 'bare'}

    def __init__(self):
        self.name = input("What Will This Adventurer Be Named?\n>>>")

    class Inventory:
        items = {}
        def __init__(self, max_spaces = 10):
            self.max_spaces = max_spaces

        def add_item(self, item, amount = 1):
            current_weight = 0
            if not len(self.items) == 0:
                for thing in self.items:
                    current_weight = current_weight + (thing.weight * self.items[thing])
                if (current_weight + item.weight) <= self.max_spaces:
                    if not item in self.items:
                        self.items[item] = amount
                    else:
                        self.items[item] += amount
                else:
                    print("Your bag can't fit this item")
                    return "bag_full"
            else:
                self.items[item] = amount

        def view(self):
            print("You have: \n")
            for item in self.items:
                if self.items[item] > 1:
                    if item.name[-1] == "h" or item.name[-1] == "H":
                        print('{} {}es'.format(self.items[item], item.name))
                    else:
                        print('{} {}s'.format(self.items[item], item.name))
                else:
                    print('{} {}'.format(self.items[item], item.name))

            def loot_drop(self, enemy):
                print('You successfully defeated {}!'.format(enemy))
                dropped_items = {}
                for item in enemy.drops:
                    if item.rarity * 100 >= random.randint(0, 100):
                        dropped_items[item] = int(item.rarity * enemy.difficulty)

    def alivecheck(self):
        if player.current_hp <= 0:
            if GameMaster.last_damage_player != "":
                player.dead(GameMaster.last_damage_player)
            else:
                print("Error: Player Took Undocumented Damage")

    def dead(self, killer):
        Console.clear()
        print("You were killed by {}.".format(killer))
        time.sleep(3)
        main_menu()

    def unequip(slot):
        if player.current_equips[slot] != 'bare':
            try_unequip = inventory.add_item(player.current_equips[slot])
            if try_unequip == "bag_full":
                return
            else:
                player.current_equips[slot] = 'bare'
        else:
            print('You have nothing equipped in the {} slot'.format(slot))


    def add_move(self, new_move):
        if new_move in supported_moves:
            if not new_move in player.unlocked_moves:
                player.unlocked_moves[new_move] = {}
                player.unlocked_moves[new_move]['type'] = supported_moves[new_move]['type']
            else:
                return "already_unlocked"
        else:
            print("Error: unknown move: {}".format(new_move.__name__))

    awareness_levels = {95: "paranoid", 90: "on guard", 80: "alert",\
    60: "drowsy", 30: "distracted", 20: "panicking"}

    def awareness_level(self, custom_awareness = None, list_position = False):
        if list_position == True:
            return self.awareness_hierarchy.index(min(list(self.awareness_levels.keys()), key=lambda x:abs(x - self.awareness)))
        if custom_awareness == None:
            return self.awareness_levels[min(list(self.awareness_levels.keys()), key=lambda x:abs(x - self.awareness))]
        else:
            return self.awareness_levels[min(list(self.awareness_levels.keys()), key=lambda x:abs(x - custom_awareness))]

    awareness_hierarchy = [20, 30, 60, 80, 90, 95]

    def new_awareness(self, change, amount = 0):
        if change == "increase":
            if amount != 0:
                temp_awareness = player.awareness
                if temp_awareness > len(self.awareness_hierarchy):
                    return
                else:
                    if temp_awareness + amount > len(self.awareness_hierarchy):
                        self.awareness = self.awareness_hierarchy[self.awareness_level(list_position = True) + amount]
                    else:
                        return
            else:
                try:
                    self.awareness = self.awareness_hierarchy[self.awareness_level(list_position = True) + 1]
                except IndexError:
                    return
        elif change == "decrease":
            if amount != 0:
                temp_awareness = player.awareness
                if temp_awareness - amount < 0:
                    return
                else:
                    self.awareness = self.awareness_hierarchy[self.awareness_level(list_position = True) - amount]
            else:
                try:
                    self.awareness = self.awareness_hierarchy[self.awareness_level(list_position = True) - 1]
                except IndexError:
                    return
        elif change == "specific":
            if amount != 0:
                self.awareness = amount
            else:
                print("Error: Unspecified new awareness")
        else:
            print("Error: Unknown change type at awareness")


    speed_levels = {90: "fast as fuck boiii", 80: "fast", 70: "fleet",\
    40: "tired", 30: "sluggish", 20: "injured"}

    speed_hierarchy = [90, 80, 70, 40, 30, 20]

    def speed_level(self, custom_speed = None, list_position = False):
        if list_position == True:
            return self.speed_hierarchy.index(min(list(self.speed_levels.keys()), key=lambda x:abs(x - self.speed)))
        if custom_speed == None:
            return self.speed_levels[min(list(self.speed_levels.keys()), key=lambda x:abs(x - self.speed))]
        else:
            return self.speed_levels[min(list(self.speed_levels.keys()), key=lambda x:abs(x - custom_speed))]

    def new_speed(self, change, amount = 0):
        if change == "increase":
            if amount != 0:
                temp_speed = player.speed
                while temp_speed == player.speed:
                    if temp_speed > len(speed_hierarchy):
                        return
                    else:
                        self.speed = self.speed_hierarchy[self.speed_level(list_position = True) + amount]
            else:
                try:
                    self.speed = self.speed_hierarchy[self.awareness_level(list_position = True) + 1]
                except:
                    return
        elif change == "decrease":
            if amount != 0:
                temp_speed = player.speed
                while temp_speed == player.speed:
                    try:
                        self.speed = self.speed_hierarchy[self.speed(list_position) - amount]
                    except:
                        amount += 1
            else:
                try:
                    self.speed = self.speed_hierarchy[self.speed(list_position) - 1]
                except:
                    return
        elif change == "specific":
            if amount != 0:
                self.speed = amount
            else:
                print("Error: Unspecified new speed")
        else:
            print("Error: Unknown change type at speed")

    def state(self):
        if not len(self.statuses) == 0:
            effect_descriptions = []
            for effect in self.statuses:
                effect_descriptions.append(supported_statuses[effect]['description'])

            effect_string = ""
            for effect in effect_descriptions:
                if effect_descriptions.index(effect) == (len(effect_descriptions) - 2):
                    effect_string = effect_string + effect + " "
                elif effect_descriptions.index(effect) == (len(effect_descriptions) - 1):
                    if not len(effect_string) == 0:
                        effect_string = effect_string + "and " + effect + "."
                    else:
                        effect_string = effect_string + effect + "."
                else:
                    effect_string = effect_string + effect + ", "

            current_states = "You are " + effect_string
        else:
            current_states = ""

        temp_speed = player.speed
        temp_awareness = player.awareness
        temp_strength = self.strength
        #last

        return "You have {}/{} hp.\nYour current strength is {}\nYou are currently {} and {}.\n{}"\
        .format(self.current_hp, self.max_hp, self.strength,\
        self.awareness_level(temp_awareness), self.speed_level(temp_speed), current_states)

class Enemy(Character):
    statuses = {}
    def __init__(self, current_hp, max_hp, strength, name, description, speed, *args):
        if speed == "fast":
            speed = 80
        elif speed == "fleet":
            speed = 70
        elif speed == "tired":
            speed = 40
        elif speed == "sluggish":
            speed = 30
        elif speed == "injured":
            speed = 20
        else:
            print("Error: unknown speed on enemy")

        self.current_hp = current_hp
        self.max_hp = max_hp
        self.strength = strength
        self.name = name
        self.description = description
        self.speed = speed
        self.drops = []
        for item in args:
            self.drops.append(item)

    def inspect(self):
        print(self.description)
        print('It has {}/{} hp and {} strength'.format(self.current_hp, self.max_hp, self.strength))




class Orc(Enemy):
    resistances = {
        statuses.apply_on_fire: 0,
        statuses.apply_blead: 0,
        statuses.apply_weak: 0,
    }


class Animal(Enemy):
    resistances = {
        statuses.apply_on_fire: 0,
        statuses.apply_blead: 0,
        statuses.apply_weak: 0,
    }


class Human(Enemy):
    resistances = {
        statuses.apply_on_fire: 0,
        statuses.apply_blead: 0,
        statuses.apply_weak: 0,
    }

class Skeleton(Enemy):
    resistances = {
        statuses.apply_on_fire: 0,
        statuses.apply_blead: 0,
        statuses.apply_weak: 0,
    }






def main_menu():
    while True:
        game_name = "GrötQuest"
        console_spaces_center_name = 60 - int(len(game_name)/2)
        #Dramatic sort of startup animation
        for i in range(5, -1, -1):
            Console.clear()
            print("\n" * i + " " * console_spaces_center_name + game_name)
            time.sleep(0.2)
        for i in range(console_spaces_center_name, -1, -1):
            Console.clear()
            print(" " * i + game_name)
            time.sleep(0.03)

        time.sleep(0.2)
        Console.clear()
        print("Welcome to {}".format(game_name))
        time.sleep(2)


def combat(enemy, location):
    print("{} approaches!".format(enemy.name))
    def player_turn():
        print("player")
        for status in list(player.statuses):
            player.statuses[status] -= 1
            if player.statuses[status] <= 0:
                del player.statuses[status]

        for effect in player.statuses:
            if supported_statuses[effect]['apply_type'] == "start_dot":
                damage = effect(player)
                GameMaster.action_log.append("{} {} damage.You have {} hp left".format\
                (supported_statuses[effect]['on_apply_message_player'], damage, player.current_hp))
                GameMaster.last_damage_player = supported_statuses[effect]['type']
                player.alivecheck()

        def main_choice():

            def execute_move(move_type,):
                moves = []
                for move in player.unlocked_moves:
                    if player.unlocked_moves[move]['type'] == move_type:
                        moves.append(move)
                if len(moves) == 0:
                    while True:
                        Console.combat_screen('Type continue when you are ready', enemy, "You Do not Have any Heal Moves Yet. Please Try Something Else")
                        next = input(">>> ")
                        if next.lower() == "continue":
                            break
                else:
                    pretty_moves = []
                    for move in moves:
                        pretty_string_split = move.__name__.split("_")
                        pretty_string_joined = " ".join(pretty_string_split)
                        pretty_moves.append(pretty_string_joined)

                    string_out = "Which move do you want to use?\nAviable moves:"
                    for move in pretty_moves:
                        string_out = string_out + "\n*" + move


                    while True:
                        Console.combat_screen('Now, which one will you use?', enemy, string_out)
                        print(pretty_moves)
                        move_used = input(">>> ")
                        if move_used in pretty_moves:
                            print(player.awareness)
                            print(player.awareness_level())
                            result = moves[pretty_moves.index(move_used)](player)
                            GameMaster.action_log.append(result)
                            return True

                        elif move_used == "back":
                            return False


            Console.clear()
            supported_head_moves = ['defend', 'heal', 'attack', 'debuff', 'buff', 'use item', 'inspect', 'help']
            while True:
                Console.combat_screen("What do you want to do?", enemy,\
                "What Action Do You Want To Perform?\n*Attack\n*Defend\n*Heal\n*debuff\n*buff\n*Use item\n*Inspect\n*Help")
                action = input(">>> ")

                action = action.lower()
                if action in supported_head_moves or action[:4] == "help" or action[:7] == "inspect":
                    if action == "heal":
                        break_main = execute_move("heal")
                        if break_main == True:
                            break

                        """
                        heal_moves = []
                        for move in player.unlocked_moves:
                            if player.unlocked_moves[move]['type'] == "heal":
                                heal_moves.append(move)
                        if not len(heal_moves) == 0:
                            Console.clear()

                            pretty_heal_moves = []
                            for move in heal_moves:
                                pretty_string_splitted = move.__name__.split("_")
                                pretty_string_joined = " ".join(pretty_string_splitted)
                                pretty_heal_moves.append(pretty_string_joined)

                            string_out = "Which move do you want to use?\nAviable moves:"
                            for move in pretty_heal_moves:
                                string_out = string_out + "\n*" + move

                            while True:
                                Console.combat_screen('Now, which one will you use?', enemy, string_out)
                                move_used = input(">>> ")
                                if move_used in pretty_heal_moves:
                                    result = heal_moves[pretty_heal_moves.index(move_used)](player)
                                    GameMaster.action_log.append(result)
                                    player.state()
                                    break_main = True
                                    break
                                elif move_used == "back":
                                    break_main = False
                                    break
                            if break_main == True:
                                break
                        else:
                            Console.clear()
                            main_choice("Sorry, You Do not Have any Heal Moves Yet. Please Try Something Else")
                            """
                    elif action == "defend":
                        pass
                    elif action == "attack":
                        pass
                    elif action == "debuff":
                        pass
                    elif action == "use item":
                        pass
                    elif action == "buff":
                        pass
                    elif action == "inspect" or action[:7] == "inspect":
                        if len(action) == 7:
                            action = "help inspect"
                        else:
                            to_inspect = action[7:len(action)]
                            #last

                            if to_inspect == "self":
                                Console.combat_screen("Type continue when you are ready",enemy,player.state())
                                while True:
                                    next = input(">>> ")
                                    if next.lower() == "continue":
                                        break



                    if action == "help" or action[:4] == "help":
                        if len(action) == 4:
                            Console.combat_screen("Type continue when you are ready",enemy,\
                            'Syntax for help:\n"help {}" where {} is a status, effect, item or anything\nIt can also be a type, example help statuses\nIt can be typed straight into the main combat menu\nExample: help on fire')
                            while True:
                                next = input(">>> ")
                                if next.lower() == "continue":
                                    break
                        else:
                            help_with = action[5:len(action)]

                            help_options = {
                                #commands
                                'inspect': {'description': 'Syntax for inspect:\n"inspect {}" where {} can be the current enemy, self or an item in your inventory\nExample: "inspect feather"\nIt is supposed to bo typed "straight" into the main menu', 'type': 'moves'},
                                #statuses
                                'on fire': {'description': 'On fire: Sets your awareness to panicking and deals damage equal to 10% of the targets current hp.', 'type': 'statuses'},
                                'weak': {'description': 'Weak: Deals damage equal to 15% of the targets current hp', 'type': 'statuses'},
                            }
                            help_heads = ['moves', 'statuses', 'sword enchantments']
                            if help_with in help_options:
                                while True:
                                    Console.combat_screen\
                                    ('Type continue when you are ready', enemy, help_options[help_with]['description'])
                                    next = input(">>> ")
                                    if next.lower() == "continue":
                                        break

                            elif help_with == "categories":
                                help_string = ""
                                for head in help_heads:
                                    help_string = help_string + head + "\n"
                                while True:
                                    Console.combat_screen('Type continue when you are ready', enemy, help_string)
                                    next = input(">>> ")
                                    if next.lower() == "continue":
                                        break

                            elif help_with in help_heads:
                                help_string = ""
                                for effect in help_options:
                                    if help_options[effect]['type'] == help_with:
                                        help_string = help_string + help_options\
                                        [effect]['description'] + "\n"

                                while True:
                                    Console.combat_screen\
                                    ('Type continue when you are ready', enemy, help_string)
                                    next = input(">>> ")
                                    if next.lower() == "continue":
                                        break
                else:
                    print("Sorry, i didn't quite get that. Please try again")
        main_choice()
    def enemy_turn():
        print("enemy")
        print("\n")

    while True:
        if (player.awareness * 100) >= random.randint(0, 100):
            player_first = True
        else:
            player_first = False
        while True:
            if player_first == True:
                player_turn()
                enemy_turn()
            else:
                enemy_turn()
                player_turn()

            temp_player_speed = int((player.speed))
            temp_enemy_speed = int((enemy.speed))

            for effect in player.statuses:
                if supported_statuses[effect]['apply_type'] == 'weaker_speed':
                    temp_player_speed = effect(temp_player_speed)

            for effect in enemy.statuses:
                if supported_statuses[effect]['apply_type'] == 'weaker_speed':
                    temp_enemy_speed = effect(temp_enemy_speed)

            if random.randint(random.randint(int((temp_player_speed / 3)), (temp_player_speed - 10)), temp_player_speed * 2) >= \
            random.randint(random.randint(int((temp_enemy_speed / 3)), (temp_enemy_speed - 10)), temp_enemy_speed * 2):
                player_first = True
            else:
                player_first = False
            time.sleep(2)

player = Player()
hen = Enemy(5, 5, 50, 'Gullbert the hen', 'A hen', 'tired', "feather", "radish")
player.add_move(moves.calming_heal)
player.add_move(moves.intense_heal)
hen.dealdmg(hen, player, 10)
player.apply_effect(statuses.apply_frozen, 10)


combat(hen, "swamp")


