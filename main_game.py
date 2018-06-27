# Better drop system
# Fix back windows 10
import pickle
import random
import time
import os
import win32gui
import pynput
import sys
import ctypes
import colorama
import logging
import json


def closest_match(value, array):
    # Returns the closest matching integer to the passed value in an array of integers
    if isinstance(array, dict):
        return min(list(array.keys()), key=lambda x: abs(x - value))
    else:
        return min(array, key=lambda x: abs(x - value))


def isint(variable_to_test):
    # Returns a bool representing if the entered variable is an int or not
    try:
        variable_to_test = int(variable_to_test)
        variable_to_test += 1
        return True
    except ValueError:
        return False


class Console:
    # A class for collecting all methods related to the console
    @staticmethod
    def clear():
        # Removes all written characters in the console
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def console_location_reset():
        # Sets the console to a specific location and resizes it
        hwnd = win32gui.GetForegroundWindow()
        win32gui.MoveWindow(hwnd, GameMaster.console_location_x, GameMaster.console_location_y,
                            GameMaster.console_height_x, GameMaster.console_height_y, True)
        os.system("mode con cols=120 lines=30")

    @staticmethod
    def print_with_layout(extra_text=None, battle=False):
        # Method for printing text along with other things, for example a healthbar
        # "Other things" will remain at the same location, even if there's other text in the same line
        # If battle is true, enemy must also be supplied
        # If battle is true, a healthbar for the player and enemy will be printed along with an action log
        Console.clear()
        if extra_text is not None:
            # Splitting input into a list
            lines_in = extra_text.split("\n")
        else:
            lines_in = []

        # Filling up so that the list will contain 30 entries
        # This is to ensure that even if less than 30 lines of input is entered, the code will not cause an exception
        for i in range(len(lines_in), 31):
            lines_in.append("")

        # Adding the lines to be printed
        # If input was entered, it will contain that input to be printed, otherwise it will contain an empty string
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
        line_11 = lines_in[10]
        line_12 = lines_in[11]
        line_13 = lines_in[12]
        line_14 = lines_in[13]
        line_15 = lines_in[14]
        line_16 = lines_in[15]
        line_17 = lines_in[16]
        line_18 = lines_in[17]
        line_19 = lines_in[18]
        line_20 = lines_in[19]
        line_21 = lines_in[20]
        line_22 = lines_in[21]
        line_23 = lines_in[22]
        line_24 = lines_in[23]
        line_25 = lines_in[24]
        line_26 = lines_in[25]
        line_27 = lines_in[26]
        line_28 = lines_in[27]
        line_29 = lines_in[28]

        # Declaring ASCII characters for the healthbars and the action log
        standing_line = chr(124)
        block = chr(9608)
        top_line = chr(175)

        # Checking if we want the battle layout
        if battle:
            # The spacings used for the healthbars and the log, from left to right
            player_healthbar_spacing = 30
            enemy_healthbar_spacing = 80
            overlapping_action_log_spacing_special = 30
            overlapping_action_log_spacing = 22
            normal_action_log_spacing = overlapping_action_log_spacing + 30

            # Declaring the healthbars and actions logs
            # This is done in such a way that they will remain at a static position in the console
            player_bot_healthbar = ' ' * (player_healthbar_spacing - len(line_24)) + " " + top_line * 10
            enemy_bot_healthbar = ' ' * (enemy_healthbar_spacing - len(line_8)) + " " + top_line * 10

            player_top_healthbar = ' ' * (player_healthbar_spacing - len(line_22)) + " " + "_" * 10 + player.name
            if line_6 == '*{}buff{}'.format(colorama.Fore.LIGHTCYAN_EX, colorama.Fore.RESET):
                enemy_top_healthbar = (' ' * (enemy_healthbar_spacing - len(line_6) + 10)
                                       + " " + "_" * 10 + player.current_enemy.name)
            else:
                enemy_top_healthbar = (' ' * (enemy_healthbar_spacing - len(line_6))
                                       + " " + "_" * 10 + player.current_enemy.name)

            player_hp = int((player.current_hp / player.max_hp) * 10)
            enemy_hp = int((player.current_enemy.current_hp / player.current_enemy.max_hp) * 10)

            player_mid_healthbar = (' ' * (player_healthbar_spacing - len(line_23)) + standing_line + block * player_hp
                                    + " " * (10 - player_hp) + standing_line +
                                    "{}/{} hp".format(player.current_hp, player.max_hp))

            enemy_mid_healthbar = (' ' * (enemy_healthbar_spacing - len(line_7)) + standing_line +
                                   block * enemy_hp + " " * (10 - enemy_hp) + standing_line +
                                   '{}/{} hp'.format(player.current_enemy.current_hp, player.current_enemy.max_hp))

            log_lines = 4
            max_spacing = max(
                list(len(GameMaster.action_log[len(GameMaster.action_log) - (i + 1)]) for i in range(log_lines)))
            spacing_1 = " " * (max_spacing - len(GameMaster.action_log[len(GameMaster.action_log) - 1]))
            spacing_2 = " " * (max_spacing - len(GameMaster.action_log[len(GameMaster.action_log) - 2]))
            spacing_3 = " " * (max_spacing - len(GameMaster.action_log[len(GameMaster.action_log) - 3]))
            spacing_4 = " " * (max_spacing - len(GameMaster.action_log[len(GameMaster.action_log) - 4]))

            action_log_mid_1 = (' ' * (overlapping_action_log_spacing - (len(player_mid_healthbar)) +
                                       (overlapping_action_log_spacing_special - len(line_23)))
                                + standing_line +
                                GameMaster.action_log[len(GameMaster.action_log) - 1]
                                + spacing_1 + standing_line)

            action_log_mid_2 = (' ' * (overlapping_action_log_spacing - len(player_bot_healthbar) +
                                       (overlapping_action_log_spacing_special - len(line_24)))
                                + standing_line +
                                GameMaster.action_log[len(GameMaster.action_log) - 2]
                                + spacing_2 + standing_line)

            action_log_mid_3 = (' ' * (normal_action_log_spacing - len(line_25)) + standing_line +
                                GameMaster.action_log[len(GameMaster.action_log) - 3]
                                + spacing_3 + standing_line)

            action_log_mid_4 = (' ' * (normal_action_log_spacing - len(line_26)) + standing_line +
                                GameMaster.action_log[len(GameMaster.action_log) - 4]
                                + spacing_4 + standing_line)

            action_log_top = (' ' * (overlapping_action_log_spacing - len(player_top_healthbar) +
                                     (overlapping_action_log_spacing_special - len(line_22))) + " " +
                              "_" * max_spacing + "Action log")

            action_log_bot = (" " + ' ' * (normal_action_log_spacing - len(line_27)) + top_line * max_spacing)

        # If we don't want the battle layout, the healthbars and the log will instead be empty strings
        else:
            enemy_top_healthbar = ""
            enemy_mid_healthbar = ""
            enemy_bot_healthbar = ""
            player_mid_healthbar = ""
            player_top_healthbar = ""
            player_bot_healthbar = ""
            action_log_top = ""
            action_log_bot = ""
            action_log_mid_1 = ""
            action_log_mid_2 = ""
            action_log_mid_3 = ""
            action_log_mid_4 = ""

        # Joining all the strings to be printed
        lines = {0: line_1, 1: line_2, 2: line_3, 3: line_4, 4: line_5,
                 5: line_6 + enemy_top_healthbar,
                 6: line_7 + enemy_mid_healthbar,
                 7: line_8 + enemy_bot_healthbar,
                 8: line_9, 9: line_10, 10: line_11, 11: line_12, 12: line_13,
                 13: line_14, 14: line_15, 15: line_16, 16: line_17, 17: line_18,
                 18: line_19, 19: line_20, 20: line_21,
                 21: line_22 + player_top_healthbar + action_log_top,
                 22: line_23 + player_mid_healthbar + action_log_mid_1,
                 23: line_24 + player_bot_healthbar + action_log_mid_2,
                 24: line_25 + action_log_mid_3,
                 25: line_26 + action_log_mid_4,
                 26: line_27 + action_log_bot,
                 27: line_28, 28: line_29}

        # Printing the strings
        for i in range(0, 29):
            print(lines[i])

    @staticmethod
    def interactive_choice(cases: list, head_string: str, back_want: bool = False,
                           battle: bool = False, enumerated: bool = False):
        # This method makes use of the print_with_layout method in order to make some printed objects clickable
        # Cases is a list of the clickable strings
        # Head_string will be printed at the top of the console and will not be clickable
        # If battle is True, an enemy must be supplied and print_with_layout will use the battle layout
        # If back_want is True, a back option will be added
        # Returns the name of the string clicked(or None, signaling that back was clicked)
        def move_to_string():
            # Formatting the string to be printed
            string_output = head_string
            for action in cases:
                string_output = string_output + "\n*" + action

            return string_output

        # Information about the console to be used during text area calculations
        Console.console_location_reset()

        # Console borders need to be accounted for
        console_x_border: int = GameMaster.x_to_console  # pixels
        console_y_border = GameMaster.y_to_console  # pixels
        font_size_x = GameMaster.font_size_x  # pixels
        font_size_y = GameMaster.font_size_y  # pixels

        # Some lines are not clickable
        uninteractive_lines = head_string.count("\n") + 1

        # Adding a back option if desired
        if back_want and "back" not in cases:
            cases.append("back")

        # Formatting the string to be printed
        string_out = move_to_string()

        # Battle layout or not
        if battle:
            Console.print_with_layout(extra_text=string_out, battle=True)
        else:
            Console.print_with_layout(extra_text=string_out)

        # Calculating the areas which are clickable
        # First two x values, then two y values in the dict
        line_areas = []
        for i in range(0, 31):
            line_areas.append([])
        for move in cases:
            line_areas[cases.index(move)].append(console_x_border)
            line_areas[cases.index(move)].append(len(move) * font_size_x + console_x_border)

            line_areas[cases.index(move)].append(console_y_border + font_size_y * uninteractive_lines)
            line_areas[cases.index(move)].append((cases.index(move) + 1) * font_size_y
                                                 + console_y_border + font_size_y * uninteractive_lines)
        # Removing empty nested lists
        line_areas = [x for x in line_areas if x != []]

        def on_click(x, y, button, pressed):
            # Checking whether a left click is performed
            if pressed and button == pynput.mouse.Button.left:
                for x_y in line_areas:
                    # Checking if the mouse input is within the desired area
                    if x in range(line_areas[line_areas.index(x_y)][0],
                                  line_areas[line_areas.index(x_y)][1]) and \
                            y in range(line_areas[line_areas.index(x_y)][2],
                                       line_areas[line_areas.index(x_y)][3]):
                        # For the listener to exit, we need to return false
                        # Therefore, in order to return other values, we use a global variable
                        global case
                        case = cases[line_areas.index(x_y)]
                        return False

        # Checks for mouse clicks, if there are any it calls on_click
        with pynput.mouse.Listener(on_click=on_click) as listener:
            listener.join()

        if case == "back":
            # If the input is back, return None
            return None
        else:
            # If a clickable case was clicked, return which one
            # If enumerated is true, we return the index of the case
            if enumerated:
                return cases.index(case)
            else:
                return case


