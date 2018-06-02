# Better drop system
# Fix back windows 10
import pickle
import random
import time
import os
import win32gui
import pynput


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


class WrongArgsError(Exception):
    # Custom exception to be raised when an unsupported argument is passed
    pass


class GameMasterError(Exception):
    # Custom exception to be raised when an error related to the game master is found
    pass


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
        win32gui.MoveWindow(hwnd, GameMaster.console_location_x, GameMaster.console_location_y, 1000, 400, True)
        os.system("mode con cols=120 lines=30")

    @staticmethod
    def print_with_layout(enemy=None, extra_text=None, battle=False):
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
            enemy_top_healthbar = ' ' * (enemy_healthbar_spacing - len(line_6)) + " " + "_" * 10 + enemy.name

            player_hp = int((player.current_hp / player.max_hp) * 10)
            enemy_hp = int((enemy.current_hp / enemy.max_hp) * 10)

            player_mid_healthbar = (' ' * (player_healthbar_spacing - len(line_23)) + standing_line + block * player_hp
                                    + " " * (10 - player_hp) + standing_line +
                                    "{}/{} hp".format(player.current_hp, player.max_hp))

            enemy_mid_healthbar = (' ' * (enemy_healthbar_spacing - len(line_7)) + standing_line +
                                   block * enemy_hp + " " * (10 - enemy_hp) + standing_line +
                                   '{}/{} hp'.format(enemy.current_hp, enemy.max_hp))

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
    def interactive_choice(cases: list, head_string: str, back_want: bool =False, enemy: object =None,
                           battle: bool=False, enumerated: bool=False):
        # This method makes use of the print_with_layout method in order to make some printed objects clickable
        # Cases is a list of the clickable strings
        # Head_string will be printed at the top of the console and will not be clickable
        # If battle is True, an enemy must be supplied and print_with_layout will use the battle layout
        # If backwant is True, a back option will be added
        # Returns the name of the string clicked(or None, signaling that back was clicked)
        def move_to_string():
            # Formatting the string to be printed
            string_output = head_string
            for action in cases:
                string_output = string_output + "\n*" + action

            if back_want:
                string_output = string_output + "\n*back"

            return string_output

        # Information about the console to be used during text area calculations
        Console.console_location_reset()
        # Console borders need to be accounted for
        console_x_border: int = GameMaster.x_to_console  # pixels
        console_y_border = GameMaster.y_to_console  # pixels
        window_character_width = GameMaster.font_size_x  # pixels
        console_character_height = GameMaster.font_size_y  # pixels
        # Some lines are not clickable
        uninteractive_lines = head_string.count("\n") + 1
        # Formatting the string to be printed
        string_out = move_to_string()
        # Battle layout or not
        if battle:
            Console.print_with_layout(enemy=enemy, extra_text=string_out, battle=True)
        else:
            Console.print_with_layout(extra_text=string_out)

        # Adding a back option if desired
        if back_want:
            cases.append("back")

        # Calculating the areas which are clickable
        # First two x values, then two y values in the dict
        line_areas = []
        for i in range(0, 31):
            line_areas.append([])
        for move in cases:
            line_areas[cases.index(move)].append(console_x_border)
            line_areas[cases.index(move)].append(len(move) * window_character_width + console_x_border)

            line_areas[cases.index(move)].append(console_y_border + console_character_height * uninteractive_lines)
            line_areas[cases.index(move)].append((cases.index(move) + 1) * console_character_height
                                                 + console_y_border + console_character_height * uninteractive_lines)
        # Removing empty nested lists
        line_areas = [x for x in line_areas if x != []]

        # Support for back feature
        temp = len(GameMaster.action_log)

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
            # If a clickable object was clicked, return which one
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
    def __init__(self, name: str, weight: int, value: int, item_type: str, item_id: int, description: str, rarity: int):
        self.rarity = rarity
        self.name = name
        self.weight = weight
        self.value = value
        self.item_type = item_type
        self.item_id = item_id
        self.description = description

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
        return self.rarity_levels[closest_match(self.rarity, self.rarity_hierarchy)]

    # Displaying information about the item when inspected
    def inspect(self):
        # Checking whether to use "a" or "an"
        if str(self.item_type)[0] in GameMaster.vowels:
            a_or_an = "an"
        else:
            a_or_an = "a"

        # Some flavor texts contains quest marks or exclamation marks at the end
        # We do not want (flavor text)?. hence, we do the following operation
        temp_description = self.description
        sentence_endings = ('!', '?', '.')
        if not temp_description[-1] in sentence_endings:
            temp_description = temp_description + "."

        # Concatenating it all together
        return ("{}\nIt is worth {} gold and weighs {}.\nIt is {} {} that is {}".format
                (temp_description, self.value, self.weight, a_or_an, self.item_type, self.rarity_level()))


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
    inspect_flavor_text = "Error: no set inspect_flavor_text"

    # noinspection PyMethodOverriding
    def inspect(self, setbonus):
        if setbonus:
            special_effect_text = ". {}".format(self.inspect_flavor_text)
        else:
            special_effect_text = ""
        return super(Wearable, self).inspect() + "{}".format(special_effect_text)