class Statuses:
    # A collection class of all the statuses a character can have
    @staticmethod
    def apply_on_fire(target):
        # Applies DOT damage at the start of a turn and makes the target panic (lower awareness)
        damage_taken = (int((target.current_hp * 0.1)))
        if target == player:
            player.new_awareness('specific', 20)
        return damage_taken

    @staticmethod
    def apply_frozen(original_speed):
        # Decreases the target's speed during turn calculations
        slowed_speed = (int(original_speed * 0.5))
        return slowed_speed

    @staticmethod
    def apply_weak(original_damage):
        # Decreases an incoming attack's damage
        weakened_damage = int(original_damage * 0.5)
        return weakened_damage

    @staticmethod
    def apply_bleed(target):
        # Applies DOT damage at the start of a turn
        damage_taken = (int(target.max_hp * 0.15))
        return damage_taken


supported_Statuses = {
    # Information about the previous class's statuses
    # head_type sorting whether it's a positive or negative effect.
    # head_type is also used in curses, effects that don't go away by simply playing
    # apply_type is used to determine when during combat the effect takes effect
    # type doesn't serve any purpose at the moment
    # description is used when inspecting someone who is afflicted
    # on_apply_message_player and enemy are to be used in the action log
    Statuses.apply_on_fire:
        {
            'head_type': 'debuff',
            'apply_type': 'start_dot', 'type': 'fire',
            'description': 'on fire',
            'on_apply_message_player': 'Hot! You panic and take',
            'on_apply_message_enemy': 'Hot! '
        },
    Statuses.apply_frozen:
        {
            'head_type': 'debuff',
            'apply_type': 'weaker_speed', 'type': 'ice',
            'description': 'frozen',
            'on_apply_message_player': '',
            'on_apply_message_enemy': ''
        },
    Statuses.apply_bleed:
        {
            'head_type': 'debuff',
            'apply_type': 'start_dot', 'type': 'bleeding',
            'description': 'bleeding',
            'on_apply_message_player': 'You better stop this bleeding soon... You take',
            'on_apply_message_enemy': 'Blood spills forth as the enemy takes'
        },
    Statuses.apply_weak:
        {
            'head_type': 'debuff',
            'apply_type': 'weaker_damage', 'type': None,
            'description': 'weak',
            'help': 'Halves the damage of the targets incoming attacks',
            'on_apply_message_player': 'Your attacked is weakend and deals',
            'on_apply_message_enemy': "The enemy's attack is weakened and deals"
        }

}


class Moves:
    # A collection of all possible moves
    # The general blueprint is:
    # does an action based on why made the move (caster)
    # creates a string to add to the action log and returns it
    @staticmethod
    def calming_heal(caster):
        amount_healed = int((caster.current_hp / 5) + (caster.max_hp / 10))
        caster.current_hp += amount_healed
        if caster.current_hp >= caster.max_hp:
            caster.current_hp = caster.max_hp
        if caster == player:
            player.new_awareness('increase', 1)
            return "You heal for {} hp and feel a bit calmer".format(amount_healed)
        else:
            return "The enemy heals for {} hp".format(amount_healed)

    @staticmethod
    def intense_heal(caster):
        amount_healed = int((caster.current_hp / 3) + (caster.max_hp / 4))
        caster.current_hp += amount_healed
        if caster.current_hp >= caster.max_hp:
            caster.current_hp = caster.max_hp
        if caster == player:
            return "You heal for {} hp".format(amount_healed)
        else:
            return "The enemy heals for {} hp".format(amount_healed)


supported_moves = {
    Moves.calming_heal:
        {
            'type': 'heal',
        },
    Moves.intense_heal:
        {
            'type': 'heal',
        }

}


class ArmorEffect:
    # Effects that are tied to armors

    @staticmethod
    def change_stat(stat: int, change_amount: int, effect_level: int, effect_description: str):
        # change_type specifies if the stat parameter is to be increased or decreased
        # The stat is then changed according to change_amount * effect_level
        # Change amount is negative if we want to perform a reduction
        # Effect_level is increased by 1 for each item in that is in the same set worn by6 the player
        # effect_description is then added to the action log to inform the player that a set bonus has kicked in
        GameMaster.action_log.append(effect_description)
        if effect_level < 3:
            stat += change_amount * effect_level
            if stat >= 0:
                return stat
            else:
                return 0
        else:
            # If effect_level is 3 (the whole set is worn), the set bonus becomes more powerful
            stat += change_amount * (effect_level + 2)
            return 0


class WeaponEffect:
    pass


class Item:
    """ name -- the name of the item
        weight -- the item's weight
        value -- the item's raw value, not accounting for merchant rates etc
        item_type -- determines its uses, i.e. weapon, material, consumable
        description -- the item's flavor text
        rarity -- the rate at which the item is dropped
    """

    def __init__(self, name: str, weight: int, value: int, item_type: str, item_id: int, description: str, rarity: int,
                 max_stack: int):
        self.rarity = rarity
        self.name = name
        self.weight = weight
        self.value = value
        self.item_type = item_type
        self.item_id = item_id
        self.description = description
        self.max_stack = max_stack

    # Keep in mind that this is far from optimal
    # The code below returns a string containing the closest match to the item's rarity
    # The data structures are for making the method rarity_level work
    #
    # It works by having a 'hierarchy' of rarities and a dictionary of keys being the same values as the hierarchy
    # The function takes the item's rarity, finds its closest match in the hierarchy
    # It then returns a string according to its level in the hierarchy from the dictionary
    rarity_levels = {75: 'extremely common', 40: "very common", 20: "common", 10: "uncommon",
                     5: "rare", 2: "legendary"}

    rarity_hierarchy = (2, 5, 10, 20, 40, 75)

    def rarity_level(self):
        return Item.rarity_levels[closest_match(self.rarity, Item.rarity_hierarchy)]

    # Displaying information about the item when inspected
    def inspect(self):
        # Checking whether to use "a" or "an"
        if str(self.item_type)[0] in GameMaster.vowels:
            a_or_an = "an"
        else:
            a_or_an = "a"

        # Instead of "it weighs 0", it becomes "it weighs nothing"
        weight = self.weight
        if weight == 0:
            weight = "nothing"
        # Some flavor texts contains quest marks or exclamation marks at the end
        # We do not want (flavor text)?. hence, we do the following operation
        temp_description = self.description
        sentence_endings = ('!', '?', '.')
        if not temp_description[-1] in sentence_endings:
            temp_description = temp_description + "."

        # Concatenating it all together
        return ("{}\nIt is worth {} gold and weighs {}.\nIt is {} {} that is {}".format
                (temp_description, self.value, weight, a_or_an, self.item_type, Item.rarity_level(self)))


class Wearable(Item):
    # This class exists only for the wearable class to inherit the inspect method
    #
    """ Name: The armor's name
        Weight: The armor's weight
        Value: The armor's value
        item_type: Should always be armor
        item_id: The id of the item
        Description: The item's flavor text
        Rarity: The rate at which the item will be dropped
        Armor_weight: The weight of the armor
        Defense: How much damage the armor will defend against
        Armor_effect: A special effect bound to the armor
        Set_member: What armor set the armor is part of (used for set bonuses)
    """
    effect_inspect_text = "Error: no inspection text"

    # noinspection PyMethodOverriding
    def inspect(self):
        # noinspection PyUnresolvedReferences
        return Item.inspect(self) + "\n{}".format(self.parent.effect_inspect_text)


class Weapon(Item):
    def __init__(self, name, weight, value, item_type, item_id, description, rarity, max_stack,
                 weapon_damage, special_effect=None, effect_rate=0):
        super().__init__(name, weight, value, item_type, item_id, description, rarity, max_stack)
        self.weapon_damage = weapon_damage
        if not effect_rate:
            self.special_effect = special_effect
            self.effect_rate = effect_rate

    likeliness_levels = {80: "very likely", 60: "likely", 40: "unlikely",
                         20: "very unlikely"}

    likeliness_hierarchy = (20, 40, 60, 80)

    def likeliness_level(self):
        return self.likeliness_levels[closest_match(self.effect_rate, self.likeliness_hierarchy)]

    def inspect(self):
        if str(self.item_type)[0] in GameMaster.vowels:
            a_or_an = "an"
        else:
            a_or_an = "a"
        if hasattr(Wearable, self.special_effect):
            special_effect_text = (". {} and {} affect the enemy".format
                                   (weapon_effects[self.special_effect]['description'],
                                    self.likeliness_level()))
        else:
            special_effect_text = ""

        return ("{}.It is worth {} gold and weighs {}. It is {} {} that is {}{}".format
                (self.description, self.value, self.weight, a_or_an, self.item_type, self.rarity_level(),
                 special_effect_text))

    def get_id(self):
        return self.item_id


# feather = Item('feather', 1, 10, 'material', 1, 'A feather from a hen', 'common')
# radish = Item('radish', 1, 20, 'food', 2, 'Fresh from The earth!', 'uncommon')
#
# feather.inspect()
# b = Wearable()
class Bare(Wearable):
    item_id = 1

    set_effect_description_good = 'People are astonished by your amazing body, increasing your speech by '
    set_effect_description_bad = "People won't trust you, running around without clothes, decreasing your speech by "
    set_effect = ArmorEffect.change_stat

    effect_inspect_text = "If you're weak and naked, no one will trust you, making negotiating harder.\n" \
                          "However, if you're buff, people will be amazed, making negotiating easier"

    change_type = "speech"
    inspect_flavor_text = 'Get some real clothes, you hobo'

    class Head:
        def __init__(self, parent):
            self.parent = parent

        set_part = "head"
        description = "Just a plain old ugly head"
        item_type = "wearable"
        name = "Bare"
        weight = 0
        value = 'unsellable'
        rarity = 'unobtainable'
        defense = 1
        description_good = 'Even though your face looks terrible, people are distracted by your glorious body,'
        effect_amount_good = 0
        description_bad = 'Your face looks terrible, it will make negotiating harder'
        effect_amount_bad = -2

    class Chest:
        def __init__(self, parent):
            self.parent = parent

        set_part = "chest"
        description = "Just a plain old torso"
        item_type = "wearable"
        name = "Bare"
        weight = 0
        value = 'unsellable'
        rarity = 'unobtainable'
        defense = 3
        description_good = 'Nice gains, bro'
        effect_amount_good = 4
        description_bad = 'You even lift, bro?'
        effect_amount_bad = -1

    class Legs:
        def __init__(self, parent):
            self.parent = parent

        set_part = "legs"
        description = "What humans use to walk"
        item_type = "wearable"
        name = "Bare"
        weight = 0
        value = 'unsellable'
        rarity = 'unobtainable'
        defense = 2
        description_good = 'Not wearing pants only seems to be in your flavor with such a body'
        effect_amount_good = 1
        description_bad = 'Oh please, at least put some pants on'
        effect_amount_bad = -7

    @staticmethod
    def get_set_part_description(set_part, user) -> str:
        if user.strength > 50:
            return set_part.description_good
        else:
            return set_part.description_bad

    @staticmethod
    def get_set_effect(user, head: bool = False, chest: bool = False, legs: bool = False):
        change_amount = 0
        if user.strength > 50:
            if head:
                change_amount += Bare.Head.effect_amount_good
            if chest:
                change_amount += Bare.Chest.effect_amount_good
            if legs:
                change_amount += Bare.Legs.effect_amount_good
            return "speech", change_amount, Bare.set_effect_description_good
        else:
            if head:
                change_amount -= Bare.Head.effect_amount_bad
            if chest:
                change_amount -= Bare.Chest.effect_amount_bad
            if legs:
                change_amount -= Bare.Legs.effect_amount_bad
            return "speech", change_amount, Bare.set_effect_description_bad


Bare.Head = Bare.Head(Bare)
Bare.Chest = Bare.Chest(Bare)
Bare.Legs = Bare.Legs(Bare)


class Leaves(Wearable):
    item_id = 2

    set_effect_description_good = "People are happy that you're hiding at least a little of your weak body, " \
                                  "increasing your speech by "
    set_effect_description_bad = "People are disappointed that you're hiding your glorious body, decreasing " \
                                 "your speech by "
    set_effect = ArmorEffect.change_stat
    effect_inspect_text = "If you're weak, people will respect you for hiding your weak body, increasing your " \
                          "speech\nHowever, if you're buff, people will become angry for not showing yourself," \
                          " decreasing your speech"
    change_type = "speech"
    inspect_flavor_text = 'Mother nature to the rescue!'

    class Head:
        def __init__(self, parent):
            self.parent = parent

        set_part = "head"
        description = "A pretty leaf crown"
        item_type = "wearable"
        name = "leaf crown"
        weight = 0
        value = 2
        rarity = 3
        defense = 2
        description_good = 'Your leaf crown actually hides your horrible face pretty well'
        effect_amount_good = 1
        description_bad = "People don't really mind your face since your body is so muscular"
        effect_amount_bad = -0

    class Chest:
        def __init__(self, parent):
            self.parent = parent

        set_part = "chest"
        description = "A well-made leaf chestmail"
        item_type = "wearable"
        name = "leaf chestmail"
        weight = 0
        value = 4
        rarity = 3
        defense = 2
        description_good = 'This finely crafted leaf chestmail hides your weak chest perfectly'
        effect_amount_good = 2
        description_bad = 'Why hide your amazing chest?'
        effect_amount_bad = -4

    class Legs:
        def __init__(self, parent):
            self.parent = parent

        set_part = "legs"
        description = "Just some leafs to cover the private parts. The leggings part was a lie"
        item_type = "wearable"
        name = "leaf leggings"
        weight = 0
        value = 3
        rarity_level = 3
        defense = 2
        description_good = 'People are looking happy that you at least covered up your private parts'
        effect_amount_good = 4
        description_bad = 'People look angry that you hide your amazing body'
        effect_amount_bad = -2

    @staticmethod
    def get_set_part_description(set_part, user) -> str:
        if user.strength < 50:
            return set_part.description_good
        else:
            return set_part.description_bad

    @staticmethod
    def get_set_effect(user, head: bool = False, chest: bool = False, legs: bool = False):
        change_amount = 0
        if user.strength < 50:
            if head:
                change_amount += Leaves.Head.effect_amount_good
            if chest:
                change_amount += Leaves.Chest.effect_amount_good
            if legs:
                change_amount += Leaves.Legs.effect_amount_good
            return "speech", change_amount, Leaves.set_effect_description_good
        else:
            if head:
                change_amount -= Leaves.Head.effect_amount_bad
            if chest:
                change_amount -= Leaves.Chest.effect_amount_bad
            if legs:
                change_amount -= Leaves.Legs.effect_amount_bad
            return "speech", change_amount, Leaves.set_effect_description_bad


Leaves.Head = Leaves.Head(Leaves)
Leaves.Chest = Leaves.Chest(Leaves)
Leaves.Legs = Leaves.Legs(Leaves)

Gold = Item('Gold', 0, 1, 'valuable', 0, 'The foundation of modern society.. or perhaps its worst mistake?', 75,
            50000)