class Weapon(Item):
    def __init__(self, name, weight, value, item_type, item_id, description, rarity,
                 weapon_damage, special_effect=None, effect_rate=0):
        Item.__init__(self, name, weight, value, item_type, item_id, description, rarity)
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

    set_effect_description_good = 'People are astonished by your amazing body, making negotiating easier'
    set_effect_description_bad = "People won't trust you, running around without clothes"
    set_effect = ArmorEffect.change_stat
    change_type = "speech"
    inspect_flavor_text = 'Get some real clothes, you hobo'
    Head = {
        'weight': 0,
        'value': 'unsellable',
        'rarity': 'unobtainable',
        'defense': 1,
        'description_good': 'Even though your face looks terrible, people are distracted by your glorious body,',
        'effect_amount_good': 0,
        'description_bad': 'Your face looks terrible, it will make negotiating harder',
        'effect_amount_bad': -2
    }

    Chest = {
        'weight': 0,
        'value': 'unsellable',
        'rarity': 'unobtainable',
        'defense': 3,
        'description_good': 'Nice gains, bro',
        'effect_amount_good': 4,
        'description_bad': 'You even lift, bro?',
        'effect_amount_bad': -1
    }

    Legs = {
        'weight': 0,
        'value': 'unsellable',
        'rarity': 'unobtainable',
        'defense': 2,
        'description_good': 'Not wearing pants only seems to be in your flavor with such a body',
        'effect_amount_good': 1,
        'description_bad': 'oh please, at least put some pants on',
        'effect_amount bad': -7

    }

    @staticmethod
    def get_set_part_description(set_part: dict) -> str:
        if player.strength > 50:
            return set_part['description_good']
        else:
            return set_part['description_bad']

    @staticmethod
    def get_set_effect(user: object, head: bool, chest: bool, legs: bool):
        change_amount = 0
        effect_level = 0
        if user.strength > 50:
            if head:
                effect_level += 1
                change_amount += Bare.Head['effect_amount_good']
            if chest:
                effect_level += 1
                change_amount += Bare.Chest['effect_amount_good']
            if legs:
                effect_level += 1
                change_amount += Bare.Legs['effect_amount_good']
            return "speech", change_amount, effect_level, Bare.set_effect_description_good
        else:
            if head:
                effect_level += 1
                change_amount -= Bare.Head['effect_amount_good']
            if chest:
                effect_level += 1
                change_amount -= Bare.Chest['effect_amount_good']
            if legs:
                effect_level += 1
                change_amount -= Bare.Legs['effect_amount_good']
            return "speech", change_amount, effect_level, Bare.set_effect_description_bad


Gold = Item('Gold', 0, 1, 'valuable', 0, 'The foundation of modern society.. or perhaps its worst mistake?', 75)