class GameMaster:
    # This is the class where we store data which do not make sense to contain in the player class
    settings = {}
    Bare_set = (Bare.Head, Bare.Chest, Bare.Legs)
    no_s_at_end_exceptions = ('Gold',)
    game_name = "Please select a game name"
    last_damage_player = ""
    vowels = ("a", "o", "u", "e", "i")
    action_log = ['               ', '               ', '               ', '               ', '               ']
    game_state = {}
    statistics = {}
    y_to_console = 0
    x_to_console = 0
    font_size_x = 0
    font_size_y = 0
    console_location_x = 0
    console_location_y = 0
    console_height_x = 0
    console_height_y = 0


class Character:
    awareness: int
    speed: int
    current_enemy = None

    def __init__(self):
        self.description = str
        self.strength = int
        self.gender = str
        self.Statuses = {}
        self.name = str
        self.current_hp = int
        self.max_hp = int

    def apply_effect(self, status, duration, effect_amount):
        if status in supported_Statuses:
            if status in self.Statuses:
                self.Statuses[status]['duration'] += duration
                self.Statuses[status]['amount'] += effect_amount
            else:
                self.Statuses[status] = {}
                self.Statuses[status]['duration'] = duration
                self.Statuses[status]['amount'] = effect_amount
        else:
            error_logger.error("Unknown Effect: {}".format(status))

    awareness_levels = {95: "paranoid", 90: "on guard", 80: "alert",
                        60: "drowsy", 30: "distracted", 20: "panicking"}

    awareness_hierarchy = (20, 30, 60, 80, 90, 95)

    def awareness_level(self, custom_awareness=None, list_position=False):
        if list_position:
            return self.awareness_hierarchy.index(closest_match(self.awareness, self.awareness_hierarchy))
        if custom_awareness is None:
            return self.awareness_levels[min(list(self.awareness_levels.keys()), key=lambda x: abs(x - self.awareness))]
        else:
            return self.awareness_levels[
                min(list(self.awareness_levels.keys()), key=lambda x: abs(x - custom_awareness))]

    def new_awareness(self, change, amount=0):
        if change == "increase":
            if amount != 0:
                temp_awareness = self.awareness_level(list_position=True)
                if temp_awareness + amount > (len(self.awareness_hierarchy) - 1):
                    return
                else:
                    self.awareness = self.awareness_hierarchy[temp_awareness + amount]

            else:
                try:
                    self.awareness = self.awareness_hierarchy[self.awareness_level(list_position=True) + 1]
                except IndexError:
                    return
        elif change == "decrease":
            if amount != 0:
                temp_awareness = self.awareness_hierarchy.index(closest_match(self.awareness,
                                                                              self.awareness_hierarchy))
                if temp_awareness - amount < 0:
                    return
                else:
                    self.awareness = self.awareness_hierarchy[self.awareness_level(list_position=True) - amount]
            else:
                try:
                    self.awareness = self.awareness_hierarchy[self.awareness_level(list_position=True) - 1]
                except IndexError:
                    return
        elif change == "specific":
            if amount != 0 and 100 >= amount >= 0:
                self.awareness = amount
            else:
                error_logger.error("Invalid custom awareness:{}".format(amount))
        else:
            error_logger.error("Unknown awareness change type{}".format(change))

    speed_levels = {90: "fast as fuck boiii", 80: "fast", 70: "fleet",
                    40: "tired", 30: "sluggish", 20: "injured"}

    speed_hierarchy = (20, 30, 40, 70, 80, 90)

    def speed_level(self, custom_speed=None, list_position=False):
        if list_position:
            return self.speed_hierarchy.index(min(list(self.speed_levels.keys()), key=lambda x: abs(x - self.speed)))
        if custom_speed is None:
            return self.speed_levels[min(list(self.speed_levels.keys()), key=lambda x: abs(x - self.speed))]
        else:
            return self.speed_levels[min(list(self.speed_levels.keys()), key=lambda x: abs(x - custom_speed))]

    def new_speed(self, change, amount=0):
        if change == "increase":
            if amount != 0:
                temp_speed = self.speed_hierarchy.index(closest_match(self.speed,
                                                                      self.speed_hierarchy))
                if temp_speed + amount > (len(self.speed_hierarchy) - 1):
                    return
                else:
                    self.speed = self.speed_hierarchy[self.speed_level(list_position=True) + amount]

            else:
                try:
                    self.speed = self.speed_hierarchy[self.speed_level(list_position=True) + 1]
                except IndexError:
                    return
        elif change == "decrease":
            if amount != 0:
                temp_speed = self.speed_hierarchy.index(closest_match(self.speed,
                                                                      self.speed_hierarchy))
                if temp_speed - amount < 0:
                    return
                else:
                    self.speed = self.speed_hierarchy[self.speed_level(list_position=True) - amount]
            else:
                try:
                    self.speed = self.speed_hierarchy[self.speed_level(list_position=True) - 1]
                except IndexError:
                    return
        elif change == "specific":
            if amount != 0 and 100 >= amount >= 0:
                self.speed = amount
            else:
                error_logger.error("Invalid custom speed{}".format(amount))
        else:
            error_logger.error("Unknown speed change type{}".format(change))

    def deal_damage(self, damage):
        self.current_enemy.current_hp -= damage
        if self.current_enemy.current_hp <= 0 and self.current_enemy != player:
            player.Inventory.loot_drop(player.current_enemy)

    def inspect(self, target):
        if self.gender == "male":
            gender_pronoun_1 = "his"
            gender_pronoun_2 = "he"
        else:
            gender_pronoun_1 = "her"
            gender_pronoun_2 = "she"
        # Checking Whether to add descriptions for ones statuses
        # If so, creates a list with all the current statuses's descriptions
        if not len(self.Statuses) == 0:
            status_descriptions = []
            for status in self.Statuses:
                status_descriptions.append(supported_Statuses[status]['description'])

            # Creates a pretty string, properly joining the descriptions with " ", "," and "and"
            status_string = ""
            for status in status_descriptions:
                if status_descriptions.index(status) == (len(status_descriptions) - 2):
                    status_string = status_string + status + " "
                elif status_descriptions.index(status) == (len(status_descriptions) - 1):
                    if not len(status_string) == 0:
                        status_string = status_string + "and " + status + "."
                    else:
                        status_string = status_string + status + "."
                else:
                    status_string = status_string + status + ", "

            current_states = "\n{} is {}".format(gender_pronoun_2.capitalize(), status_string)
        else:
            # If the enemy is not afflicted, an empty string will be returned to be sued
            current_states = ""

        # Applying buffs and debuffs to the values
        temp_speed = self.speed
        temp_awareness = self.awareness
        temp_strength = self.strength
        for status in self.Statuses:
            if supported_Statuses[status]['head_type'] == "buff":
                if supported_Statuses[status]['apply_type'] == "stronger_speed":
                    temp_speed += self.Statuses[status]
                elif supported_Statuses[status]['apply_type'] == "stronger_awareness":
                    temp_awareness += self.Statuses[status]
                elif supported_Statuses[status]['apply_type'] == "stronger_strength":
                    temp_strength += self.Statuses[status]

        # Joining all the string together
        # Different depending on if the target is the player or the enemy
        if isinstance(target, Player):
            return "You have {}/{} hp.\nYour current strength is {}.\nYou are currently {} and {}.{}" \
                .format(self.current_hp, self.max_hp, temp_strength,
                        self.awareness_level(custom_awareness=temp_awareness),
                        self.speed_level(custom_speed=temp_speed), current_states)
        else:
            return ("{}.\n{} has {}/{} hp.\n{} strength is {}.\n{} is currently {} and {}.{}".format
                    (self.description, self.name, self.current_hp, self.max_hp, gender_pronoun_1.capitalize(),
                     temp_strength, gender_pronoun_2.capitalize(), self.awareness_level(temp_awareness),
                     self.speed_level(temp_speed), current_states))

    # noinspection PyUnresolvedReferences
    def calculate_stat_change(self, stat, stat_value):
        for status in self.Statuses:
            if supported_Statuses[status]['apply_type'] == stat:
                stat_value += player.Statuses[status]['amount']
            elif supported_Statuses[status]['apply_type'] == stat:
                stat_value -= player.Statuses[status]['amount']

        # This code is messy, let's pray that it doesn't break
        effect_level_head = 1
        effect_level_chest = 1
        effect_level_legs = 1
        if player.Inventory.current_equips['head'].parent == player.Inventory.current_equips['chest'].parent:
            effect_level_head += 1
            effect_level_chest += 1
        if player.Inventory.current_equips['head'].parent == player.Inventory.current_equips['legs'].parent:
            effect_level_head += 1
            effect_level_legs += 1
        if player.Inventory.current_equips['chest'].parent == player.Inventory.current_equips['legs'].parent:
            effect_level_legs += 1
            effect_level_chest += 1
        if effect_level_chest == 3:
            effect_level_chest += 2
        if effect_level_head == 3:
            effect_level_head += 2
        if effect_level_legs == 3:
            effect_level_legs += 2

        change_types = []
        armor_effect_amounts = []
        for set_part in player.Inventory.current_equips:
            if set_part == "head":
                change_type, amount, __ = (player.Inventory.current_equips[set_part].parent
                                           .get_set_effect(player, head=True))
            elif set_part == "chest":
                change_type, amount, __ = (player.Inventory.current_equips[set_part].parent
                                           .get_set_effect(player, chest=True))
            elif set_part == "legs":
                change_type, amount, __ = (player.Inventory.current_equips[set_part].parent
                                           .get_set_effect(player, legs=True))
            else:
                error_logger.error("A key dict which does not belong there is in current_equips: {}"
                                   .format(player.Inventory.current_equips))
                amount = 0
                change_type = ""

            change_types.append(change_type)
            armor_effect_amounts.append(amount)

        armor_effect_amounts[0] *= effect_level_head
        armor_effect_amounts[1] *= effect_level_chest
        armor_effect_amounts[2] *= effect_level_legs

        change = False
        if change_types[0] == change_types[1]:
            del change_types[1]
            armor_effect_amounts[0] += armor_effect_amounts[1]
            del armor_effect_amounts[1]
            change = True

        if change:
            if change_types[0] == change_types[1]:
                del change_types[1]
                armor_effect_amounts[0] += armor_effect_amounts[1]
                del armor_effect_amounts[1]
        else:
            if change_types[0] == change_types[2]:
                del change_types[2]
                armor_effect_amounts[0] += armor_effect_amounts[2]
                del armor_effect_amounts[2]
            try:
                if change_types[1] == change_types[2]:
                    del change_types[2]
                    armor_effect_amounts[1] += armor_effect_amounts[2]
                    del armor_effect_amounts[2]
            except IndexError:
                pass

        for change_type in change_types:
            if change_type == stat:
                stat_value += armor_effect_amounts[change_types.index(change_type)]

        if stat_value > 100:
            return 100
        elif stat_value < -100:
            return -100
        else:
            return stat_value


class Player(Character):
    unlocked_Moves = {}
    Statuses = {}

    strength = random.randint(5, 10)
    max_hp = random.randint(25, 30)
    current_hp = max_hp

    # noinspection PyMissingConstructor
    def __init__(self):
        self.name = "tester"
        self.gender = "male"
        self.awareness = 70
        self.speed = 80

    class Inventory:
        items = {}
        max_spaces = 10
        current_equips = {'head': Leaves.Head, 'chest': Leaves.Chest, 'legs': Leaves.Legs}

        # noinspection PyUnresolvedReferences
        @staticmethod
        def get_plural(words):
            # Dicts are only used in the case of the player inventory
            if isinstance(words, dict):
                plural_words = []
                for item in words:
                    if words[item] > 1:
                        if item.name[-1] == "h" or item.name[-1] == "H":
                            plural_words.append('{} {}es'.format(words[item], item.name))
                        # Some things shouldn't have s at the end, even in plural. Example: golds
                        elif item.name not in GameMaster.no_s_at_end_exceptions:
                            plural_words.append('{} {}s'.format(words[item], item.name))
                        else:
                            plural_words.append('{} {}'.format(words[item], item.name))
                    else:
                        plural_words.append('{} {}'.format(words[item], item.name))
                return plural_words
            else:
                item = words
                if isinstance(item, type):
                    if item.name[-1] == "h" or item.name[-1] == "H":
                        final_word = ('{}es'.format(item.name))
                    # Some things shouldn't have s at the end, even in plural. Example: golds is wrong
                    elif item.name not in GameMaster.no_s_at_end_exceptions:
                        final_word = ('{}s'.format(item.name))
                    else:
                        final_word = ('{}'.format(item.name))
                else:
                    if item[-1] == "h" or item[-1] == "H":
                        final_word = ('{}es'.format(item))
                        # Some things shouldn't have s at the end, even in plural. Example: golds
                    elif item not in GameMaster.no_s_at_end_exceptions:
                        final_word = ('{}s'.format(item))
                    else:
                        final_word = ('{}'.format(item))

                return final_word

        @staticmethod
        def unequip(slot: str):
            if player.Inventory.current_equips[slot] != Bare:
                try_unequip = Player.Inventory.add_item(player.Inventory.current_equips[slot])
                if try_unequip == "bag_full":
                    return
                else:
                    if slot == "head":
                        player.Inventory.current_equips[slot] = Bare.Head
                    elif slot == "chest":
                        player.Inventory.current_equips[slot] = Bare.Chest
                    elif slot == "legs":
                        player.Inventory.current_equips[slot] = Bare.Legs
                    else:
                        error_logger.error("slot at unequip={}".format(slot))
            else:
                error_logger.error('Unhandled case of trying to unequip bare in the {} slot'.format(slot))

        @staticmethod
        def throw_away(item):
            # Method for removing an item from the player's inventory
            if item in player.Inventory.items:
                # Checking if the item actually "exists", otherwise deletes it and logs it
                if player.Inventory.items[item] <= 0:
                    del player.Inventory.items[item]
                    error_logger.error("An item of amount {} was found in inventory at throw_away".format(item))
                elif player.Inventory.items[item] == 1:
                    # If only one of the item exists, check if the player is sure
                    # If the player does want to throw it away, it does so and informs the player via the action log
                    confirmation = Console.interactive_choice(['Yes', 'No'],
                                                              ('Are you sure that you want to throw away the {} ?'.
                                                               format(item.name)),
                                                              battle=True)
                    if confirmation == "Yes":
                        del player.Inventory.items[item]
                        GameMaster.action_log.append("You threw away the {}".format(item.name))
                        return "all"
                    elif confirmation == "No":
                        return
                    else:
                        error_logger.error('Unknown case "{}"'.format(confirmation))

                else:
                    amount = Console.interactive_choice(['all', 'specific amount'],
                                                        'How many do you want to throw away?',
                                                        battle=True, back_want=True)
                    if amount == 'all':
                        confirmation = (Console.interactive_choice
                                        (['Yes', 'No'], ('Are you sure that you want to throw away all of the {} ?'.
                                                         format(item.name)), battle=True))

                        if confirmation == "Yes":
                            GameMaster.action_log.append("You threw away all the {}".format(item.name))
                            del player.Inventory.items[item]
                            return 'all'
                        elif confirmation == "No":
                            return
                        else:
                            error_logger.error('Unknown case "{}"'.format(confirmation))
                    elif amount == 'specific amount':
                        if item.name in GameMaster.no_s_at_end_exceptions:
                            head_string = "How much of the {} do you want to throw away?".format(player.Inventory.
                                                                                                 get_plural(item.name))
                        else:
                            head_string = "How many of the {} do you want to throw away?".format(player.Inventory.
                                                                                                 get_plural(item.name))

                        while True:
                            while True:
                                Console.clear()
                                amount_to_throw_away: int = input(head_string + "\n"
                                                                  "If you do not want to throw away any, enter 0\n")
                                if isint(amount_to_throw_away):
                                    amount_to_throw_away = int(amount_to_throw_away)
                                    break
                            if amount_to_throw_away >= player.Inventory.items[item]:
                                GameMaster.action_log.append("You threw away all the {}".format(item.name))
                                del player.Inventory.items[item]
                                return 'all'
                            elif amount_to_throw_away <= 0:
                                return
                            else:
                                (GameMaster.action_log.append("You threw away {} {}"
                                                              .format(amount_to_throw_away,
                                                                      player.Inventory.get_plural(item.name))))
                                player.Inventory.items[item] -= amount_to_throw_away
                                return

            elif item in player.Inventory.current_equips:
                # You can't throw away your own body
                if player.Inventory.current_equips[item] in GameMaster.Bare_set:
                    if item == "head":
                        player.Inventory.current_equips[item] = Bare.Head
                    elif item == "chest":
                        player.Inventory.current_equips[item] = Bare.Chest
                    elif item == "legs":
                        player.Inventory.current_equips[item] = Bare.Legs

            else:
                error_logger.error("Trying to remove the item {}"
                                   " that isn't in the inventory: {}".format(item, player.Inventory.items))

        @staticmethod
        def add_item(item, amount: int = 1):
            current_weight = 0
            if not len(Player.Inventory.items) == 0:
                for thing in Player.Inventory.items:
                    current_weight = current_weight + (thing.weight * Player.Inventory.items[thing])
                if (current_weight + item.weight) <= Player.Inventory.max_spaces:
                    if item not in Player.Inventory.items:
                        Player.Inventory.items[item] = amount
                    else:
                        Player.Inventory.items[item] += amount
                else:
                    print("Your bag can't fit this item")
                    return "bag_full"
            else:
                Player.Inventory.items[item] = amount

        # Method for equipping an armor
        @staticmethod
        def equip(item):
            # Checking if the item is an armor piece
            if hasattr(item, "parent"):
                # Checking that it exists
                if not player.Inventory.items[item] <= 0:
                    # noinspection PyUnresolvedReferences
                    if player.Inventory.current_equips[item.set_part].parent == Bare:
                        player.Inventory.current_equips[item.set_part] = item
                        GameMaster.action_log.append("You equip a {}".format(item.name))
                        if player.Inventory.items[item] == 1:
                            del player.Inventory.items[item]
                        else:
                            player.Inventory.items[item] -= 1
                        return "success"
                else:
                    error_logger.error("{} {} found in inventory".format(player.Inventory.items[item], item.name))
                    del player.Inventory.items[item]
            else:
                error_logger.error("trying to equip {}, which does not have a parent attribute".format(item))

        @staticmethod
        def view():
            # Returns a list of your current items and an informative string that will not be clickable
            if len(player.Inventory.items) != 0:
                head_string = "You have:"
            else:
                head_string = "You have nothing at all, you poor peasant"
            # Formatting the items to be grammatically proper
            item_list = player.Inventory.get_plural(player.Inventory.items)
            # Returning the items in the inventory
            return head_string, item_list

        @staticmethod
        def view_raw_names():
            # Returns a list of all the object names in the inventory
            item_list = []
            for item in player.Inventory.items:
                item_list.append(item)

            return item_list

        # noinspection PyUnresolvedReferences
        @staticmethod
        def view_equips():
            # Returns a string with the player's current equips and the effects of the armor
            # This code is messy, i don't want to talk about it
            # It works(Probably)
            effect_level_head = 1
            effect_level_chest = 1
            effect_level_legs = 1
            if player.Inventory.current_equips['head'].parent == player.Inventory.current_equips['chest'].parent:
                effect_level_head += 1
                effect_level_chest += 1
            if player.Inventory.current_equips['head'].parent == player.Inventory.current_equips['legs'].parent:
                effect_level_head += 1
                effect_level_legs += 1
            if player.Inventory.current_equips['chest'].parent == player.Inventory.current_equips['legs'].parent:
                effect_level_legs += 1
                effect_level_chest += 1

            if effect_level_chest == 3:
                effect_level_chest += 2
            if effect_level_head == 3:
                effect_level_head += 2
            if effect_level_legs == 3:
                effect_level_legs += 2
            head_string = "Equipment bonuses:\n"
            armor_effect_descriptions = []
            armor_effect_amounts = []
            for set_part in player.Inventory.current_equips:
                if set_part == "head":
                    __, amount, description = (player.Inventory.current_equips[set_part].parent
                                               .get_set_effect(player, head=True))
                elif set_part == "chest":
                    __, amount, description = (player.Inventory.current_equips[set_part].parent
                                               .get_set_effect(player, chest=True))
                elif set_part == "legs":
                    __, amount, description = (player.Inventory.current_equips[set_part].parent
                                               .get_set_effect(player, legs=True))
                else:
                    error_logger.error("A key dict which does not belong there is in current_equips: {}"
                                       .format(player.Inventory.current_equips))
                    description = "Something has gone terribly wrong and will be fixed soon"
                    amount = 0

                armor_effect_descriptions.append(description)
                armor_effect_amounts.append(amount)

            armor_effect_amounts[0] *= effect_level_head
            armor_effect_amounts[1] *= effect_level_chest
            armor_effect_amounts[2] *= effect_level_legs

            change = False
            if armor_effect_descriptions[0] == armor_effect_descriptions[1]:
                del armor_effect_descriptions[1]
                armor_effect_amounts[0] += armor_effect_amounts[1]
                del armor_effect_amounts[1]
                change = True

            if change:
                if armor_effect_descriptions[0] == armor_effect_descriptions[1]:
                    del armor_effect_descriptions[1]
                    armor_effect_amounts[0] += armor_effect_amounts[1]
                    del armor_effect_amounts[1]
            else:
                if armor_effect_descriptions[0] == armor_effect_descriptions[2]:
                    del armor_effect_descriptions[2]
                    armor_effect_amounts[0] += armor_effect_amounts[2]
                    del armor_effect_amounts[2]
                try:
                    if armor_effect_descriptions[1] == armor_effect_descriptions[2]:
                        del armor_effect_descriptions[2]
                        armor_effect_amounts[1] += armor_effect_amounts[2]
                        del armor_effect_amounts[2]
                except IndexError:
                    pass

            for armor_effect in armor_effect_descriptions:
                head_string = (head_string + armor_effect +
                               str(abs(armor_effect_amounts[armor_effect_descriptions.index(armor_effect)])) + "\n")

            head_string = head_string + "Current equips:"
            return ['Head: {}'.format(Player.Inventory.current_equips['head'].name),
                    'Chest: {}'.format(Player.Inventory.current_equips['chest'].name),
                    'Legs: {}'.format(Player.Inventory.current_equips['legs'].name)], head_string

        @staticmethod
        def loot_drop(enemy):
            print('You successfully defeated {}!'.format(enemy))
            dropped_items = {}
            if Gold.rarity >= random.randint(0, 100):
                dropped_items[Gold] = random.randint(enemy.rank * 25, enemy.rank * 100)
            for drop in enemy.drops:  # last
                if drop.rarity >= random.randint(0, 100):
                    dropped_items[drop] = int(drop.rarity * (enemy.rank * 0.5))

    def speed_level(self, custom_speed=None, list_position=False):
        return super(Player, self).speed_level(custom_speed=custom_speed, list_position=list_position)

    def awareness_level(self, custom_awareness=None, list_position=False):
        return super(Player, self).awareness_level(custom_awareness=custom_awareness, list_position=list_position)

    def new_awareness(self, change, amount=0):
        super(Player, self).new_awareness(change, amount=amount)

    def new_speed(self, change, amount=0):
        super(Player, self).new_speed(change, amount=amount)

    @staticmethod
    def alive_check():
        if player.current_hp <= 0:
            if GameMaster.last_damage_player != "":
                player.dead(GameMaster.last_damage_player)
            else:
                error_logger.error("Player Took Undocumented Damage")

    @staticmethod
    def dead(killer, custom_text: str = ''):
        Console.clear()
        if custom_text != '':
            print(custom_text)
        else:
            print("You were killed by {}.".format(killer))
        time.sleep(5)
        main_menu()

    @staticmethod
    def add_move(new_move):
        if new_move in supported_moves:
            if new_move not in player.unlocked_Moves:
                player.unlocked_Moves[new_move] = {}
                player.unlocked_Moves[new_move]['type'] = supported_moves[new_move]['type']
            else:
                return "already_unlocked"
        else:
            error_logger.error("unknown move: {} at add_move".format(new_move.__name__))