class GameMaster:
    # This is the class where we store data which do not make sense to contain in the player class
    last_damage_player = ""
    vowels = ("a", "o", "u", "e", "i")
    action_log = ['               ', '               ', '               ', '               ', '               ']
    game_state = {}
    statistics = {}
    y_to_console = int
    x_to_console = int
    font_size_x = int
    font_size_y = int
    console_location_x = int
    console_location_y = int


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
            raise WrongArgsError("Unknown Effect: {} at apply_effect".format(status))

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
                raise WrongArgsError("Invalid custom awareness at new_awareness")
        else:
            raise WrongArgsError("Unknown change type at new_awareness")

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
                raise WrongArgsError("Invalid custom speed at new_speed")
        else:
            raise WrongArgsError("Unknown change type at new_speed")

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

    def calculate_stat_change(self, stat, stat_value):
        for status in self.Statuses:
            if supported_Statuses[status]['apply_type'] == stat:
                stat_value += player.Statuses[status]['amount']
            elif supported_Statuses[status]['apply_type'] == stat:
                stat_value -= player.Statuses[status]['amount']


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
        current_equips = {'head': Bare, 'chest': Bare, 'legs': Bare}

        def calculate_carry_strength():
            temp_strength = player.strength




        @staticmethod
        def unequip(slot):
            if player.current_equips[slot] != Bare:
                try_unequip = Player.Inventory.add_item(player.current_equips[slot])
                if try_unequip == "bag_full":
                    return
                else:
                    player.current_equips[slot] = Bare
            else:
                print('You have nothing equipped in the {} slot'.format(slot))

        @staticmethod
        def add_item(item, amount=1):
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

        @staticmethod
        def view():
            # Returns a list of your current items and an informative string that will not be clickable
            # Some things shouldn't have s at the end, even in plural. Example: golds
            no_s_at_end_exceptions = ('Gold')
            head_string = "You have:"
            item_list = []
            # Formatting the items to be grammatically proper
            for item in Player.Inventory.items:
                if Player.Inventory.items[item] > 1:
                    if item.name[-1] == "h" or item.name[-1] == "H":
                        item_list.append('{} {}es'.format(Player.Inventory.items[item], item.name))
                    elif item.name not in no_s_at_end_exceptions:
                        item_list.append('{} {}s'.format(Player.Inventory.items[item], item.name))
                    else:
                        item_list.append('{} {}'.format(Player.Inventory.items[item], item.name))
                else:
                    item_list.append('{} {}'.format(Player.Inventory.items[item], item.name))

            # Returning the items in the inventory
            return head_string, item_list

        @staticmethod
        def view_equips():
            # Returns a string with the player's current equips
            return ['Head: {}'.format(Player.Inventory.current_equips['head'].__name__),
                    'Chest: {}'.format(Player.Inventory.current_equips['chest'].__name__),
                    'Legs: {}'.format(Player.Inventory.current_equips['legs'].__name__)], 'Current equips:'



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
                raise GameMasterError("Player Took Undocumented Damage")

    @staticmethod
    def dead(killer, custom_text: str=''):
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
            raise WrongArgsError("unknown move: {} at add_move".format(new_move.__name__))


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
        game_name = "Haitai"
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
                                               format(move_type), battle=True, enemy=enemy)
                else:
                    pretty_moves = []
                    for move in available_moves:
                        pretty_string_split = move.__name__.split("_")
                        pretty_string_joined = " ".join(pretty_string_split)
                        pretty_moves.append(pretty_string_joined)
                    move = Console.interactive_choice(pretty_moves,
                                                      "Click on the move you want to use\nAvailable Moves:",
                                                      back_want=True, enemy=enemy, battle=True)
                    if move is not None:
                        result: str = available_moves[pretty_moves.index(move)](player)
                    else:
                        result = None
                    if result is not None:
                        GameMaster.action_log.append(result)
                        return True

            Console.clear()
            supported_head_moves = ['defend', 'heal', 'attack', 'debuff', 'buff',
                                    'use item', 'inspect', 'help', 'view and edit your inventory']
            while True:
                action = Console.interactive_choice(supported_head_moves, "What do you want to do?",
                                                    enemy=enemy, battle=True)

                action = action.lower()
                if action == "heal":
                    end_player_choice = execute_move("heal")
                    if end_player_choice:
                        break

                elif action == "defend":
                    end_player_choice = execute_move("defend")
                    if end_player_choice:
                        break

                elif action == "attack":
                    end_player_choice = execute_move("attack")
                    if end_player_choice:
                        break

                elif action == "debuff":
                    end_player_choice = execute_move("debuff")
                    if end_player_choice:
                        break

                elif action == "use item":
                    end_player_choice = execute_move("use item")
                    if end_player_choice:
                        break

                elif action == "buff":
                    end_player_choice = execute_move("buff")
                    if end_player_choice:
                        break

                elif action == "view and edit your inventory":
                    # The while loop hierarchy makes it so that you don't go back to the main menu from clicking back
                    while True:
                        # Asking the player for what part of their inventory they want to view
                        case_inventory = Console.interactive_choice(['Current equips', 'Items'],
                                                                    'what part of your inventory do you want to view?',
                                                                    back_want=True, battle=True, enemy=enemy)
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
                                                                           enemy=enemy, enumerated=True)

                                def handle_slot(slot: str, joke_text: str=''):
                                    if slot == "head":
                                        slot_dict = (Player.Inventory.current_equips
                                                     [slot].get_set_part_description
                                                     (Player.Inventory.current_equips[slot].Head))
                                    elif slot == "chest":
                                        slot_dict = (Player.Inventory.current_equips
                                                     [slot].get_set_part_description
                                                     (Player.Inventory.current_equips[slot].Chest))
                                    elif slot == "legs":
                                        slot_dict = (Player.Inventory.current_equips
                                                     [slot].get_set_part_description
                                                     (Player.Inventory.current_equips[slot].Legs))
                                    else:
                                        raise WrongArgsError("Unknown slot type at handle_slot")
                                    slot_actions = []
                                    if not Player.Inventory.current_equips[slot] == Bare:
                                        slot_actions.append('Throw away')
                                    slot_actions.append('Unequip')
                                    action = Console.interactive_choice(slot_actions,
                                                                        slot_dict,
                                                                        battle=True, enemy=enemy, back_want=True)
                                    if action == "Unequip":
                                        if not Player.Inventory.current_equips[slot]:
                                            Player.Inventory.unequip(slot)
                                        else:
                                            player.dead(None, custom_text=joke_text)

                                # The equivalent of head
                                if numbered_case == 0:
                                    handle_slot('head', joke_text='You dismember your own head and die immediately')

                                # The equivalent of chest
                                elif numbered_case == 1:
                                    handle_slot('chest',
                                                joke_text='How do you even manage to dismember your whole torso?!')
                                # The equivalent of legs
                                elif numbered_case == 2:
                                    handle_slot('legs',
                                                joke_text='You dismember your legs and slowly die from blood loss')
                                #

                elif action == "inspect":
                    inspectable_objects = ['inventory items', 'yourself', '{}'.format(player.current_enemy.name)]
                    to_inspect = Console.interactive_choice(inspectable_objects, ('Which one of these do you '
                                                                                  'want to inspect?'),
                                                            enemy=enemy, battle=True, back_want=True)
                    if to_inspect == "yourself":
                        while True:
                            break_local = Console.interactive_choice(["I'm done"], player.inspect(player), enemy=enemy,
                                                                     battle=True)
                            if break_local == "I'm done":
                                break

                    elif to_inspect == "{}".format(player.current_enemy.name):
                        Console.interactive_choice(["I'm done"], player.current_enemy.inspect(enemy), enemy=enemy,
                                                   battle=True)

                    elif to_inspect == "inventory items":
                        head_string, inventory_items = player.Inventory.view()
                        item_to_inspect = Console.interactive_choice(inventory_items, head_string,
                                                                     battle=True, enemy=enemy, back_want=True)

                        # Removing integer amounts and whitespace from the string so that it can be used
                        item_to_inspect = item_to_inspect.replace(" ", "")
                        no_int_item_to_inspect = ""
                        for letter in item_to_inspect:
                            if not isint(letter):
                                no_int_item_to_inspect = no_int_item_to_inspect + letter
                        # Eval isn't accounted for in my IDE's styling guide
                        # noinspection PyUnusedLocal
                        # Adding so parenthesis to make the item callable through eval
                        final_item_to_inspect = no_int_item_to_inspect + ".inspect()"
                        print(final_item_to_inspect)
                        Console.interactive_choice(["back"], eval("eval(final_item_to_inspect)"),
                                                   battle=True, enemy=enemy)

                if action == "help":
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
                        help_with = Console.interactive_choice(list(help_options.keys()),
                                                               'What sort of thing do you want to know more about?',
                                                               back_want=True, battle=True, enemy=enemy)
                        if help_with is None:
                            break
                        while True:
                            subcategory = Console.interactive_choice(list(help_options[help_with].keys()),
                                                                     'Which one of these categories '
                                                                     'do you want to know more about?',
                                                                     back_want=True, battle=True, enemy=enemy)
                            if subcategory is None:
                                break
                            while True:
                                final_type = Console.interactive_choice(list(help_options[help_with]
                                                                             [subcategory].keys()),
                                                                        'Which one of these do you want to know more '
                                                                        'about?',
                                                                        battle=True, enemy=enemy, back_want=True)
                                if final_type is None:
                                    break
                                Console.interactive_choice(["back"], help_options[help_with][subcategory]
                                                           [final_type], battle=True, enemy=enemy)

        # Calls the player's main choice
        # The call is way back here because the function after and the functions it depends on need to be declared
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