class Enemy(Character):
    Statuses = {}
    unlocked_Moves = {}

    # noinspection PyMissingConstructor
    def __init__(self, rank: int, name: str, description: str, speed: int, awareness: int, gender: str, *drops,
                 injured: float = False):
        self.current_hp = (int(player.current_hp * (rank * 0.5)) - random.randint(-3, 5))
        if injured:
            self.current_hp = int(self.current_hp * injured)
        self.max_hp = int(player.current_hp * (rank * 0.5)) + (random.randint(-int(player.max_hp * 0.3),
                                                                              int(player.max_hp * 0.3)))
        if self.current_hp > self.max_hp:
            self.current_hp = self.max_hp
        self.strength = round(player.max_hp * (rank * 0.1)) + rank * 2
        self.awareness = awareness
        self.name = name
        self.description = description
        self.speed = speed
        self.gender = gender
        self.drops = []
        for item in drops:
            self.drops.append(item)

    def speed_level(self, custom_speed=None, list_position=False):
        return super(Enemy, self).speed_level(custom_speed=custom_speed, list_position=list_position)

    def awareness_level(self, custom_awareness=None, list_position=False):
        return super(Enemy, self).awareness_level(custom_awareness=custom_awareness, list_position=list_position)

    def new_awareness(self, change, amount=0):
        super(Enemy, self).new_awareness(change, amount=amount)

    def new_speed(self, change, amount=0):
        super(Enemy, self).new_speed(change, amount=amount)


class Orc(Enemy):
    resistances = {
        Statuses.apply_on_fire: 0,
        Statuses.apply_bleed: 0,
        Statuses.apply_weak: 0,
    }


class Animal(Enemy):
    resistances = {
        Statuses.apply_on_fire: 0,
        Statuses.apply_bleed: 0,
        Statuses.apply_weak: 0,
    }


class Human(Enemy):
    resistances = {
        Statuses.apply_on_fire: 0,
        Statuses.apply_bleed: 0,
        Statuses.apply_weak: 0,
    }


class Skeleton(Enemy):
    resistances = {
        Statuses.apply_on_fire: 0,
        Statuses.apply_bleed: 0,
        Statuses.apply_weak: 0,
    }


def main_menu():
    while True:
        # The name which will be shown during the startup sequence and a calculation to ensure it will be centered
        game_name = GameMaster.game_name
        console_spaces_center_name = 60 - int(len(game_name) / 2)
        # Dramatic sort of startup animation
        # This is possible by having for loops counting down determine the game name's location and clearing the console
        # in each new iteration
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
    # Sets both combatant's current enemy to the others
    # This is used in a couple of places for example to determine the loot offered to the player
    player.current_enemy, enemy.current_enemy = enemy, player
    print("{} approaches!".format(enemy.name))

    print(1)

    def player_turn():
        print("player")
        for status in list(player.Statuses):
            player.Statuses[status] -= 1
            if player.Statuses[status] <= 0:
                del player.Statuses[status]

        for status in player.Statuses:
            if supported_Statuses[status]['apply_type'] == "start_dot":
                damage = status(player)
                GameMaster.action_log.append("{} {} damage.You have {} hp left".format
                                             (supported_Statuses[status]['on_apply_message_player'], damage,
                                              player.current_hp))
                GameMaster.last_damage_player = supported_Statuses[status]['type']
                player.alive_check()

        def main_choice():

            def execute_move(move_type):
                available_moves = []
                for ability in player.unlocked_Moves:
                    if player.unlocked_Moves[ability]['type'] == move_type:
                        available_moves.append(ability)
                if len(available_moves) == 0:
                    Console.interactive_choice(["back"],
                                               'You Do not Have any {} Moves Yet. Please Try Something Else'.
                                               format(move_type), battle=True)
                else:
                    pretty_moves = []
                    for move in available_moves:
                        pretty_string_split = move.__name__.split("_")
                        pretty_string_joined = " ".join(pretty_string_split)
                        pretty_moves.append(pretty_string_joined)
                    move: str = Console.interactive_choice(pretty_moves,
                                                           "Click on the move you want to use\nAvailable Moves:",
                                                           back_want=True, battle=True)
                    if move is not None:
                        move_result: str = available_moves[pretty_moves.index(move)](player)
                    else:
                        move_result = None
                    if move_result is not None:
                        GameMaster.action_log.append(move_result)
                        return True

            Console.clear()
            supported_head_moves = ['{}defend{}'.format(colorama.Style.DIM, colorama.Style.NORMAL),
                                    '{}heal{}'.format(colorama.Fore.LIGHTYELLOW_EX, colorama.Fore.RESET),
                                    '{}attack{}'.format(colorama.Fore.LIGHTRED_EX, colorama.Fore.RESET),
                                    '{}debuff{}'.format(colorama.Fore.YELLOW, colorama.Fore.RESET),
                                    '{}buff{}'.format(colorama.Fore.LIGHTCYAN_EX, colorama.Fore.RESET),
                                    'use item(upcoming)', 'inspect', 'help', 'view and edit your inventory', 'settings']
            while True:
                action = Console.interactive_choice(supported_head_moves,
                                                    "{}What do you want to do?{}".format(colorama.Style.BRIGHT,
                                                                                         colorama.Style.NORMAL),
                                                    battle=True, enumerated=True)

                # The equivalent of defend
                if action == 0:
                    end_player_choice = execute_move("defend")
                    if end_player_choice:
                        break

                # The equivalent of heal
                elif action == 1:
                    end_player_choice = execute_move("heal")
                    if end_player_choice:
                        break

                # The equivalent of attack
                elif action == 2:
                    end_player_choice = execute_move("attack")
                    if end_player_choice:
                        break

                # The equivalent of debuff
                elif action == 3:
                    end_player_choice = execute_move("debuff")
                    if end_player_choice:
                        break

                # The equivalent of buff
                elif action == 4:
                    end_player_choice = execute_move("buff")
                    if end_player_choice:
                        break

                # The equivalent of use item
                elif action == 5:
                    end_player_choice = execute_move("use item")
                    if end_player_choice:
                        break

                # The equivalent of inspect
                elif action == 6:
                    inspectable_objects = ['yourself', '{}'.format(player.current_enemy.name)]
                    to_inspect = Console.interactive_choice(inspectable_objects, ('Which one of these do you '
                                                                                  'want to inspect?'),
                                                            battle=True, back_want=True)
                    if to_inspect == "yourself":
                        while True:
                            break_local = Console.interactive_choice(["I'm done"], player.inspect(player),
                                                                     battle=True)
                            if break_local == "I'm done":
                                break

                    elif to_inspect == "{}".format(player.current_enemy.name):
                        Console.interactive_choice(["I'm done"], player.current_enemy.inspect(enemy),
                                                   battle=True)

                # The equivalent of help
                if action == 7:
                    # Different categories you have to traverse through to reach desired information
                    # This is to make sure there are never more than 30 options at the screen at once
                    # If more than 30 options are present at once, it would "break" the console layout
                    help_options = {
                        'moves': {
                            'healing moves': {
                                'calming heal': "Restores health equal to the total of 20% of the caster's current hp"
                                                " and 10% of the caster's maximum hp\n"
                                                "It also increases the caster's awareness by one level",
                                'intense heal': "Restores health equal to the total of 33% of the caster's current hp"
                                                " and 25% of the caster's maximum hp"
                            },
                            'damaging moves': {

                            },
                        },
                        'statuses': {
                            'buffs': {
                                '': '',
                            },
                            'debuffs': {
                                'weak': "Halves the damage of the afflicted's incoming attacks",
                                'bleeding': "At the start of the afflicted's turn, deals damage equal to 15% of "
                                            "the afflicted's maximum hp",
                                'frozen': "Halves the afflicted's speed",
                                'on fire': "At the start of the afflicted's turn, deals damage equal to 10% of"
                                           "the afflicted's turn\nIt also makes the afflicted panic",
                            },
                            'curses': {
                                '': "",
                            }
                        },
                        'sword enchantments': {

                        },

                        'general glossary': {

                        },

                    }
                    # Creates a menu which makes it possible to view the different levels of the above dictionary
                    # The while loops create the functionality to only go back one level
                    while True:
                        help_with: str = Console.interactive_choice(list(help_options.keys()),
                                                                    'What sort of thing do you want to know more '
                                                                    'about?',
                                                                    back_want=True, battle=True)
                        if help_with is None:
                            break
                        while True:
                            subcategory: str = Console.interactive_choice(list(help_options[help_with].keys()),
                                                                          'Which one of these categories '
                                                                          'do you want to know more about?',
                                                                          back_want=True, battle=True)
                            if subcategory is None:
                                break
                            while True:
                                final_type: str = Console.interactive_choice(list(help_options[help_with]
                                                                                  [subcategory].keys()),
                                                                             'Which one of these do you want to know '
                                                                             ' more about?',
                                                                             battle=True, back_want=True)
                                if final_type is None:
                                    break
                                Console.interactive_choice(["back"], help_options[help_with][subcategory]
                                                           [final_type], battle=True)

                # The equivalent of view and edit your inventory
                elif action == 8:
                    # The while loop hierarchy makes it so that you don't go back to the main menu from clicking back
                    while True:
                        # Asking the player for what part of their inventory they want to view
                        case_inventory = Console.interactive_choice(['Current equips', 'Items'],
                                                                    'what part of your inventory do you want to view?',
                                                                    back_want=True, battle=True)
                        # If the player selects back
                        if case_inventory is None:
                            break

                        elif case_inventory == "Current equips":
                            while True:
                                # Getting the current equips
                                case_list, head_string = Player.Inventory.view_equips()
                                # Asking what equip they want to view
                                # We will be using a text changing depending on the equip as the case
                                # Therefore, we will enumerate the cases
                                numbered_case = Console.interactive_choice(case_list, head_string,
                                                                           back_want=True, battle=True,
                                                                           enumerated=True)

                                # noinspection PyUnresolvedReferences
                                def handle_slot(slot: str, joke_text: str = ''):
                                    if slot == "head":
                                        slot_dict = (Player.Inventory.current_equips
                                                     [slot].parent.get_set_part_description
                                                     (Player.Inventory.current_equips[slot], player))
                                    elif slot == "chest":
                                        slot_dict = (Player.Inventory.current_equips
                                                     [slot].parent.get_set_part_description
                                                     (Player.Inventory.current_equips[slot], player))
                                    elif slot == "legs":
                                        slot_dict = (Player.Inventory.current_equips
                                                     [slot].parent.get_set_part_description
                                                     (Player.Inventory.current_equips[slot], player))
                                    else:
                                        error_logger.error("Unknown slot type at handle_slot:{}".format(slot))
                                        slot_dict = {'sorry': 'something failed miserably and it has been noted'}
                                    slot_actions = []
                                    if not Player.Inventory.current_equips[slot] in GameMaster.Bare_set:
                                        slot_actions.append('Throw away')
                                    slot_actions.append('Unequip')
                                    decision = Console.interactive_choice(slot_actions,
                                                                          slot_dict,
                                                                          battle=True, back_want=True)
                                    if decision == "Unequip":
                                        if not Player.Inventory.current_equips[slot] in GameMaster.Bare_set:
                                            Player.Inventory.unequip(slot)
                                        else:
                                            player.dead(None, custom_text=joke_text)

                                    elif decision == "Throw away":
                                        player.Inventory.throw_away(slot)

                                # The equivalent of head
                                if numbered_case == 0:
                                    if player.Inventory.current_equips['head'] == Bare.Head:
                                        handle_slot('head', joke_text='You dismember your own head and die immediately')
                                    else:
                                        handle_slot('head')

                                # The equivalent of chest
                                elif numbered_case == 1:
                                    if player.Inventory.current_equips['chest'] == Bare.Chest:
                                        handle_slot('chest',
                                                    joke_text='How do you even manage to dismember your whole torso?!')
                                    else:
                                        handle_slot('chest')

                                # The equivalent of legs
                                elif numbered_case == 2:
                                    if player.Inventory.current_equips['legs'] == Bare.Legs:
                                        handle_slot('legs',
                                                    joke_text='You dismember your legs and slowly die from blood loss')
                                    else:
                                        handle_slot('legs')

                                # Back
                                elif numbered_case is None:
                                    break
                        elif case_inventory == "Items":
                            while True:
                                head_string, inventory_items = player.Inventory.view()
                                raw_inventory_items = player.Inventory.view_raw_names()
                                item_to_inspect: str = Console.interactive_choice(inventory_items, head_string,
                                                                                  battle=True, back_want=True)

                                # Going back if desired
                                if item_to_inspect is None:
                                    break

                                # Removing integer amounts and whitespace from the string so that it can be used
                                try:
                                    description = (raw_inventory_items
                                                   [inventory_items.index(item_to_inspect)]
                                                   .parent.inspect(raw_inventory_items
                                                                   [inventory_items.index(item_to_inspect)]))
                                except (AttributeError, ValueError):
                                    if item_to_inspect is not None:
                                        description = (raw_inventory_items[inventory_items.index(item_to_inspect)].
                                                       inspect())
                                    else:
                                        description = "Something went wrong under Inventory -> items"

                                # Making a list of the possible ways to interact with the item
                                # noinspection PyListCreation
                                item_actions = []
                                item_actions.append("throw away")

                                # If the item is some sort of armor, you can equip it
                                if hasattr(raw_inventory_items[inventory_items.index(item_to_inspect)], "parent"):
                                    item_actions.append("equip")

                                while True:
                                    item_interaction = Console.interactive_choice(item_actions, description,
                                                                                  battle=True, back_want=True)

                                    if item_interaction is None:
                                        break
                                    elif item_interaction == "throw away":
                                        thrown_away = player.Inventory.throw_away(raw_inventory_items
                                                                                  [inventory_items.index
                                                                                   (item_to_inspect)])
                                        if thrown_away == "all":
                                            break
                                    elif item_interaction == "equip":
                                        result = player.Inventory.equip(raw_inventory_items
                                                                        [inventory_items.index
                                                                         (item_to_inspect)])
                                        if result == "success":
                                            break
                                    else:
                                        error_logger.error("Unknown item interaction: {}".format(item_interaction))

                # The equivalent of settings
                elif action == 9:
                    def save_settings():
                        project_path = os.path.abspath("")
                        with open("{}\\Saves\\General info\\Config.json".format(project_path), 'w') as f:
                            json.dump(GameMaster.settings, f)

                    while True:
                        setting_list = []
                        for key in GameMaster.settings:
                            setting_list.append("{}: {}".format(key, GameMaster.settings[key]))

                        setting_to_be_changed = Console.interactive_choice(setting_list,
                                                                           'Click on any of these to change them',
                                                                           battle=True, back_want=True, enumerated=True)

                        # Going back case
                        if setting_to_be_changed is None:
                            break

                        # Nerd mode case
                        elif setting_to_be_changed == 0:
                            if not GameMaster.settings['nerd mode']:
                                GameMaster.settings['nerd mode'] = True
                            elif GameMaster.settings['nerd mode']:
                                GameMaster.settings['nerd mode'] = False
                            else:
                                (error_logger.error("Illegal case in settings nerd mode:{}"
                                                    .format(GameMaster.settings['nerd mode'])))
                            save_settings()

        # Calls the player's main choice
        # The call is way back here because the code it depends on need to be declared
        main_choice()

    def enemy_turn():
        enemy.deal_damage(enemy.strength)

        print("enemy")
        print("\n")

    while True:
        if (player.awareness * 100) >= random.randint(0, 100):
            player_first = True
        else:
            player_first = False
        while True:
            if player_first:
                player_turn()
                enemy_turn()
            else:
                enemy_turn()
                player_turn()

            temp_player_speed = int(player.speed)
            temp_enemy_speed = int(enemy.speed)

            for effect in player.Statuses:
                if supported_Statuses[effect]['apply_type'] == 'weaker_speed':
                    temp_player_speed = effect(temp_player_speed)

            for effect in enemy.Statuses:
                if supported_Statuses[effect]['apply_type'] == 'weaker_speed':
                    temp_enemy_speed = effect(temp_enemy_speed)

            if random.randint(random.randint(int((temp_player_speed / 3)), (temp_player_speed - 10)),
                              temp_player_speed * 2) >= \
                    random.randint(random.randint(int((temp_enemy_speed / 3)), (temp_enemy_speed - 10)),
                                   temp_enemy_speed * 2):
                player_first = True
            else:
                player_first = False
            time.sleep(2)