def windows_version_handling():
    accepted_windows_versions = ('windows 8', 'windows 10', 'other')
    print("Welcome!\nI see this is your first time running this game.\nSo far, this game is only supported on "
          'windows 10 and windows 8.\nPlease type in which one of these you are using.\nIf it is antoher version, try'
          ' typing "other" although the game might not play well')

    while True:
        version = input("Please type your version\n>>> ")
        version = version.lower()
        if version in accepted_windows_versions:
            if version == 'windows 8':
                GameMaster.console_location_x = 0
                GameMaster.console_location_y = 0
                GameMaster.font_size_x = 8
                GameMaster.font_size_y = 12
                GameMaster.x_to_console = 9
                GameMaster.y_to_console = 32
                break
            elif version == 'windows 10':
                GameMaster.console_location_x = -7
                GameMaster.console_location_y = 0
                GameMaster.font_size_x = 8
                GameMaster.font_size_y = 16
                GameMaster.x_to_console = 1
                GameMaster.y_to_console = 30
                break


if __name__ == '__main__':
    windows_version_handling()
    player = Player()
    hen = Enemy(1, 'Gullbert the hen', 'A hen', 40, 20, 'male', "feather", "radish")
    player.add_move(Moves.calming_heal)
    player.add_move(Moves.intense_heal)
    hen.apply_effect(Statuses.apply_frozen, 10, 50)
    Console.console_location_reset()
    player.Inventory.add_item(Gold, 10)
    combat(hen, "swamp")