def on_start():
    # Setting the game's name
    GameMaster.game_name = "Temporary placeholder for a game name, please change later"

    # Changing the game's title(on the console)
    # Both python 2 and 3 support
    if sys.version_info > (3, 0):
        ctypes.windll.kernel32.SetConsoleTitleW(GameMaster.game_name)
    else:
        ctypes.windll.kernel32.SetConsoleTitleA(GameMaster.game_name)

    # Defining the path of the game
    project_path = os.path.abspath("")

    # Setting up the game settings with json
    if os.stat("{}\\Saves\\General info\\Config.json".format(project_path)).st_size != 0:
        with open("{}\\Saves\\General info\\Config.json".format(project_path)) as f:
            GameMaster.settings = json.load(f)

    else:
        settings = '''
        {
            "nerd mode": false
        }
        '''
        settings = json.loads(settings)
        GameMaster.settings = settings

    # Setting up some loggers
    # Info logger
    def setup_logger(name, file, level=logging.WARNING):
        # Function to easily create loggers

        handler = logging.FileHandler(file)
        formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(filename)s:%(lineno)d:%(message)s")
        handler.setFormatter(formatter)

        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.addHandler(handler)

        return logger

    # Info logger
    info_log = setup_logger("Info logging", "{}\\Logs\\logging_info.log".format(project_path), level=logging.INFO)

    # Error logger
    error_log = setup_logger("Error logging", "{}\\Logs\\logging_errors.log".format(project_path))

    # Settings up some info depending on the windows version used
    with open(project_path + "\\Saves\\General info\\Platform.txt", 'r') as f:
        os_version = f.read()

    if os_version == 'Windows-8.1' or os_version == 'Windows-8':
        GameMaster.console_location_x = 0
        GameMaster.console_location_y = 0
        GameMaster.font_size_x = 8
        GameMaster.font_size_y = 12
        GameMaster.x_to_console = 9
        GameMaster.y_to_console = 32
        GameMaster.console_height_x = 0
        GameMaster.console_location_y = 0
    elif os_version == 'Windows-10':
        GameMaster.console_location_x = -9
        GameMaster.console_location_y = 0
        GameMaster.font_size_x = 8
        GameMaster.font_size_y = 16
        GameMaster.x_to_console = 1
        GameMaster.y_to_console = 30
        GameMaster.console_height_x = 980
        GameMaster.console_height_y = 524
    else:
        # If the user is using an os i'm not yet supporting
        error_log.warning("Unsupported os:{}".format(os_version))

        # Will default to windows 10 settings
        GameMaster.console_location_x = -9
        GameMaster.console_location_y = 0
        GameMaster.font_size_x = 8
        GameMaster.font_size_y = 16
        GameMaster.x_to_console = 1
        GameMaster.y_to_console = 30
        GameMaster.console_height_x = 980
        GameMaster.console_height_y = 524

    return error_log, info_log


if __name__ == '__main__':
    # Setting some variables to be used during runtime
    error_logger, info_logger = on_start()
    player = Player()
    # Initiating colorama so that we can color console output
    colorama.init()
    hen = Enemy(1, 'Gullbert the hen', 'A hen', 40, 20, 'male', "feather", "radish")
    player.add_move(Moves.calming_heal)
    player.add_move(Moves.intense_heal)
    hen.apply_effect(Statuses.apply_frozen, 10, 50)
    Console.console_location_reset()
    player.Inventory.add_item(Gold, 10)
    combat(hen, "swamp")
