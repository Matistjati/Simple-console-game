# todo Better drop system
# Return values:
# 0: Failed for something like an error in internal structure
# 1: Success (even if nothing changed, it may be considered success)
# 2: "Failed" due to some sort of intended reason

import random
import time
import os
import sys
import ctypes
import logging
import json
import subprocess
import winreg
import platform
from enum import Enum

# Importing modules not in standard library
try:
    import colorama
    import win32gui
    import pynput
except ModuleNotFoundError as missing_module:
    print("Missing module error: {}".format(missing_module))


# Returns the closest matching integer/float to the passed value in an array of integers/floats
def closest_match(number, array):
    if isinstance(array, dict):
        return min(list(array.keys()), key=lambda x: abs(x - number))
    else:
        return min(array, key=lambda x: abs(x - number))


# Returns a bool representing if the entered variable is an int or not
def isint(variable_to_test):
    try:
        variable_to_test = int(variable_to_test)
        variable_to_test += 1
        return True
    except ValueError:
        return False


# Starts a subprocess playing a the passed wav file
# We only need to pass the name since it looks in the game's music folder
# A subprocess is used so that it runs in the background and stops if the game is exited
def play_wav(file_name):
    # Ensuring that we don't play try to play a nonexistant file
    if file_name not in GameMaster.missing_audio:
        project_path = os.path.dirname(sys.argv[0])

        subprocess.Popen(["python", "{}\\Scripts\\play_wav.py".format(project_path),
                          "{}\\Audio\\{}".format(project_path, file_name)], shell=False)
    else:
        return


class ColoredString(str):
    """
    A custom data type intended to contain strings with ANSI codes
    The main purpose of it is to return the length of the string that will be displayed, not the ANSI
    """
    def __new__(cls, string: str, reset_colors: bool=True, colored_chars=0):
        if reset_colors and string[-4:] != colorama.Style.RESET_ALL:
            string += colorama.Style.RESET_ALL
            colored_chars += len(colorama.Style.RESET_ALL)
        new_str = super(ColoredString, cls).__new__(cls, string)
        new_str.string = string
        new_str.colored_chars = colored_chars
        return new_str

    def __len__(self):
        temp_str_len = super(ColoredString, self).__len__()
        temp_str_len -= self.colored_chars

        return temp_str_len

    def __add__(self, s):
        if isinstance(s, ColoredString):
            return ColoredString((self.string + s), colored_chars=(self.colored_chars + s.colored_chars),
                                 reset_colors=False)
        else:
            return ColoredString((self.string + s), colored_chars=self.colored_chars, reset_colors=False)

    def __radd__(self, other):
        if isinstance(other, ColoredString):
            return ColoredString((other + self.string), colored_chars=(self.colored_chars + other.colored_chars),
                                 reset_colors=False)
        else:
            return ColoredString((other + self.string), colored_chars=self.colored_chars, reset_colors=False)

    def __repr__(self):
        return ColoredString(self.string)

    def __str__(self):
        return ColoredString(self.string)


class Console:
    # A class for collecting all methods related to the console
    @staticmethod
    def clear():
        # Removes all written characters in the console
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def size_reset():
        # Sets the console to a desired size
        os.system("mode con cols=120 lines=30")

    @staticmethod
    def print_with_layout(extra_text=None, battle=False):
        """ Method for printing text along with other things, for example a layout
         The layout will remain at static location, even if other text is printed to the same line
         If battle is passed as true, the battle layout containing healthbars,
         an action log and turn meter will be printed too
        """
        Console.clear()
        enemy = player.current_enemy

        # Determining the type of extra_text in order to handle correctly
        if extra_text is not None:
            if isinstance(extra_text, list):
                lines_in = extra_text
            elif isinstance(extra_text, str):
                # Splitting input into a list
                lines_in = extra_text.split("\n")
            else:
                error_logger.error("Unknown extra text type: {}, {}".format(type(extra_text), extra_text))
                lines_in = extra_text
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

        # Declaring ASCII characters for the health_bars and the action log
        standing_line = chr(124)
        block = chr(9608)
        top_line = chr(175)

        # Checking if we want the battle layout
        if battle:
            # Declaring the resource bars, actions log and turn meter
            # This is done in such a way that they will remain at a static position in the console

            # A turn meter at the upper-right corner
            turn = (" " * ((119 - (len("Turn ") + len(str(GameMaster.turn)))) - len(line_1)) +
                    "Turn {}".format(GameMaster.turn))

            # Player's resource bar
            # The top and bottom of the player's resource bar
            # How many characters from left the resource bar is
            player_health_bar_spacing = 26

            player_top_resource_bar = (' ' * (player_health_bar_spacing - len(line_22)) + " " + ("_" * 10) +
                                       player.name + " ")
            player_bot_resource_bar = ' ' * (player_health_bar_spacing - len(line_26)) + " " + top_line * 10

            # Adding symbols for easy information of current statuses
            for status in player.Statuses:
                if status == Statuses.stun:
                    player_top_resource_bar += ColoredString("{}*".format(colorama.Fore.LIGHTYELLOW_EX),
                                                             colored_chars=len(colorama.Fore.LIGHTYELLOW_EX))
                elif status == Statuses.apply_bleed:
                    player_top_resource_bar += ColoredString("{}{}".format(colorama.Fore.LIGHTRED_EX, chr(191)),
                                                             colored_chars=len(colorama.Fore.LIGHTRED_EX))
                # Checking if the effect is a stat boost
                elif status in [i.value for i in Stats]:
                    if player.Statuses[status]['amount'] >= 0:
                        player_top_resource_bar += ColoredString("{}^".format(colorama.Fore.LIGHTBLUE_EX),
                                                                 colored_chars=len(colorama.Fore.LIGHTBLUE_EX))
                    else:
                        player_top_resource_bar += ColoredString("{}v".format(colorama.Fore.YELLOW),
                                                                 colored_chars=len(colorama.Fore.YELLOW))

            # Calculating and displaying the player's resources
            player_hp = int((player.current_hp / player.max_hp) * 10)
            player_mp = int((player.current_mp / player.max_mp) * 10)
            player_stamina = int((player.current_stamina / player.max_stamina) * 10)

            player_mid_health_bar = (' ' * (player_health_bar_spacing - len(line_23)) + standing_line +
                                     ColoredString("{}{}".format(colorama.Fore.RED, (block * player_hp)),
                                                   colored_chars=len(colorama.Fore.RED))
                                     + " " * (10 - player_hp) + standing_line +
                                     "{}/{} hp".format(player.current_hp, player.max_hp))

            player_mid_mp_bar = (' ' * (player_health_bar_spacing - len(line_24)) + standing_line +
                                 ColoredString("{}{}".format(colorama.Fore.BLUE, (block * player_mp)),
                                               colored_chars=len(colorama.Fore.BLUE))
                                 + " " * (10 - player_mp) + standing_line +
                                 "{}/{} mp".format(player.current_mp, player.max_mp))

            player_mid_stamina_bar = (' ' * (player_health_bar_spacing - len(line_25)) + standing_line +
                                      ColoredString("{}{}".format(colorama.Fore.GREEN, (block * player_stamina)),
                                                    colored_chars=len(colorama.Fore.GREEN))
                                      + " " * (10 - player_stamina) + standing_line +
                                      "{}/{} stamina".format(player.current_stamina, player.max_stamina))

            # Enemy's resources
            # The top and bottom of the enemy's resource bar

            # How many characters from left to right the resource bar is
            enemy_health_bar_spacing = 80

            enemy_top_resource_bar = (' ' * (enemy_health_bar_spacing - len(line_6))
                                      + " " + "_" * 10 + player.current_enemy.name + " ")
            enemy_bot_resource_bar = ' ' * (enemy_health_bar_spacing - len(line_10)) + " " + top_line * 10

            # Adding symbols for easy information of current statuses
            for status in player.current_enemy.Statuses:
                if status == Statuses.stun:
                    enemy_top_resource_bar += "{}*{}".format(colorama.Fore.LIGHTYELLOW_EX, colorama.Style.RESET_ALL)
                elif status == Statuses.apply_bleed:
                    enemy_top_resource_bar += "{}{}{}".format(colorama.Fore.LIGHTRED_EX, chr(191),
                                                              colorama.Style.RESET_ALL)
                # Checking if the effect is a stat boost
                elif status in [i.value for i in Stats]:
                    if enemy.Statuses[status]['amount'] >= 0:
                        enemy_top_resource_bar += "{}^{}".format(colorama.Fore.LIGHTBLUE_EX, colorama.Style.RESET_ALL)
                    else:
                        enemy_top_resource_bar += "{}v{}".format(colorama.Fore.YELLOW, chr(8673),
                                                                 colorama.Style.RESET_ALL)

            # Calculating and diplaying the enemy's resources
            enemy_hp = int((player.current_enemy.current_hp / player.current_enemy.max_hp) * 10)
            enemy_mp = int((player.current_enemy.current_mp / player.current_enemy.max_mp) * 10)
            enemy_stamina = int((player.current_enemy.current_stamina / player.current_enemy.max_stamina) * 10)

            enemy_mid_health_bar = (' ' * (enemy_health_bar_spacing - len(line_7)) + standing_line +
                                    ColoredString("{}{}".format(colorama.Fore.RED, (block * enemy_hp)),
                                                  colored_chars=len(colorama.Fore.RED))
                                    + " " * (10 - enemy_hp) + standing_line +
                                    '{}/{} hp'.format(player.current_enemy.current_hp, player.current_enemy.max_hp))

            enemy_mid_mp_bar = (' ' * (enemy_health_bar_spacing - len(line_8)) + standing_line +
                                ColoredString("{}{}".format(colorama.Fore.BLUE, (block * enemy_mp)),
                                              colored_chars=len(colorama.Fore.BLUE))
                                + " " * (10 - enemy_mp) + standing_line +
                                '{}/{} mp'.format(player.current_enemy.current_mp, player.current_enemy.max_mp))

            enemy_mid_stamina_bar = (' ' * (enemy_health_bar_spacing - len(line_9)) + standing_line +
                                     ColoredString("{}{}".format(colorama.Fore.GREEN, (block * enemy_stamina)),
                                                   colored_chars=len(colorama.Fore.GREEN))
                                     + " " * (10 - enemy_stamina) + standing_line +
                                     '{}/{} stamina'.format(player.current_enemy.current_stamina,
                                                            player.current_enemy.max_stamina))

            # Calculating some spacing for the action log
            overlapping_action_log_spacing_special = 30
            overlapping_action_log_spacing = 22
            normal_action_log_spacing = 52

            log_lines = 5
            max_spacing = max(
                list(len(GameMaster.action_log[- (i + 1)]) for i in range(log_lines)))

            spacing_1 = " " * (max_spacing - len(GameMaster.action_log[-1]))
            spacing_2 = " " * (max_spacing - len(GameMaster.action_log[-2]))
            spacing_3 = " " * (max_spacing - len(GameMaster.action_log[-3]))
            spacing_4 = " " * (max_spacing - len(GameMaster.action_log[-4]))
            spacing_5 = " " * (max_spacing - len(GameMaster.action_log[-5]))

            # Defining the action log parts
            action_log_top = (' ' * (overlapping_action_log_spacing - (len(player_top_resource_bar)) +
                                     (overlapping_action_log_spacing_special - len(line_22))) + " " +
                              "_" * max_spacing + "Action log")

            action_log_bot = (" " + ' ' * (normal_action_log_spacing - len(line_27)) + top_line * max_spacing)

            action_log_mid_1 = (' ' * (overlapping_action_log_spacing - (len(player_mid_health_bar)) +
                                (overlapping_action_log_spacing_special - len(line_23)))
                                + standing_line +
                                GameMaster.action_log[len(GameMaster.action_log) - 1]
                                + spacing_1 + standing_line)

            action_log_mid_2 = (' ' * (overlapping_action_log_spacing - (len(player_mid_mp_bar)) +
                                       (overlapping_action_log_spacing_special - len(line_24)))
                                + standing_line +
                                GameMaster.action_log[len(GameMaster.action_log) - 2]
                                + spacing_2 + standing_line)

            action_log_mid_3 = (' ' * (overlapping_action_log_spacing - (len(player_mid_stamina_bar)) +
                                       (overlapping_action_log_spacing_special - len(line_25)))
                                + standing_line +
                                GameMaster.action_log[len(GameMaster.action_log) - 3]
                                + spacing_3 + standing_line)

            action_log_mid_4 = (' ' * (overlapping_action_log_spacing - (len(player_bot_resource_bar)) +
                                       (overlapping_action_log_spacing_special - len(line_26)))
                                + standing_line +
                                GameMaster.action_log[len(GameMaster.action_log) - 4]
                                + spacing_4 + standing_line)

            action_log_mid_5 = (' ' * (normal_action_log_spacing - len(line_27)) + standing_line +
                                GameMaster.action_log[len(GameMaster.action_log) - 5]
                                + spacing_5 + standing_line)

        # If we don't want the battle layout, the health_bars and the log will instead be empty strings
        else:
            turn = ""

            enemy_top_resource_bar = ""
            enemy_bot_resource_bar = ""
            enemy_mid_health_bar = ""
            enemy_mid_mp_bar = ""
            enemy_mid_stamina_bar = ""

            player_top_resource_bar = ""
            player_bot_resource_bar = ""
            player_mid_health_bar = ""
            player_mid_stamina_bar = ""
            player_mid_mp_bar = ""

            action_log_top = ""
            action_log_bot = ""
            action_log_mid_1 = ""
            action_log_mid_2 = ""
            action_log_mid_3 = ""
            action_log_mid_4 = ""
            action_log_mid_5 = ""

        # Joining all the strings to be printed
        lines = {0: line_1 + turn, 1: line_2, 2: line_3, 3: line_4, 4: line_5,
                 5: line_6 + enemy_top_resource_bar,
                 6: line_7 + enemy_mid_health_bar,
                 7: line_8 + enemy_mid_mp_bar,
                 8: line_9 + enemy_mid_stamina_bar,
                 9: line_10 + enemy_bot_resource_bar,
                 10: line_11, 11: line_12, 12: line_13,
                 13: line_14, 14: line_15, 15: line_16, 16: line_17, 17: line_18,
                 18: line_19, 19: line_20, 20: line_21,
                 21: line_22 + player_top_resource_bar + action_log_top,
                 22: line_23 + player_mid_health_bar + action_log_mid_1,
                 23: line_24 + player_mid_mp_bar + action_log_mid_2,
                 24: line_25 + player_mid_stamina_bar + action_log_mid_3,
                 25: line_26 + player_bot_resource_bar + action_log_mid_4,
                 26: line_27 + action_log_mid_5,
                 27: line_28 + action_log_bot,
                 28: line_29}

        # Printing the strings
        for i in range(0, 29):
            print(lines[i])

    @staticmethod
    def interactive_choice(cases: list, head_string: str, back_want: bool = False,
                           battle: bool = False, enumerated: bool = False, custom_area=()):
        # This method makes use of the print_with_layout method in order to make some printed objects clickable
        # Cases is a list of the clickable strings
        # Head_string will be printed at the top of the console and will not be clickable
        # If battle is True, an enemy must be supplied and print_with_layout will use the battle layout
        # If back_want is True, a back option will be added
        # Returns the name of the string clicked(or None, signaling that back was clicked)
        if len(custom_area) == 0:
            GameMaster.last_interactive_choice_call['cases'] = cases
            GameMaster.last_interactive_choice_call['head_string'] = head_string
            GameMaster.last_interactive_choice_call['back_want'] = back_want
            GameMaster.last_interactive_choice_call['battle'] = battle
            GameMaster.last_interactive_choice_call['enumerated'] = enumerated

        # Console borders need to be accounted for
        console_x_border: int = GameMaster.x_to_console  # pixels
        console_y_border: int = GameMaster.y_to_console  # pixels
        font_size_x: int = GameMaster.font_size_x  # pixels
        font_size_y: int = GameMaster.font_size_y  # pixels

        # Some lines are not clickable
        uninteractive_lines = head_string.count("\n") + 1

        # Adding a back option if desired
        if back_want and "back" not in cases:
            cases.append("back")

        # If you're bug hunting a displaced turn meter, this is the root of the problem
        # The split method returns a string, therefore removing the coloredstring's custom len
        # The easiest way to solve this is to never have two colored strings as head strings
        if len(custom_area) == 0:
            if head_string.count("\n") != 0:
                head_string_list = head_string.split("\n")
                temp_cases = head_string_list + cases
            else:
                temp_cases = cases.copy()
                temp_cases.insert(0, head_string)

        if len(custom_area) == 0:
            # noinspection PyUnboundLocalVariable
            temp_cases = ["*" + case for case in temp_cases]
        else:
            temp_cases = cases.copy()

        # Printing everything
        Console.print_with_layout(extra_text=temp_cases, battle=battle)

        case = None

        if len(custom_area) == 0:
            line_areas = []
            for i in range(0, 31):
                line_areas.append([])
            for move in cases:
                line_areas[cases.index(move)].append(console_x_border)
                line_areas[cases.index(move)].append((len(move) * font_size_x) + console_x_border)

                line_areas[cases.index(move)].append(((cases.index(move)) * font_size_y
                                                      + console_y_border + font_size_y * uninteractive_lines) -
                                                     8)
                line_areas[cases.index(move)].append((cases.index(move) + 1) * font_size_y
                                                     + console_y_border + font_size_y * uninteractive_lines)

            # Removing empty nested lists
            line_areas = [x for x in line_areas if x != []]

        else:
            line_areas = [list(row) for row in custom_area]
            for sublist in line_areas:
                line_areas[line_areas.index(sublist)][0] *= font_size_x
                line_areas[line_areas.index(sublist)][0] += console_x_border

                line_areas[line_areas.index(sublist)][1] *= font_size_x
                line_areas[line_areas.index(sublist)][1] += console_x_border

                line_areas[line_areas.index(sublist)][2] *= font_size_y
                line_areas[line_areas.index(sublist)][2] += console_y_border

                line_areas[line_areas.index(sublist)][3] *= font_size_y
                line_areas[line_areas.index(sublist)][3] += console_y_border

        def update_area():
            x_y_window = []

            # noinspection PyUnusedLocal
            def callback(hwnd, extra):
                rect = win32gui.GetWindowRect(hwnd)
                x_window = rect[0]
                y_window = rect[1]
                w = rect[2] - x_window
                h = rect[3] - y_window
                if win32gui.GetWindowText(hwnd) == GameMaster.game_name:
                    nonlocal x_y_window
                    x_y_window = [x_window, y_window]

            win32gui.EnumWindows(callback, None)

            # TODO Support stationary console location
            if len(x_y_window) == 0:
                listener.stop()
                return

            temp_console_x_border = x_y_window[0]
            temp_console_y_border = x_y_window[1]

            # Calculating the areas which are clickable
            # First two x values, then two y values in the dict
            temp_line_areas = list(sub__list.copy() for sub__list in line_areas)

            for sub_list in temp_line_areas:
                temp_line_areas[temp_line_areas.index(sub_list)][0] += temp_console_x_border
                temp_line_areas[temp_line_areas.index(sub_list)][1] += temp_console_x_border
                temp_line_areas[temp_line_areas.index(sub_list)][2] += temp_console_y_border
                temp_line_areas[temp_line_areas.index(sub_list)][3] += temp_console_y_border

            return temp_line_areas

        def on_click(x, y, button, pressed):
            temp_line_areas = update_area()
            if temp_line_areas is None:
                return

            # Checking whether a left click is performed
            if pressed and button == pynput.mouse.Button.left:
                if len(custom_area) == 0:
                    for x_y in temp_line_areas:
                        # Checking if the mouse input is within the desired area
                        if (x in range(temp_line_areas[temp_line_areas.index(x_y)][0],
                                       temp_line_areas[temp_line_areas.index(x_y)][1]) and
                            y in range(temp_line_areas[temp_line_areas.index(x_y)][2],
                                       temp_line_areas[temp_line_areas.index(x_y)][3])):
                            # For the listener to exit, we need to return false
                            # Therefore, in order to return other values, we use a global variable
                            nonlocal case
                            case = cases[temp_line_areas.index(x_y)]
                            return False

                else:
                    for x_y in temp_line_areas:

                        # Checking if the mouse input is within the desired area
                        if (x in range(temp_line_areas[temp_line_areas.index(x_y)][0],
                                       temp_line_areas[temp_line_areas.index(x_y)][1])and
                            y in range(temp_line_areas[temp_line_areas.index(x_y)][2],
                                       temp_line_areas[temp_line_areas.index(x_y)][3])):

                            if cases[temp_line_areas.index(x_y)] != "":
                                global case_custom_area
                                case_custom_area = cases[temp_line_areas.index(x_y)]
                                return False

        # Checks for mouse clicks, if there are any it calls on_click
        with pynput.mouse.Listener(on_click=on_click) as listener:
            listener.join()

        if len(custom_area) == 0:
            try:
                _ = case
                del _
            except NameError:
                print("It seems that you aren't running this game through a console. Please do")
                input()
                raise SystemExit
            finally:
                if case is None:
                    print("It seems that you aren't running this game through a console. Please do")
                    input()
                    raise SystemExit

            if case == "*back" or case == "back":
                # If the input is back, return None
                return None
            else:
                # If a clickable case was clicked, return which one
                # If enumerated is true, we return the index of the case
                if enumerated:
                    return cases.index(case)
                else:
                    if case[0] == "*":
                        case = case[1:]
                    return case

        else:
            if case_custom_area == "back":
                # If the input is back, return None
                return None
            else:
                # If a clickable case was clicked, return which one
                # If enumerated is true, we return the index of the case
                if enumerated:
                    return cases.index(case_custom_area)
                else:
                    return case_custom_area


class Statuses:
    # A collection class of all the statuses a character can have
    @staticmethod
    def apply_bleed(target):
        # Applies DOT damage at the start of a turn
        damage_taken = (int(target.max_hp * 0.15))
        return damage_taken

    @staticmethod
    def stun():
        pass


supported_Statuses = {
    # Information about the previous class's statuses
    # head_type sorting whether it's a positive or negative effect.
    # head_type is also used in curses, effects that don't go away by simply playing
    # apply_type is used to determine when during combat the effect takes effect
    # type doesn't serve any purpose at the moment
    # description is used when inspecting someone who is afflicted
    # on_apply_message_player and enemy are to be used in the action log
    Statuses.apply_bleed:
        {
            'head_type': 'debuff',
            'apply_type': 'start_dot',
            'type': 'burning',
            'description': 'Bleeding',
            'description_nerd': 'Bleed',
            'on_apply_message_player': 'You better stop this bleeding soon... You take',
            'on_apply_message_enemy': 'Blood spills forth as the enemy takes'
        },
    Statuses.stun:
        {
            'head_type': 'debuff',
            'apply_type': '',
            'description': 'Stunned',
            'description_nerd': 'Stun',
            'on_apply_message_player': 'Your head feels too dizzy to do anything.',
            'on_apply_message_enemy': 'Looks like {} is too dizzy to act'
        }
}


WeaponEffect = {

}


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
        a_or_an = "an" if str(self.item_type)[0] in GameMaster.vowels else "a"

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
        if GameMaster.settings['nerd mode']:
            return ("{}\nIt is worth {} gold and weighs {}.\nIt is {} {} whose droprate is {}%.".format
                    (temp_description, self.value, weight, a_or_an, self.item_type, self.rarity))
        else:
            return ("{}\nIt is worth {} gold and weighs {}.\nIt is {} {} that is {}.".format
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
                 weapon_damage, crit, special_effect=None, effect_rate=0):
        super().__init__(name, weight, value, item_type, item_id, description, rarity, max_stack)
        self.weapon_damage = weapon_damage
        self.crit = crit
        if not effect_rate:
            self.special_effect = special_effect
            self.effect_rate = effect_rate

    likeliness_levels = {80: "very likely", 60: "likely", 40: "unlikely",
                         20: "very unlikely"}

    crit_levels = {33: 'very likely', 20: 'highly likely', 10: 'likely', 5: 'unlikely', 2: 'very unlikely'}

    def likeliness_level(self):
        return self.likeliness_levels[closest_match(self.effect_rate, self.likeliness_levels)]

    def crit_level(self):
        return self.crit_levels[closest_match(self.crit, self.crit_levels)]

    def inspect(self):
        a_or_an = "an" if str(self.item_type)[0] in GameMaster.vowels else "a"

        if self.special_effect is not None:
            if GameMaster.settings['nerd mode']:
                special_effect_text = ("{} that works {}% of the time".format
                                       (WeaponEffect[self.special_effect]['description'],
                                        self.effect_rate))

            else:
                special_effect_text = ("{} and is {} affect the enemy".format
                                       (WeaponEffect[self.special_effect]['description'],
                                        self.likeliness_level()))
        else:
            special_effect_text = ""

        if GameMaster.settings['nerd mode']:
            return ("{}.\nGold worth: {}, weight: {}. Damage: {}, crit: {}%, droprate: {}%. {}".format
                    (self.description, self.value, self.weight, a_or_an, self.item_type, self.rarity,
                     special_effect_text))
        else:
            return ("{}.\nIt is worth {} gold and weighs {}.\n"
                    "You will deal around {} damage when attacking with this and are {} to deal double damage.\n"
                    "It is {}. {}".format
                    (self.description, self.value if self.value != 0 else 'nothing',
                     self.weight if self.weight != 0 else 'nothing', self.weapon_damage, self.crit_level(),
                     self.rarity_level(),
                     special_effect_text))


# feather = Item('feather', 1, 10, 'material', 1, 'A feather from a hen', 'common')
# radish = Item('radish', 1, 20, 'food', 2, 'Fresh from The earth!', 'uncommon')
#
# feather.inspect()
# b = Wearable()
class Bare(Wearable):
    item_id = 1

    set_effect_description_good = 'People are astonished by your amazing body, increasing your charisma by '
    set_effect_description_bad = "People won't trust you, running around without clothes, decreasing your charisma by "

    effect_inspect_text = "If you're weak and naked, no one will trust you, making negotiating harder.\n" \
                          "However, if you're buff, people will be amazed, making negotiating easier"

    change_type = "charisma"
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
        dodge_mod = 4
        crit_mod = 0
        speed_mod = 10
        damage_mod = 0
        charisma_mod = 0
        intelligence_mod = 0
        hp_regen_mod = 0
        mp_regen_mod = 0
        stamina_regen_mod = 0
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
        dodge_mod = 4
        crit_mod = 0
        speed_mod = 10
        damage_mod = 0
        charisma_mod = 0
        intelligence_mod = 0
        hp_regen_mod = 0
        mp_regen_mod = 0
        stamina_regen_mod = 1
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
        dodge_mod = 4
        crit_mod = 0
        speed_mod = 10
        damage_mod = 0
        charisma_mod = 0
        intelligence_mod = 0
        hp_regen_mod = 0
        mp_regen_mod = 0
        stamina_regen_mod = 0
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
        if hasattr(user, 'parent'):
            user_strength = user.parent.strength
        else:
            user_strength = user.strength

        if user_strength > 50:
            if head:
                change_amount += Bare.Head.effect_amount_good
            if chest:
                change_amount += Bare.Chest.effect_amount_good
            if legs:
                change_amount += Bare.Legs.effect_amount_good
            return "charisma", change_amount, Bare.set_effect_description_good
        else:
            if head:
                change_amount -= Bare.Head.effect_amount_bad
            if chest:
                change_amount -= Bare.Chest.effect_amount_bad
            if legs:
                change_amount -= Bare.Legs.effect_amount_bad
            return "charisma", change_amount, Bare.set_effect_description_bad


class Leaves(Wearable):
    item_id = 2

    set_effect_description_good = "People are happy that you're hiding at least a little of your weak body, " \
                                  "increasing your charisma by "
    set_effect_description_bad = "People are disappointed that you're hiding your glorious body, decreasing " \
                                 "your charisma by "
    effect_inspect_text = "If you're weak, people will respect you for hiding your weak body, increasing your " \
                          "charisma\nHowever, if you're buff, people will become angry for not showing yourself," \
                          " decreasing your charisma"
    change_type = "charisma"
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
        dodge_mod = 4
        crit_mod = 0
        speed_mod = 13
        damage_mod = 0
        charisma_mod = 0
        intelligence_mod = 3
        hp_regen_mod = 0
        mp_regen_mod = 0
        stamina_regen_mod = 0
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
        dodge_mod = 4
        crit_mod = 0
        speed_mod = 13
        damage_mod = 0
        charisma_mod = 0
        intelligence_mod = 3
        hp_regen_mod = 0
        mp_regen_mod = 1
        stamina_regen_mod = 0
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
        dodge_mod = 4
        crit_mod = 0
        speed_mod = 13
        damage_mod = 0
        charisma_mod = 0
        intelligence_mod = 3
        hp_regen_mod = 0
        mp_regen_mod = 0
        stamina_regen_mod = 0
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
        # noinspection PyUnresolvedReferences
        if hasattr(user, 'parent'):
            user_strength = user.parent.strength
        else:
            user_strength = user.strength

        if user_strength < 50:
            if head:
                change_amount += Leaves.Head.effect_amount_good
            if chest:
                change_amount += Leaves.Chest.effect_amount_good
            if legs:
                change_amount += Leaves.Legs.effect_amount_good
            return "charisma", change_amount, Leaves.set_effect_description_good
        else:
            if head:
                change_amount -= Leaves.Head.effect_amount_bad
            if chest:
                change_amount -= Leaves.Chest.effect_amount_bad
            if legs:
                change_amount -= Leaves.Legs.effect_amount_bad
            return "charisma", change_amount, Leaves.set_effect_description_bad


# Initiating all items
Gold = Item('Gold', 0, 1, 'valuable', 0, 'The foundation of modern society.. or perhaps its worst mistake?', 75,
            50000)

Leaves.Head = Leaves.Head(Leaves)
Leaves.Chest = Leaves.Chest(Leaves)
Leaves.Legs = Leaves.Legs(Leaves)

Bare.Head = Bare.Head(Bare)
Bare.Chest = Bare.Chest(Bare)
Bare.Legs = Bare.Legs(Bare)

Fist = Weapon('Fist', 0, 0, 'weapon', 3, 'A plain old fist', 75, 1, 2, 3)
WoodenSword = Weapon('Wooden sword', 5, 10, 'weapon', 4, 'A plain old sword out of sturdy oak', 20, 1, 4, 4,)


# An enumeration of all the game stats
class Stats(Enum):
    crit = 'crit'
    charisma = 'charisma'
    speed = 'speed'
    awareness = 'awareness'
    strength = 'strength'
    intelligence = 'intelligence'
    dodge = 'dodge'
    prot = 'prot'
    hp_regen = 'hp_regen'
    mp_regen = 'mp_regen'
    stamina_regen = 'stamina_regen'


class GameMaster:
    # Runtime computations

    # Tuples that can be iterated through to check for various things
    percent_stats = ('crit', 'dodge', 'prot')
    Bare_set = (Bare.Head, Bare.Chest, Bare.Legs, Fist)
    no_s_at_end_exceptions = ('Gold',)
    vowels = ("a", "o", "u", "e", "i", "A", "O", "U", "E", "I")

    # The game settings
    # Should contain nerd mode, quickedit and forcev2
    settings = {}
    # The name of the game, used for setting the title of the process and getting a handle to it
    game_name = "Please select a game name"
    # Used to ensure that an audio file exists when trying to play it
    missing_audio = []
    # Some info about the console
    y_to_console = 0
    x_to_console = 0
    font_size_x = 0
    font_size_y = 0
    # Used at the death screen
    last_damage_player = ""
    # Counter for displaying the current turn during combat
    # It gets incremented and reset from the combat function
    turn = 1
    # A dict containing the last call to interactive choice
    # This is used in case we need to update the action log
    last_interactive_choice_call = {'cases': [], 'head_string': '', 'battle': False, 'back_want': False}
    # A list containing actions made by the player and the enemy to be displayed
    # This should never be appended to directly
    action_log = ['               ', '               ', '               ', '               ', '               ',
                  '               ']

    # A method for appending to the action log
    def extend_action_log(self, new_action):
        # Ensuring that the message will never be too long
        if len(new_action) > 56:
            self.action_log.append('Message too long. Show the developer your error log')
            error_logger.error("Message longer than 56 chars found at action_log: {}. len: {}".format(new_action,
                                                                                                      len(new_action)))
        else:
            #  Calling interactive_choice to ensure a smoother experience
            self.action_log.append(new_action)
            if self.last_interactive_choice_call['head_string'] != "":
                temp_cases = GameMaster.last_interactive_choice_call['cases'].copy()
                temp_head_string = GameMaster.last_interactive_choice_call['head_string'][:]
                if (GameMaster.last_interactive_choice_call['back_want'] and
                        "back" not in GameMaster.last_interactive_choice_call['cases']):
                    temp_cases.append("back")

                if temp_head_string.count("\n") != 0:
                    temp_head_string_list = temp_head_string.split("\n")
                    temp_cases = temp_head_string_list + temp_cases
                else:
                    temp_cases.insert(0, temp_head_string)

                temp_cases = ["*" + case for case in temp_cases]
                Console.print_with_layout(extra_text=temp_cases, battle=self.last_interactive_choice_call['battle'])
                time.sleep(1)


class Character:
    awareness: int
    speed: int

    def __init__(self, name, gender, dodge, speed, intelligence, prot,
                 crit, charisma, awareness, max_hp, max_stamina, max_mp, hp_regen,
                 stamina_regen, mp_regen, strength, description=""):
        self.name = name
        name_split = name.split()
        self.first_name = name_split[0]
        self.gender = gender
        self.intelligence = intelligence
        self.dodge = dodge
        self.speed = speed
        self.gender = gender
        self.prot = prot
        self.crit = crit
        self.charisma = charisma
        self.awareness = awareness
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.max_mp = max_mp
        self.current_mp = max_mp
        self.max_stamina = max_stamina
        self.current_stamina = max_stamina
        self.hp_regen = hp_regen
        self.mp_regen = mp_regen
        self.stamina_regen = stamina_regen
        self.strength = strength
        self.description = ""
        self.Statuses = {}
        self.current_enemy = None
        self.description = description

    # noinspection PyUnresolvedReferences
    def calculate_stat_change(self, stat, stat_value):
        if stat in [i.value for i in Stats]:
            error_logger.error("Unknown stat type at calculate_stat_change: {}".format(stat))
            return stat_value

        for status in self.Statuses:
            try:
                if status == stat:
                    stat_value += player.Statuses[status]['amount']
            except KeyError:
                pass

        # This code is messy, let's pray that it doesn't break
        effect_level_head = 1
        effect_level_chest = 1
        effect_level_legs = 1
        if player.inventory.current_equips['head'].parent == player.inventory.current_equips['chest'].parent:
            effect_level_head += 1
            effect_level_chest += 1
        if player.inventory.current_equips['head'].parent == player.inventory.current_equips['legs'].parent:
            effect_level_head += 1
            effect_level_legs += 1
        if player.inventory.current_equips['chest'].parent == player.inventory.current_equips['legs'].parent:
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
        if self == player:
            for set_part in self.inventory.current_equips:
                if set_part == "head":
                    change_type, amount, __ = (self.inventory.current_equips[set_part].parent
                                               .get_set_effect(player, head=True))
                elif set_part == "chest":
                    change_type, amount, __ = (self.inventory.current_equips[set_part].parent
                                               .get_set_effect(player, chest=True))
                elif set_part == "legs":
                    change_type, amount, __ = (self.inventory.current_equips[set_part].parent
                                               .get_set_effect(player, legs=True))
                else:
                    amount = 0
                    change_type = ""

                change_types.append(change_type)
                armor_effect_amounts.append(amount)

        elif hasattr(self, 'current_equips'):
            for set_part in self.current_equips:
                if set_part == "head":
                    change_type, amount, __ = (self.current_equips[set_part].parent
                                               .get_set_effect(player, head=True))
                elif set_part == "chest":
                    change_type, amount, __ = (self.current_equips[set_part].parent
                                               .get_set_effect(player, chest=True))
                elif set_part == "legs":
                    change_type, amount, __ = (self.current_equips[set_part].parent
                                               .get_set_effect(player, legs=True))
                else:
                    amount = 0
                    change_type = ""

                change_types.append(change_type)
                armor_effect_amounts.append(amount)

        elif isinstance(self, Enemy):
            for set_part in self.inventory.current_equips:
                if set_part == "head":
                    change_type, amount, __ = (self.inventory.current_equips[set_part].parent
                                               .get_set_effect(player, head=True))
                elif set_part == "chest":
                    change_type, amount, __ = (self.inventory.current_equips[set_part].parent
                                               .get_set_effect(player, chest=True))
                elif set_part == "legs":
                    change_type, amount, __ = (self.inventory.current_equips[set_part].parent
                                               .get_set_effect(player, legs=True))
                else:
                    amount = 0
                    change_type = ""

                change_types.append(change_type)
                armor_effect_amounts.append(amount)

        else:
            error_logger.error("Unknown self: {}".format(self))

        try:
            armor_effect_amounts[0] *= effect_level_head
        except IndexError:
            pass

        try:
            armor_effect_amounts[1] *= effect_level_chest
        except IndexError:
            pass

        try:
            armor_effect_amounts[2] *= effect_level_legs
        except IndexError:
            pass

        change = False
        try:
            if change_types[0] == change_types[1]:
                del change_types[1]
                armor_effect_amounts[0] += armor_effect_amounts[1]
                del armor_effect_amounts[1]
                change = True
        except IndexError:
            pass

        if change:
            try:
                if change_types[0] == change_types[1]:
                    del change_types[1]
                    armor_effect_amounts[0] += armor_effect_amounts[1]
                    del armor_effect_amounts[1]
            except IndexError:
                pass
        else:
            try:
                if change_types[0] == change_types[2]:
                    del change_types[2]
                    armor_effect_amounts[0] += armor_effect_amounts[2]
                    del armor_effect_amounts[2]
            except IndexError:
                pass

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

        if self == player:
            head = self.inventory.current_equips['head']
            chest = self.inventory.current_equips['chest']
            legs = self.inventory.current_equips['legs']
        elif hasattr(self, 'current_equips'):
            head = self.current_equips('head')
            chest = self.current_equips('chest')
            legs = self.current_equips('legs')
        elif isinstance(self, Enemy):
            head = self.inventory.current_equips['head']
            chest = self.inventory.current_equips['chest']
            legs = self.inventory.current_equips['legs']
        else:
            error_logger.error("Unknown self: {}".format(self))
            head = Bare.Head
            chest = Bare.Chest
            legs = Bare.Legs

        if stat == 'crit':
            stat_value += head.crit_mod
            stat_value += chest.crit_mod
            stat_value += legs.crit_mod
        elif stat == 'intelligence':
            stat_value += head.intelligence_mod
            stat_value += chest.intelligence_mod
            stat_value += legs.intelligence_mod
        elif stat == 'dodge':
            stat_value += head.dodge_mod
            stat_value += chest.dodge_mod
            stat_value += legs.dodge_mod
        elif stat == 'speed':
            stat_value += head.speed_mod
            stat_value += chest.speed_mod
            stat_value += legs.speed_mod
        elif stat == 'damage':
            stat_value += head.damage_mod
            stat_value += chest.damage_mod
            stat_value += legs.damage_mod
        elif stat == 'charisma':
            stat_value += head.charisma_mod
            stat_value += chest.charisma_mod
            stat_value += legs.charisma_mod
        elif stat == 'hp_regen':
            stat_value += head.hp_regen_mod
            stat_value += chest.hp_regen_mod
            stat_value += legs.hp_regen_mod
        elif stat == 'mp_regen':
            stat_value += head.mp_regen_mod
            stat_value += chest.mp_regen_mod
            stat_value += legs.mp_regen_mod
        elif stat == 'stamina_regen':
            stat_value += head.stamina_regen_mod
            stat_value += chest.stamina_regen_mod
            stat_value += legs.stamina_regen_mod

        if stat_value > 100:
            return 100
        elif stat_value < -100:
            return -100
        else:
            return stat_value

    class Inventory:
        def __init__(self, parent, max_spaces: int = 10):
            self.max_spaces = max_spaces
            self.parent = parent
        items = {}
        current_equips = {'head': Leaves.Head, 'chest': Leaves.Chest, 'legs': Leaves.Legs, 'left hand': WoodenSword,
                          'right hand': WoodenSword}

        # noinspection PyUnresolvedReferences
        @staticmethod
        def get_plural(words):
            # Dicts are only used in the case of the inventory
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

        def unequip(self, slot: str):
            if self.current_equips[slot] != Bare:
                try_unequip = self.add_item(self.current_equips[slot])
                if try_unequip == "bag_full":
                    return
                else:
                    if slot == "head":
                        self.current_equips[slot] = Bare.Head
                    elif slot == "chest":
                        self.current_equips[slot] = Bare.Chest
                    elif slot == "legs":
                        self.current_equips[slot] = Bare.Legs
                    elif slot == "left hand":
                        self.current_equips[slot] = Fist
                    elif slot == "right hand":
                        self.current_equips[slot] = Fist

                    else:
                        error_logger.error("slot at unequip={}".format(slot))
            else:
                error_logger.error('Unhandled case of trying to unequip bare in the {} slot'.format(slot))

        def throw_away(self, item):
            # Method for removing an item from the inventory
            if item in self.items:
                # Checking if the item actually "exists", otherwise deletes it and logs it
                if self.items[item] <= 0:
                    del self.items[item]
                    error_logger.error("An item of amount {} was found in inventory at throw_away".format(item))
                elif self.items[item] == 1:
                    # If only one of the item exists, check if the player is sure
                    # If the player does want to throw it away, it does so and informs the player via the action log
                    confirmation = Console.interactive_choice(['Yes', 'No'],
                                                              ('Are you sure that you want to throw away the {} ?'.
                                                               format(item.name)),
                                                              battle=True)
                    if confirmation == "Yes":
                        del self.items[item]
                        GameMaster.extend_action_log("You threw away the {}".format(item.name))
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
                                                         format(item.name)), battle=True,))

                        if confirmation == "Yes":
                            GameMaster.extend_action_log("You threw away all the {}".format(item.name))
                            del self.items[item]
                            return 'all'
                        elif confirmation == "No":
                            return
                        else:
                            error_logger.error('Unknown case "{}"'.format(confirmation))
                    elif amount == 'specific amount':
                        if item.name in GameMaster.no_s_at_end_exceptions:
                            head_string = "How much of the {} do you want to throw away?".format(self.
                                                                                                 get_plural(item.name))
                        else:
                            head_string = "How many of the {} do you want to throw away?".format(self.
                                                                                                 get_plural(item.name))

                        while True:
                            while True:
                                Console.clear()
                                amount_to_throw_away: int = input(head_string + "\n"
                                                                  "If you do not want to throw away any, enter 0\n")
                                if isint(amount_to_throw_away):
                                    amount_to_throw_away = int(amount_to_throw_away)
                                    break
                            if amount_to_throw_away >= self.items[item]:
                                GameMaster.extend_action_log("You threw away all the {}".format(item.name))
                                del self.items[item]
                                return 'all'
                            elif amount_to_throw_away <= 0:
                                return
                            else:
                                (GameMaster.extend_action_log("You threw away {} {}"
                                                              .format(amount_to_throw_away,
                                                                      self.get_plural(item.name))))
                                self.items[item] -= amount_to_throw_away
                                return

            elif item in self.current_equips:
                confirmation = Console.interactive_choice(['Yes', 'No'],
                                                          ('Are you sure that you want to throw away the {} ?'.
                                                           format(self.current_equips[item].name)),
                                                          battle=True)
                # You can't throw away your own body
                if confirmation:
                    if item == "head":
                        self.current_equips[item] = Bare.Head
                    elif item == "chest":
                        self.current_equips[item] = Bare.Chest
                    elif item == "legs":
                        self.current_equips[item] = Bare.Legs
                    elif item == "left hand":
                        self.current_equips[item] = Fist
                    elif item == "right hand":
                        self.current_equips[item] = Fist
                    else:
                        error_logger.error('Error trying to unequip unknown type: {}'.format(item))

            else:
                error_logger.error("Trying to remove the item {}"
                                   " that isn't in the inventory or current equips: {}, {}".format(item, self.items,
                                                                                                   self.current_equips))

        def add_item(self, item, amount: int = 1):
            current_weight = 0
            if not len(self.items) == 0:
                for thing in self.items:
                    current_weight = current_weight + (thing.weight * self.items[thing])
                if (current_weight + item.weight) <= self.max_spaces:
                    if item not in self.items:
                        self.items[item] = amount
                    else:
                        self.items[item] += amount
                else:
                    print("Your bag can't fit this item")
                    return 2
            else:
                self.items[item] = amount

        # Method for equipping an armor
        def equip(self, item, hand=""):
            # Checking if the item is an armor piece
            if hasattr(item, "parent"):
                # Checking that it exists
                if not self.items[item] <= 0:
                    # noinspection PyUnresolvedReferences
                    if self.current_equips[item.set_part].parent == Bare:
                        self.current_equips[item.set_part] = item
                        GameMaster.extend_action_log("You equip a {}".format(item.name))
                        if self.items[item] == 1:
                            del self.items[item]
                        else:
                            self.items[item] -= 1
                        return 1
                    else:
                        error_logger.error("Equip called on non-bare Bare")
                        return 2
                else:
                    error_logger.error("{} {} found in inventory".format(self.items[item], item.name))
                    del self.items[item]

            elif isinstance(item, Weapon):
                # Checking that it exists
                if not self.items[item] <= 0:
                    if hand != "":
                        if self.current_equips[hand] == Fist:
                            self.current_equips[hand] = item
                            GameMaster.extend_action_log("You equip a {}".format(item.name))
                            if self.items[item] == 1:
                                del self.items[item]
                            else:
                                self.items[item] -= 1
                            return 1
                        else:
                            GameMaster.extend_action_log("Your {} is already using something else".format(hand))
                            return 1
                    else:
                        error_logger.error("Trying to equip weapon {}, {} without hand provided".format(item.name,
                                                                                                        item))
                else:
                    error_logger.error("{} {} found in inventory".format(self.items[item], item.name))
                    del self.items[item]

            else:
                error_logger.error("trying to equip {}, which is not an armor or weapon".format(item))

        def view(self):
            # Returns a list of your current items and an informative string that will not be clickable
            if len(self.items) != 0:
                head_string = "You have:"
            else:
                head_string = "You have nothing at all, you poor peasant"
            # Formatting the items to be grammatically proper
            item_list = self.get_plural(self.items)
            # Returning the items in the inventory
            return head_string, item_list

        def view_raw_names(self):
            # Returns a list of all the object names in the inventory
            item_list = []
            for item in self.items:
                item_list.append(item)

            return item_list

        # noinspection PyUnresolvedReferences
        def view_equips(self):
            # Returns a string with the current equips and the effects of the armor
            # This code is messy, i don't want to talk about it
            # It works(Probably)
            effect_level_head = 1
            effect_level_chest = 1
            effect_level_legs = 1

            if self.current_equips['head'].parent == self.current_equips['chest'].parent:
                effect_level_head += 1
                effect_level_chest += 1
            if self.current_equips['head'].parent == self.current_equips['legs'].parent:
                effect_level_head += 1
                effect_level_legs += 1
            if self.current_equips['chest'].parent == self.current_equips['legs'].parent:
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
            for set_part in self.current_equips:
                if set_part == "head":
                    __, amount, description = (self.current_equips[set_part].parent
                                               .get_set_effect(self, head=True))
                elif set_part == "chest":
                    __, amount, description = (self.current_equips[set_part].parent
                                               .get_set_effect(self, chest=True))
                elif set_part == "legs":
                    __, amount, description = (self.current_equips[set_part].parent
                                               .get_set_effect(self, legs=True))
                elif set_part == "left hand" or set_part == "right hand":
                    pass
                else:
                    error_logger.error("A key dict which does not belong there is in current_equips: {}"
                                       .format(self.current_equips))
                    description = "Something has gone terribly wrong and will be fixed soon"
                    amount = 0

                # noinspection PyUnboundLocalVariable
                armor_effect_descriptions.append(description)
                # noinspection PyUnboundLocalVariable
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

            armor_effect_descriptions = set(armor_effect_descriptions)
            armor_effect_descriptions = list(armor_effect_descriptions)

            for armor_effect in armor_effect_descriptions:
                head_string = (head_string + armor_effect +
                               str(abs(armor_effect_amounts[armor_effect_descriptions.index(armor_effect)])) + "\n")

            head_string = head_string + "Current equips:"
            return ['Head: {}'.format(self.current_equips['head'].name),
                    'Chest: {}'.format(self.current_equips['chest'].name),
                    'Legs: {}'.format(self.current_equips['legs'].name),
                    'Left Hand: {}'.format(self.current_equips['left hand'].name),
                    'Right Hand: {}'.format(self.current_equips['right hand'].name)], head_string

    class Moves:
        # A collection of all possible moves
        # The general blueprint is:
        # does an action based on why made the move (caster)
        # creates a string to add to the action log and returns it
        def __init__(self, parent):
            self.parent = parent
            self.unlocked_Moves = {}
            self.supported_moves = {
                     self.calming_heal:
                     {
                             'type': 'heal',
                     },
                     self.intense_heal:
                     {
                             'type': 'heal',
                     }
                 }

        def add_move(self, new_move):
            if new_move in self.supported_moves:
                if new_move not in self.unlocked_Moves:
                    self.unlocked_Moves[new_move] = {}
                    self.unlocked_Moves[new_move]['type'] = self.supported_moves[new_move]['type']
                else:
                    return 2
            else:
                error_logger.error("unknown move: {} at add_move".format(new_move.__name__))

        def calming_heal(self):
            if self.parent.current_mp < 5:
                if self.parent == player:
                    return "You do not have enough mp to use this move"
                else:
                    return
            else:
                self.parent.current_mp -= 5
            amount_healed = int((self.parent.current_hp / 5) + (self.parent.max_hp / 10))
            amount_healed = int(amount_healed * ((self.parent.calculate_stat_change(
                                                  Stats.intelligence, self.parent.intelligence) / 100) + 1))
            self.parent.current_hp += amount_healed
            if self.parent.current_hp >= self.parent.max_hp:
                self.parent.current_hp = self.parent.max_hp
            awareness_bonus = 20
            self.parent.awareness += awareness_bonus
            if self == player.moves:
                if GameMaster.settings['nerd mode']:
                    return "You heal for {} hp and your awareness increases by {}".format(amount_healed,
                                                                                          awareness_bonus)
                else:
                    return "You heal for {} hp and feel a bit calmer".format(amount_healed)
            else:
                if self.parent.gender == "male":
                    gender_pronoun = "his"
                else:
                    gender_pronoun = "her"
                if GameMaster.settings['nerd mode']:
                    return "{} heals {} hp and {} awareness is raised by {}".format(self.parent.first_name,
                                                                                    amount_healed,
                                                                                    gender_pronoun,
                                                                                    awareness_bonus)
                else:
                    return "{} heals for {} hp and becomes calmer".format(self.parent.first_name, amount_healed)

        def intense_heal(self):
            if self.parent.current_mp < 7:
                if self.parent == player:
                    return "You do not have enough mp to use this move"
                else:
                    return

            else:
                self.parent.current_mp -= 7
            amount_healed = int((self.parent.current_hp / 3) + (self.parent.max_hp / 4))
            amount_healed = int(amount_healed * ((self.parent.calculate_stat_change(
                                                  Stats.intelligence, self.parent.intelligence) / 100) + 1))

            self.parent.current_hp += amount_healed
            if self.parent.current_hp >= self.parent.max_hp:
                self.parent.current_hp = self.parent.max_hp
            if self == player.moves:
                return "You heal for {} hp".format(amount_healed)
            else:
                return "{} enemy heals for {} hp".format(self.parent.first_name, amount_healed)

    def apply_status(self, status, duration=0, effect_amount=0):
        stat_statuses = ('crit', 'prot', 'intelligence', 'dodge', 'strength', 'charisma')
        if status in supported_Statuses:
            if status in self.Statuses:
                if status == Statuses.stun:
                    pass
                else:
                    self.Statuses[status]['amount'] += effect_amount
                self.Statuses[status]['duration'] += duration
            else:
                if status == Statuses.stun:
                    self.Statuses[status] = {}
                    self.Statuses[status]['duration'] = duration
                else:
                    self.Statuses[status] = {}
                    self.Statuses[status]['duration'] = duration
                    self.Statuses[status]['amount'] = effect_amount

        elif status in stat_statuses:
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

    speed_levels = {90: "fast as fuck boiii", 80: "fast", 70: "fleet",
                    40: "tired", 30: "sluggish", 20: "injured"}

    crit_levels = {33: 'very likely', 20: 'highly likely', 10: 'likely', 5: 'unlikely', 2: 'very unlikely'}

    dodge_levels = {80: 'very likely', 60: 'highly likely', 45: 'likely', 20: 'unlikely', 10: 'very unlikely'}

    prot_levels = {80: 'the majority', 60: 'a big part of', 45: 'half', 20: 'a small bit', 10: 'very little'}

    def stat_level(self, stat, custom_stat=None):
        if stat == "crit":
            stat = self.calculate_stat_change(Stats.crit, self.crit)
            stat_levels = self.crit_levels

        elif stat == "awareness":
            stat = self.calculate_stat_change(Stats.awareness, self.awareness)
            stat_levels = self.awareness_levels

        elif stat == "speed":
            stat = self.calculate_stat_change(Stats.speed, self.speed)
            stat_levels = self.speed_levels

        elif stat == "dodge":
            stat = self.calculate_stat_change(Stats.dodge, self.dodge)
            stat_levels = self.dodge_levels

        elif stat == "prot":
            stat = self.calculate_stat_change(Stats.prot, self.prot)
            stat_levels = self.prot_levels

        else:
            error_logger.error("Unknown stat: {}".format(stat))
            stat_levels = {0: 'Something failed, please send your logs to the dev'}
            stat = 0

        if custom_stat is None:
            return stat_levels[closest_match(stat, stat_levels)]
        else:
            return stat_levels[closest_match(custom_stat, stat_levels)]

    def deal_damage(self, damage):
        self.current_enemy.current_hp -= damage
        if self.current_enemy.current_hp <= 0 and self.current_enemy != player:
            player.loot_drop()

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
            if GameMaster.settings['nerd mode']:
                status_string = ""
                temp_descritions = []
                for status in self.Statuses:
                    if status in supported_Statuses:
                        new_status = ""
                        new_status += "{}: ".format(supported_Statuses[status]['description_nerd'])
                        try:
                            if self.Statuses[status]['duration'] > 1:
                                end = "s"
                            else:
                                end = ""

                            duration = self.Statuses[status]['duration']
                        except KeyError:
                            error_logger.error("Status with unknown duration: {}, a {}'s statuses {}"
                                               .format(self.name, self.__class__.__name__, self.Statuses))
                            duration = "?"
                            end = "s"

                        new_status += "{} turn{}".format(duration, end)
                    else:
                        new_status = "{} increased by {} for {} turn".format(status.capitalize(),
                                                                             self.Statuses[status]['amount'],
                                                                             self.Statuses[status]['duration'])
                        if self.Statuses[status]['duration'] > 1:
                            end = "s"
                        else:
                            end = ""

                        new_status += end

                    temp_descritions.append(new_status)

                counter = 0
                for status in temp_descritions:
                    counter += 1
                    if temp_descritions.index(status) == 0:
                        status_string += status
                    else:
                        if counter >= 3:
                            try:
                                _ = temp_descritions[temp_descritions.index(status) + 1]
                                del _
                                status_string += ", {}\n".format(status)
                                counter = 0
                            except IndexError:
                                status_string += ", {}".format(status)
                                counter = 0
                        else:
                            if status.endswith("\n"):
                                status_string += status
                            else:
                                status_string += ", {}".format(status)

                if self == player:
                    current_states = "\nCurrent statuses:\n{}".format(status_string)
                else:
                    current_states = "\n{}s statuses:\n{}".format(self.first_name.capitalize(), status_string)

            else:
                status_descriptions = []
                for status in self.Statuses:
                    if status in supported_Statuses:
                        status_descriptions.append(supported_Statuses[status]['description'])
                    else:
                        new_status = "{} is {} increased by {} for {} turn".format(("your" if self == player else
                                                                                    gender_pronoun_1),
                                                                                   status.capitalize(),
                                                                                   self.Statuses[status]['amount'],
                                                                                   self.Statuses[status]['duration'])
                        if self.Statuses[status]['duration'] > 1:
                            end = "s"
                        else:
                            end = ""

                        new_status += end
                        status_descriptions.append(new_status)

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

                if self == player:
                    current_states = "\nYou are {}".format(status_string)
                else:
                    current_states = "\n{} is {}".format(self.first_name.capitalize(), status_string)

        else:
            # If the enemy is not afflicted, an empty string will be returned to be used
            current_states = ""

        # Applying buffs and debuffs to the values
        temp_speed = self.calculate_stat_change(Stats.speed, self.speed)
        temp_awareness = self.calculate_stat_change(Stats.awareness, self.awareness)
        temp_strength = self.calculate_stat_change(Stats.strength, self.strength)
        temp_intelligence = self.calculate_stat_change(Stats.intelligence, self.intelligence)
        temp_dodge = self.calculate_stat_change(Stats.dodge, self.dodge)
        temp_prot = self.calculate_stat_change(Stats.prot, self.prot)
        temp_crit = self.calculate_stat_change(Stats.crit, self.crit)
        temp_hp_regen = self.calculate_stat_change(Stats.hp_regen, self.hp_regen)
        temp_mp_regen = self.calculate_stat_change(Stats.mp_regen, self.mp_regen)
        temp_stamina_regen = self.calculate_stat_change(Stats.stamina_regen, self.stamina_regen)
        temp_charisma = self.calculate_stat_change(Stats.charisma, self.charisma)

        # Joining all the string together
        # Different depending on if the target is the player or the enemy
        if isinstance(target, Player):
            if GameMaster.settings['nerd mode']:
                # noinspection PyUnresolvedReferences
                return ("Level: {}, xp: {}.\n"
                        "Hp: {}/{}, mp: {}/{}, stamina: {}/{}.\n"
                        "Hp regen: {}, mp regen: {}, stamina regen: {}.\n"
                        "Strength: {}, intelligence: {}, crit: {}%.\n"
                        "Prot: {}%, dodge: {}%, speed: {}, awareness: {}, charisma: {}."
                        "{}"
                        .format(self.level, self.xp, self.current_hp, self.max_hp, self.current_mp, self.max_mp,
                                self.current_stamina, self.max_stamina,
                                temp_hp_regen, temp_mp_regen, temp_stamina_regen,
                                temp_strength, temp_intelligence, temp_crit, temp_prot, temp_dodge,
                                temp_speed, temp_awareness, temp_charisma, current_states))

            else:
                # noinspection PyUnresolvedReferences
                return ("You are level {} and you have {} xp. You have {}/{} hp, {}/{} mp and {}/{} stamina.\n"
                        "You will regain {} hp, {} mp and {} stamina at the start of your turn.\n"
                        "Your current strength is {}, your intelligence is {} and your attacks' damage are {} to be "
                        "doubled.\n"
                        "You are currently {} and {}.\nYou will block {} of incoming attacks and are {} to dodge them."
                        "{}"
                        .format(self.level, self.xp, self.current_hp, self.max_hp, self.current_mp, self.max_mp,
                                self.current_stamina, self.max_stamina, self.hp_regen, self.mp_regen,
                                self.stamina_regen, temp_strength, temp_intelligence, self.stat_level(Stats.crit),
                                self.stat_level(Stats.awareness),
                                self.stat_level(Stats.speed), self.stat_level(Stats.prot),
                                self.stat_level(Stats.dodge), current_states))

        else:
            if GameMaster.settings['nerd mode']:
                if self.__class__.__name__[0] in GameMaster.vowels:
                    prefix = "An"
                else:
                    prefix = "A"

                # noinspection PyUnresolvedReferences
                return("{} {}, Rank {}.\n"
                       "Hp: {}/{}, mp: {}/{}, stamina: {}/{}.\n"
                       "Hp regen: {}, mp regen: {}, stamina regen: {}.\n"
                       "Strength: {}, intelligence: {}, crit: {}%.\n"
                       "Prot: {}%, dodge: {}%, speed: {}, awareness: {}, charisma: {}."
                       "{}"
                       .format(prefix, self.__class__.__name__, self.rank, self.current_hp, self.max_hp,
                               self.current_mp, self.max_mp, self.current_stamina, self.max_stamina,
                               temp_hp_regen, temp_mp_regen, temp_stamina_regen,
                               temp_strength, temp_intelligence, temp_crit, temp_prot, temp_dodge,
                               temp_speed, temp_awareness, temp_charisma, current_states))

            else:
                return ("{}: {}.\n{} has {}/{} hp, {}/{} mp and {}/{} stamina.\n{} will regain {} hp, {} mp and {} "
                        "stamina at the start of {} turn.\n"
                        "{} strength is {}, {} intelligence is {} and {} attacks' damage are {} to be doubled.\n"
                        "{} is currently {} and {}.\n{} will block {} of your attacks and is {} to dodge them.{}"
                        .format
                        (self.name, self.description, self.name, self.current_hp, self.max_hp, self.current_mp,
                         self.max_mp, self.current_stamina, self.max_stamina, gender_pronoun_2.capitalize(),
                         self.hp_regen, self.mp_regen, self.stamina_regen, gender_pronoun_1,
                         gender_pronoun_1.capitalize(), temp_strength, gender_pronoun_1, temp_intelligence,
                         gender_pronoun_1.capitalize(), self.stat_level(Stats.crit),
                         gender_pronoun_2.capitalize(), self.stat_level(Stats.speed), self.stat_level(Stats.awareness),
                         gender_pronoun_2.capitalize(), self.stat_level(Stats.prot), self.stat_level(Stats.dodge),
                         current_states))


class Player(Character):
    # noinspection PyMissingConstructor
    def __init__(self, name, gender):
        self.level = 1
        self.xp = 0
        super(Player, self).__init__(name, gender, random.randint(20, 80), random.randint(50, 80),
                                     random.randint(5, 10), random.randint(0, 5), random.randint(1, 5),
                                     random.randint(5, 10), random.randint(70, 100), random.randint(25, 30),
                                     random.randint(10, 15), random.randint(10, 15),
                                     1 if random.randint(0, 100) > 80 else 0,
                                     random.randint(1, 3), random.randint(1, 3), random.randint(5, 10))

    def loot_drop(self):
        print('You successfully defeated {}!'.format(self.current_enemy))
        dropped_items = {}
        if Gold.rarity >= random.randint(0, 100):
            dropped_items[Gold] = random.randint(self.current_enemy.rank * 25, self.current_enemy.rank * 100)
        for drop in self.current_enemy.drops:  # last
            if drop.rarity >= random.randint(0, 100):
                dropped_items[drop] = int(drop.rarity * (self.current_enemy.rank * 0.5))

    def alive_check(self):
        if self.current_hp <= 0:
            if GameMaster.last_damage_player != "":
                self.dead(GameMaster.last_damage_player)
            else:
                error_logger.error("Player Took Undocumented Damage")
                self.dead()

    @staticmethod
    def dead(killer=None, custom_text: str = ''):
        Console.clear()
        if custom_text != '':
            print(custom_text)
        else:
            if killer is not None:
                print("You were killed by {}.".format(killer))
            else:
                print("You died")
        time.sleep(5)
        main_menu()


class Enemy(Character):
    def alive_check(self):
        if self.current_hp <= 0:
            pass
        # todo call to player xp add and loot drop


class Orc(Enemy):
    def __init__(self, rank: int, name: str, gender, description: str, dodge: int, speed: int, intelligence: int,
                 prot: int, crit, awareness: int, *drops, injured: float = False):

        self.rank = rank
        max_hp = int(player.max_hp * (rank * 0.7)) + (random.randint(-int(player.max_hp * 0.2),
                                                                     int(player.max_hp * 0.4)))

        max_mp = int(player.max_mp * (rank * 0.3)) + (random.randint(-int(player.max_mp * 0.5),
                                                                     int(player.max_mp * 0.2)))

        max_stamina = int(player.max_stamina * (rank * 0.7)) + (random.randint(-int(player.max_stamina * 0.3),
                                                                               int(player.max_stamina * 0.4)))

        hp_regen = round(random.randint(-int(player.hp_regen * (rank * 0.8)),
                                        int(player.hp_regen * (rank * 0.3))))

        mp_regen = random.randint(-int(player.mp_regen * (rank * 0.7),
                                  int(player.mp_regen * (rank * 0.3))))

        stamina_regen = random.randint(-int(player.stamina_regen * (rank * 0.5)),
                                       int(player.stamina_regen * (rank * 0.3)))

        if max_mp < 10:
            max_mp = 10

        if max_stamina < 10:
            max_stamina = 10

        if hp_regen < 0:
            hp_regen = 0

        if stamina_regen < 0:
            stamina_regen = 0

        if mp_regen < 0:
            mp_regen = 0

        strength = round(player.max_hp * (rank * 0.1)) + rank * 2

        dodge += random.randint(-20, -40)
        if dodge < 0:
            dodge = 0

        prot += random.randint(15, 50)
        if prot > 80:
            prot = 80

        intelligence += random.randint(-20, -70)
        if intelligence < 0:
            intelligence = 0

        charisma = 0

        self.drops = []
        for item in drops:
            self.drops.append(item)
        super(Orc, self).__init__(name, gender, dodge, speed, intelligence, prot, crit, charisma, awareness, max_hp,
                                  max_stamina, max_mp, hp_regen, stamina_regen, mp_regen, strength,
                                  description=description)

        self.current_hp += random.randint(round(-3 * (self.rank * 0.5)), round(5 * (self.rank * 0.5)))

        if self.current_hp > self.max_hp:
            self.current_hp = self.max_hp

        if injured:
            self.current_hp = int(self.current_hp * injured)

    resistances = {
        Statuses.apply_bleed: 0,
    }


class Animal(Enemy):
    def __init__(self, rank: int, name: str, gender, description: str, dodge: int, speed: int, intelligence: int,
                 prot: int, crit, awareness: int, *drops, injured: float = False):

        self.rank = rank
        max_hp = int(player.current_hp * (rank * 0.4)) + (random.randint(-int(player.max_hp * 0.3),
                                                                         int(player.max_hp * 0.25)))

        max_mp = int(player.max_mp * (rank * 0.2)) + (random.randint(-int(player.max_mp * 0.5),
                                                                     int(player.max_mp * 0.2)))

        max_stamina = int(player.max_stamina * (rank * 0.7)) + (random.randint(-int(player.max_stamina * 0.3),
                                                                               int(player.max_stamina * 0.4)))

        hp_regen = round(random.randint(-int(player.hp_regen * (rank * 0.8)),
                                        int(player.hp_regen * (rank * 0.3))))

        mp_regen = random.randint(-int(player.mp_regen * (rank * 0.7)),
                                  int(player.mp_regen * (rank * 0.3)))

        stamina_regen = random.randint(-int(player.stamina_regen * (rank * 0.4)),
                                       int(player.stamina_regen * (rank * 0.4)))

        if max_mp < 10:
            max_mp = 10

        if max_stamina < 10:
            max_stamina = 10

        if hp_regen < 0:
            hp_regen = 0

        if stamina_regen < 0:
            stamina_regen = 0

        if mp_regen < 0:
            mp_regen = 0

        charisma = 0

        strength = round(player.max_hp * (rank * 0.1)) + rank * 2

        self.drops = []
        for item in drops:
            self.drops.append(item)
        super(Animal, self).__init__(name, gender, dodge, speed, intelligence, prot, crit, charisma, awareness, max_hp,
                                     max_stamina, max_mp, hp_regen, stamina_regen, mp_regen,
                                     strength, description=description)

        self.current_hp += random.randint(round(-3 * (self.rank * 0.5)), round(5 * (self.rank * 0.5)))

        if self.current_hp > self.max_hp:
            self.current_hp = self.max_hp

        if injured:
            self.current_hp = int(self.current_hp * injured)

    resistances = {
        Statuses.apply_bleed: 0,
    }


class Human(Enemy):
    def __init__(self, rank: int, name: str, gender, description: str, dodge: int, speed: int, intelligence: int,
                 prot: int, crit, awareness: int, *drops, injured: float = False):

        self.rank = rank
        max_hp = int(player.current_hp * (rank * 0.5)) + (random.randint(-int(player.max_hp * 0.3),
                                                                         int(player.max_hp * 0.3)))

        max_mp = int(player.max_mp * (rank * 0.7)) + (random.randint(-int(player.max_mp * 0.3),
                                                                     int(player.max_mp * 0.5)))

        max_stamina = int(player.max_stamina * (rank * 0.5)) + (random.randint(-int(player.max_stamina * 0.2),
                                                                               int(player.max_stamina * 0.4)))

        hp_regen = round(random.randint(-int(player.hp_regen * (rank * 0.8)),
                                        int(player.hp_regen * (rank * 0.3))))

        mp_regen = random.randint(-int(player.mp_regen * (rank * 0.2),
                                  int(player.mp_regen * (rank * 0.6))))

        stamina_regen = random.randint(-int(player.stamina_regen * (rank * 0.5)),
                                       int(player.stamina_regen * (rank * 0.4)))

        if max_mp < 10:
            max_mp = 10

        if max_stamina < 0:
            max_stamina = 0

        if hp_regen < 0:
            hp_regen = 0

        if stamina_regen < 0:
            stamina_regen = 0

        if mp_regen < 0:
            mp_regen = 0

        strength = round(player.max_hp * (rank * 0.1)) + rank * 2

        dodge += random.randint(-10, 25)
        if dodge < 0:
            dodge = 0

        prot += random.randint(10, -10)
        if prot > 80:
            prot = 80

        intelligence += random.randint(round(rank * 5), round(rank * 20))
        if intelligence < 0:
            intelligence = 0

        charisma = player.charisma + 10
        if charisma > 100:
            charisma = 100

        self.drops = []
        for item in drops:
            self.drops.append(item)
        super(Human, self).__init__(name, gender, dodge, speed, intelligence, prot, crit, charisma, awareness,  max_hp,
                                    max_stamina, max_mp, hp_regen, stamina_regen, mp_regen,
                                    strength, description=description)

        self.current_hp += random.randint(round(-3 * (self.rank * 0.5)), round(5 * (self.rank * 0.5)))

        if self.current_hp > self.max_hp:
            self.current_hp = self.max_hp

        if injured:
            self.current_hp = int(self.current_hp * injured)

    resistances = {
        Statuses.apply_bleed: 0,
    }


class Skeleton(Enemy):
    def __init__(self, rank: int, name: str, gender, description: str, dodge: int, speed: int, intelligence: int,
                 prot: int, crit, awareness: int, *drops, injured: float = False):

        self.rank = rank
        max_hp = int(player.max_hp * (rank * 0.3)) + (random.randint(-int(player.max_hp * 0.3),
                                                                     int(player.max_hp * 0.15)))

        max_mp = int(player.max_mp * (rank * 0.2)) + (random.randint(-int(player.max_mp * 0.5),
                                                                     int(player.max_mp * 0.2)))

        max_stamina = int(player.max_stamina * (rank * 1.5)) + (random.randint(-int(player.max_stamina * 0.3),
                                                                               int(player.max_stamina * 0.6)))

        hp_regen = round(random.randint(-int(player.hp_regen * (rank * 0.8)),
                                        int(player.hp_regen * (rank * 0.3))))

        mp_regen = random.randint(-int(player.mp_regen * (rank * 0.7),
                                       int(player.mp_regen * (rank * 0.3))))

        stamina_regen = random.randint(-int(player.stamina_regen * (rank * 0.2),
                                            int(player.stamina_regen * (rank * 0.6))))

        if max_mp < 10:
            max_mp = 10

        if max_stamina < 10:
            max_stamina = 10

        if hp_regen <= 0:
            hp_regen = 0

        if stamina_regen < 0:
            stamina_regen = 0

        if mp_regen < 0:
            mp_regen = 0

        strength = round(player.max_hp * (rank * 0.1)) + rank * 2

        dodge += random.randint(10, 25)
        if dodge < 0:
            dodge = 0

        intelligence -= random.randint(round(rank * 3), round(rank * 10))

        prot += random.randint(-10, -50)
        if prot > 80:
            prot = 80

        charisma = 0

        self.drops = []
        for item in drops:
            self.drops.append(item)
        super(Skeleton, self).__init__(name, gender, dodge, speed, intelligence, prot, crit, charisma, awareness,
                                       max_hp, max_stamina, max_mp, hp_regen, stamina_regen, mp_regen,
                                       strength, description=description)

        self.current_hp += random.randint(round(-3 * (self.rank * 0.5)), round(5 * (self.rank * 0.5)))

        if self.current_hp > self.max_hp:
            self.current_hp = self.max_hp

        if injured:
            self.current_hp = int(self.current_hp * injured)

    resistances = {
        Statuses.apply_bleed: 100,
        Statuses.stun: 100
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


def combat(enemy):  # todo location
    # Sets both combatant's current enemy to the others
    # This is used in a couple of places for example to determine the loot offered to the player
    player.current_enemy, enemy.current_enemy = enemy, player
    print("{} approaches!".format(enemy.name))
    GameMaster.turn: int = 1
    first_turn: bool = True

    def player_turn():
        player.current_hp += player.hp_regen
        if player.current_hp > player.max_hp:
            player.current_hp = player.max_hp

        player.current_mp += player.mp_regen
        if player.current_mp > player.max_mp:
            player.current_mp = player.max_mp

        player.current_stamina += player.stamina_regen
        if player.current_stamina > player.max_stamina:
            player.current_stamina = player.max_stamina

        print("player")
        for status in list(player.Statuses):
            player.Statuses[status]['duration'] -= 1
            if player.Statuses[status]['duration'] <= 0:
                del player.Statuses[status]

        for status in list(player.Statuses):
            if status in supported_Statuses:
                if supported_Statuses[status]['apply_type'] == "start_dot":
                    damage = status(player)
                    GameMaster.extend_action_log("{} {} damage.".format
                                                 (supported_Statuses[status]['on_apply_message_player'], damage))
                    GameMaster.last_damage_player = supported_Statuses[status]['type']
                    player.current_hp -= damage
                    player.alive_check()

        def main_choice():

            def execute_move(move_type):
                available_moves = []
                for ability in player.moves.unlocked_Moves:
                    if player.moves.unlocked_Moves[ability]['type'] == move_type:
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
                        move_result: str = available_moves[pretty_moves.index(move)]()
                    else:
                        move_result = None
                    if move_result is not None:
                        GameMaster.extend_action_log(move_result)
                        return True

            Console.clear()
            supported_head_moves = [ColoredString('{}defend{}'.format(colorama.Style.DIM, colorama.Style.NORMAL),
                                                  colored_chars=(len(colorama.Style.DIM) + len(colorama.Style.NORMAL))),
                                    ColoredString('{}heal'.format(colorama.Fore.LIGHTYELLOW_EX),
                                                  colored_chars=len(colorama.Fore.LIGHTYELLOW_EX)),
                                    ColoredString('{}attack'.format(colorama.Fore.LIGHTRED_EX),
                                                  colored_chars=len(colorama.Fore.LIGHTRED_EX)),
                                    ColoredString('{}debuff'.format(colorama.Fore.YELLOW),
                                                  colored_chars=len(colorama.Fore.YELLOW)),
                                    ColoredString('{}buff'.format(colorama.Fore.LIGHTCYAN_EX),
                                                  colored_chars=len(colorama.Fore.LIGHTCYAN_EX)),
                                    'use item(upcoming)', 'inspect', 'help', 'view and edit your inventory', 'settings']
            while True:
                action = Console.interactive_choice(supported_head_moves,
                                                    ColoredString("{}What do you want to do?".format
                                                                  (colorama.Style.BRIGHT),
                                                                  colored_chars=(len(colorama.Style.BRIGHT))),
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
                    while True:
                        inspectable_objects = ['yourself', '{}'.format(player.current_enemy.name)]
                        to_inspect = Console.interactive_choice(inspectable_objects, ('Which one of these do you '
                                                                                      'want to inspect?'),
                                                                battle=True, back_want=True)
                        if to_inspect == "yourself":

                                Console.interactive_choice(["I'm done"], player.inspect(player),
                                                           battle=True)

                        elif to_inspect == "{}".format(player.current_enemy.name):
                            Console.interactive_choice(["I'm done"], player.current_enemy.inspect(enemy),
                                                       battle=True)

                        # Back selected
                        elif to_inspect is None:
                            break

                        else:
                            error_logger.error("Unknown case at inspect: {}".format(to_inspect))

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
                                case_list, head_string = player.inventory.view_equips()
                                # Asking what equip they want to view
                                # We will be using a text changing depending on the equip as the case
                                # Therefore, we will enumerate the cases
                                numbered_case = Console.interactive_choice(case_list, head_string,
                                                                           back_want=True, battle=True,
                                                                           enumerated=True)

                                # noinspection PyUnresolvedReferences
                                def handle_slot(slot: str, joke_text: str = ''):
                                    armor_slots = ('head', 'chest', 'legs')
                                    hand_slots = ('left hand', 'right hand')
                                    if slot in armor_slots:
                                        equipment_header_str = (player.inventory.current_equips
                                                                [slot].parent.get_set_part_description
                                                                (player.inventory.current_equips[slot], player))

                                    elif slot in hand_slots:
                                        equipment_header_str = (player.inventory.current_equips[slot].inspect())

                                    else:
                                        error_logger.error("Unknown slot type at handle_slot: {}".format(slot))
                                        equipment_header_str = 'Sorry, something failed miserably and it has been noted'

                                    slot_actions = []
                                    if not player.inventory.current_equips[slot] in GameMaster.Bare_set:
                                        slot_actions.append('Throw away')
                                    if not player.inventory.current_equips[slot] == Fist:
                                        slot_actions.append('Unequip')

                                    decision = Console.interactive_choice(slot_actions,
                                                                          equipment_header_str,
                                                                          battle=True, back_want=True)

                                    if decision == "Unequip":
                                        if not player.inventory.current_equips[slot] in GameMaster.Bare_set:
                                            player.inventory.unequip(slot)
                                        else:
                                            player.dead(None, custom_text=joke_text)

                                    elif decision == "Throw away":
                                        player.inventory.throw_away(slot)

                                # The equivalent of head
                                if numbered_case == 0:
                                    if player.inventory.current_equips['head'] == Bare.Head:
                                        handle_slot('head', joke_text='You dismember your own head and die immediately')
                                    else:
                                        handle_slot('head')

                                # The equivalent of chest
                                elif numbered_case == 1:
                                    if player.inventory.current_equips['chest'] == Bare.Chest:
                                        handle_slot('chest',
                                                    joke_text='How do you even manage to dismember your whole torso?!')
                                    else:
                                        handle_slot('chest')

                                # The equivalent of legs
                                elif numbered_case == 2:
                                    if player.inventory.current_equips['legs'] == Bare.Legs:
                                        handle_slot('legs',
                                                    joke_text='You dismember your legs and slowly die from blood loss')
                                    else:
                                        handle_slot('legs')

                                # The equivalent of left hand
                                elif numbered_case == 3:
                                    handle_slot('left hand')

                                # The equivalent of right hand
                                elif numbered_case == 4:
                                    handle_slot('right hand')

                                # Back
                                elif numbered_case is None:
                                    break

                        elif case_inventory == "Items":
                            while True:
                                head_string, inventory_items = player.inventory.view()
                                raw_inventory_items = player.inventory.view_raw_names()
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
                                        if hasattr(raw_inventory_items[inventory_items.index(item_to_inspect)],
                                                   'parent'):
                                            description = (raw_inventory_items[inventory_items.index(item_to_inspect)].
                                                           parent.inspect())
                                        else:
                                            description = (raw_inventory_items[inventory_items.index(item_to_inspect)].
                                                           inspect())
                                    else:
                                        description = "Something went wrong under Inventory -> items"
                                        error_logger.error('item_to_inspect changed')

                                # Making a list of the possible ways to interact with the item
                                item_actions = ["throw away"]

                                # If the item is some sort of armor, you can equip it
                                if (hasattr(raw_inventory_items[inventory_items.index(item_to_inspect)], "parent") or
                                        isinstance(raw_inventory_items[inventory_items.index(item_to_inspect)],
                                                   Weapon)):
                                    item_actions.append("equip")

                                while True:
                                    item_interaction = Console.interactive_choice(item_actions, description,
                                                                                  battle=True, back_want=True)

                                    if item_interaction is None:
                                        break
                                    elif item_interaction == "throw away":
                                        thrown_away = player.inventory.throw_away(raw_inventory_items
                                                                                  [inventory_items.index
                                                                                   (item_to_inspect)])
                                        if thrown_away == "all":
                                            break
                                    elif item_interaction == "equip":
                                        if isinstance(raw_inventory_items[inventory_items.index(item_to_inspect)],
                                                      Weapon):
                                            hand = Console.interactive_choice(['left hand', 'right hand'],
                                                                              'With which hand do you want to use this '
                                                                              'item with?', back_want=True, battle=True)

                                            if hand is None:
                                                hand = ""
                                        else:
                                            hand = ""
                                        result = player.inventory.equip(raw_inventory_items
                                                                        [inventory_items.index
                                                                         (item_to_inspect)], hand=hand)
                                        if result == 1:
                                            break
                                        else:
                                            error_logger.error("Unexpected result: {}".format(result))
                                    else:
                                        error_logger.error("Unknown item interaction: {}".format(item_interaction))

                # The equivalent of settings
                elif action == 9:
                    def save_settings():
                        project_path = os.path.abspath("")
                        with open("{}\\Saves\\Config\\Config.json".format(project_path), 'w') as f:
                            json.dump(GameMaster.settings, f)

                    while True:
                        setting_list = []
                        for key in GameMaster.settings:
                            if key == "ForceV2":
                                if GameMaster.settings[key] is None:
                                    display_key = False
                                else:
                                    display_key = True
                            else:
                                display_key = True

                            if display_key:
                                setting_list.append("{}: {}".format(key, '{}On{}'.format(colorama.Fore.GREEN,
                                                                                         colorama.Style.RESET_ALL)
                                                    if GameMaster.settings[key] else
                                                    '{}Off{}'.format(colorama.Fore.RED, colorama.Style.RESET_ALL)))

                        setting_to_be_changed = Console.interactive_choice(setting_list,
                                                                           "Click on any of these to change them\n"
                                                                           "Disabling Quickedit makes the game sort of "
                                                                           "unplayable",
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

                        # Quickedit case
                        elif setting_to_be_changed == 1:
                            if not GameMaster.settings['Quickedit']:
                                new_setting = 1
                                safe_registry_edit = True
                                GameMaster.settings['Quickedit'] = new_setting
                            elif GameMaster.settings['Quickedit']:
                                new_setting = 0
                                safe_registry_edit = True
                                GameMaster.settings['Quickedit'] = new_setting
                            else:
                                (error_logger.error("Illegal case in settings nerd mode:{}"
                                                    .format(GameMaster.settings['Quickedit'])))
                                safe_registry_edit = False
                                new_setting = 0

                            if safe_registry_edit:
                                try:
                                    path = "Console\\%SystemRoot%_py.exe"
                                    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, path, 0, winreg.KEY_WRITE)
                                    winreg.SetValueEx(key, "Quickedit", 0, winreg.REG_DWORD, new_setting)
                                    winreg.CloseKey(key)
                                except WindowsError:
                                    path = "Console"
                                    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, path, 0, winreg.KEY_WRITE)
                                    winreg.SetValueEx(key, "Quickedit", 0, winreg.REG_DWORD, new_setting)
                                    winreg.CloseKey(key)
                            save_settings()

                        # ForceV2 case
                        elif setting_to_be_changed == 2:
                            if not GameMaster.settings['ForceV2']:
                                new_setting = 1
                                safe_registry_edit = True
                                GameMaster.settings['ForceV2'] = new_setting
                            elif GameMaster.settings['ForceV2']:
                                new_setting = 0
                                safe_registry_edit = True
                                GameMaster.settings['ForceV2'] = new_setting
                            else:
                                (error_logger.error("Illegal case in settings ForceV2:{}"
                                                    .format(GameMaster.settings['Quickedit'])))
                                safe_registry_edit = False
                                new_setting = 0

                            if safe_registry_edit:
                                path = "Console"
                                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, path, 0, winreg.KEY_WRITE)
                                winreg.SetValueEx(key, "ForceV2", 0, winreg.REG_DWORD, new_setting)
                                winreg.CloseKey(key)
                            save_settings()

                        else:
                            error_logger.error("Unknown case in settings to edit: {}".format(setting_to_be_changed))

        # Calls the player's main choice
        # The call is way back here because the code it depends on need to be declared
        main_choice()

    def enemy_turn():
        enemy.current_hp += enemy.hp_regen
        if enemy.current_hp > enemy.max_hp:
            enemy.current_hp = enemy.max_hp

        enemy.current_mp += enemy.mp_regen
        if enemy.current_mp > enemy.max_mp:
            enemy.current_mp = enemy.max_mp

        enemy.current_stamina += enemy.stamina_regen
        if enemy.current_stamina > enemy.max_stamina:
            enemy.current_stamina = enemy.max_stamina

        enemy.deal_damage(enemy.strength)
        result = enemy.Moves.calming_heal(enemy.moves)
        if result is not None:
            GameMaster.extend_action_log(result)
        print("enemy")
        print("\n")
        time.sleep(1)

    while True:
        if first_turn:
            if (player.awareness + random.randint(0, 100)) >= (
                    player.current_enemy.awareness + random.randint(0, 100)):
                player_first = True
            else:
                player_first = False

            first_turn = False
        else:
            GameMaster.turn += 1
            temp_player_speed = player.calculate_stat_change(Stats.speed, player.speed)
            temp_enemy_speed = enemy.calculate_stat_change(Stats.speed, enemy.speed)

            if random.randint(random.randint(int((temp_player_speed / 3)), (temp_player_speed - 10)),
                              temp_player_speed * 2) >= \
                    random.randint(random.randint(int((temp_enemy_speed / 3)), (temp_enemy_speed - 10)),
                                   temp_enemy_speed * 2):
                player_first = True
            else:
                player_first = False

        if player_first:
            if Statuses.stun in player.Statuses:
                GameMaster.extend_action_log(supported_Statuses[Statuses.stun]['on_apply_message_player'])
                player.Statuses[Statuses.stun]['duration'] -= 1
                if player.Statuses[Statuses.stun]['duration'] <= 0:
                    del player.Statuses[Statuses.stun]
            else:
                player_turn()

            if Statuses.stun in player.current_enemy.Statuses:
                GameMaster.extend_action_log(supported_Statuses[Statuses.stun]
                                             ['on_apply_message_enemy'].format(enemy.name))
                enemy.Statuses[Statuses.stun]['duration'] -= 1
                if enemy.Statuses[Statuses.stun]['duration'] <= 0:
                    del enemy.Statuses[Statuses.stun]
            else:
                enemy_turn()

        else:
            if Statuses.stun in player.current_enemy.Statuses:
                GameMaster.extend_action_log(supported_Statuses[Statuses.stun]
                                             ['on_apply_message_enemy'].format(enemy.name))
                enemy.Statuses[Statuses.stun]['duration'] -= 1
                if enemy.Statuses[Statuses.stun]['duration'] <= 0:
                    del enemy.Statuses[Statuses.stun]
            else:
                enemy_turn()

            if Statuses.stun in player.Statuses:
                GameMaster.extend_action_log(supported_Statuses[Statuses.stun]['on_apply_message_player'])
                player.Statuses[Statuses.stun]['duration'] -= 1
                if player.Statuses[Statuses.stun]['duration'] <= 0:
                    del player.Statuses[Statuses.stun]
            else:
                player_turn()


def on_start():
    # Defining this projects path
    project_path = os.path.dirname(sys.argv[0])

    # Setting the name of the game
    GameMaster.game_name = "Temporary placeholder for a game name, please change later"

    Console.size_reset()

    try:
        os.mkdir("{}\\Saves".format(project_path))
    except FileExistsError:
        pass

    try:
        os.mkdir("{}\\Logs".format(project_path))
    except FileExistsError:
        pass

    try:
        os.mkdir("{}\\Saves\\Player saves".format(project_path))
    except FileExistsError:
        pass

    try:
        os.mkdir("{}\\Saves\\Config".format(project_path))
    except FileExistsError:
        pass

    # A function for creating loggers
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

    # Debug logger
    debug_log = setup_logger('Debug Logging', "{}\\Logs\\debug_log.log".format(project_path), level=logging.DEBUG)

    # A json structure to be filled with info about things
    setup = '''
    {
        "os": null,
        "font_size_x": null,
        "font_size_y": null
    }
    '''
    setup = json.loads(setup)

    # The versions i am supporting
    # This is basically information about the fallback size of the console, used in interactive choices
    accepted_operating_systems = ('Windows-8', 'Windows-10', 'Windows-8.1')

    supported_os = True
    os_version = platform.platform(terse=True)
    if os_version in accepted_operating_systems:
        setup['os'] = os_version
    else:
        setup['os'] = os_version
        supported_os = False
        error_log.error("Unsupported os: {}. Falling back to windows 10 settings".format(os))

    # Getting the console's font size
    # Done using the win32 api
    ctypes.windll.kernel32.SetConsoleTitleW(GameMaster.game_name)

    error = ctypes.windll.kernel32.GetLastError()
    if error:
        hwnd = win32gui.GetForegroundWindow()
        win32gui.SetWindowText(hwnd, GameMaster.game_name)

    class COORD(ctypes.Structure):
        _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]

    # noinspection PyPep8Naming
    class CONSOLE_FONT_INFO(ctypes.Structure):
        _fields_ = [("nFont", ctypes.c_uint32),
                    ("dwFontSize", COORD)]

    font = CONSOLE_FONT_INFO()

    # noinspection PyPep8Naming
    STD_OUTPUT_HANDLE = -11
    handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    ctypes.windll.kernel32.GetCurrentConsoleFont(
        handle,
        ctypes.c_long(False),
        ctypes.pointer(font))

    setup['font_size_x'] = font.dwFontSize.X
    setup['font_size_y'] = font.dwFontSize.Y

    if font.dwFontSize.X == 0 and font.dwFontSize.Y == 0:
        error_log.error("Get font size error: msdn error {}".format(ctypes.windll.kernel32.GetLastError()))

    # Asserting that all audio files exist
    audio_path = "{}\\Audio\\".format(project_path)
    audio_files = ("abc_123_a.ogg",)
    missing_audio_files = []
    for audio_name in audio_files:
        if not os.path.isfile(audio_path + audio_name):
            GameMaster.missing_audio.append(audio_name)
            missing_audio_files.append(audio_path)

    if not len(missing_audio_files) == 0:
        missing_files_str = ", ".join(missing_audio_files)
        missing_files_str = "Missing auido:" + missing_files_str
        error_log.error(missing_files_str)

    # We only want to meddle with the registry if we know what we are dealing with
    if supported_os:
        # Reading the user's initial values set for the console in case they want to reverse it later
        py_exe_installed = False
        try:
            registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Console\\%SystemRoot%_py.exe", 0,
                                          winreg.KEY_READ)
            quickedit_py_exe, __ = winreg.QueryValueEx(registry_key, "Quickedit")
            winreg.CloseKey(registry_key)
            py_exe_installed = True
        except WindowsError:
            pass
        finally:
            try:
                registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Console", 0,
                                              winreg.KEY_READ)
                quickedit_cmd, __ = winreg.QueryValueEx(registry_key, "Quickedit")
                winreg.CloseKey(registry_key)
            except WindowsError:
                quickedit_cmd = 0

        try:
            registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Console", 0,
                                          winreg.KEY_READ)
            legacy, __ = winreg.QueryValueEx(registry_key, "ForceV2")
            winreg.CloseKey(registry_key)
        except WindowsError:
            legacy = None

        # Setting registry values of the console for an optimized experience
        # If the option to enable legacy console exists, we want do that
        if legacy is not None:
            try:
                path = "Console"
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, path, 0, winreg.KEY_WRITE)
                winreg.SetValueEx(key, "ForceV2", 0, winreg.REG_DWORD, 0)
                winreg.CloseKey(key)
            except WindowsError:
                pass

        # Disabling quickedit
        if py_exe_installed:
            try:
                path = "Console\\%SystemRoot%_py.exe"
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, path, 0, winreg.KEY_WRITE)
                winreg.SetValueEx(key, "Quickedit", 0, winreg.REG_DWORD, 0)
                winreg.CloseKey(key)
            except WindowsError:
                pass
            finally:
                path = "Console"
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, path, 0, winreg.KEY_WRITE)
                winreg.SetValueEx(key, "Quickedit", 0, winreg.REG_DWORD, 0)
                winreg.CloseKey(key)

    else:
        quickedit_cmd = None
        quickedit_py_exe = None
        legacy = None

    try:
        # noinspection PyUnboundLocalVariable
        temp = quickedit_py_exe
        del temp
    except NameError:
        quickedit_py_exe = 0

    if quickedit_cmd or quickedit_py_exe:
        os.system("start {}\\Scripts\\Restart_game.pyw".format(project_path))

    if quickedit_cmd or quickedit_py_exe:
        raise SystemExit

    # Dumping the json settings
    try:
        with open("{}\\Saves\\Config\\Config.json".format(project_path), 'x') as _:
            pass
    except FileExistsError:
        pass

    if os.stat("{}\\Saves\\Config\\Config.json".format(project_path)).st_size == 0:
        with open("{}\\Saves\\Config\\Config.json".format(project_path), 'w') as f:
            settings = '''
            {
                "nerd mode": false,
                "Quickedit": null,
                "ForceV2": null
            }
            '''
            settings = json.loads(settings)
            settings['Quickedit'] = quickedit_cmd
            settings['ForceV2'] = legacy
            json.dump(settings, f)
            GameMaster.settings = settings

    else:
        with open("{}\\Saves\\Config\\Config.json".format(project_path), 'r') as f_1:
            test_content = f_1.readlines()
            if test_content[0] == "\n" and len(test_content) == 1:
                with open("{}\\Saves\\Config\\Config.json".format(project_path), 'w') as f_2:
                    settings = '''
                            {
                                "nerd mode": false,
                                "Quickedit": null,
                                "ForceV2": null
                            }
                            '''
                    settings = json.loads(settings)
                    settings['Quickedit'] = quickedit_cmd
                    settings['ForceV2'] = legacy
                    json.dump(settings, f_2)
                    GameMaster.settings = settings

    # Settings up some info depending on the windows version used
    with open("{}\\Saves\\Config\\Config.json".format(project_path)) as f:
        try:
            GameMaster.settings = json.load(f)
        except json.JSONDecodeError as json_error:
            error_log.error("JsonDecodeError: {}".format(json_error))
            settings = '''
                    {
                        "nerd mode": false,
                        "Quickedit": null,
                        "ForceV2": null
                    }
                    '''
            settings = json.loads(settings)
            settings['Quickedit'] = quickedit_cmd
            settings['ForceV2'] = legacy
            GameMaster.settings = settings

    if len(GameMaster.settings) == 0:
        settings = '''
                {
                    "nerd mode": false,
                    "Quickedit": null,
                    "ForceV2": null
                }
                '''
        settings = json.loads(settings)
        settings['Quickedit'] = quickedit_cmd
        settings['ForceV2'] = legacy
        GameMaster.settings = settings

    try:
        with open("{}\\Saves\\Config\\Setup.json".format(project_path), 'x') as _:
            pass
    except FileExistsError:
        pass

    with open("{}\\Saves\\Config\\Setup.json".format(project_path), 'w') as f:
        json.dump(setup, f)

    # Settings up some info depending on the windows version used
    with open("{}\\Saves\\Config\\Setup.json".format(project_path)) as f:
        try:
            config = json.load(f)
            os_version = config['os']
        except json.JSONDecodeError as json_error:
            error_log.error("JsonDecodeError: {}".format(json_error))
            os_version = "Windows-10"
            config = setup

    # Setting information about the font size and the width of the console border
    if len(sys.argv) != 1:
        if sys.argv[1] == "debug":
            GameMaster.font_size_x = 7 if not config['font_size_x'] else config['font_size_x']
            GameMaster.font_size_y = 12 if not config['font_size_y'] else config['font_size_y']
            GameMaster.x_to_console = 9
            GameMaster.y_to_console = 32

    else:
        if os_version == 'Windows-8.1' or os_version == 'Windows-8':
            GameMaster.font_size_x = 8 if not config['font_size_x'] else config['font_size_x']
            GameMaster.font_size_y = 12 if not config['font_size_y'] else config['font_size_y']
            GameMaster.x_to_console = 9
            GameMaster.y_to_console = 32

        elif os_version == 'Windows-10':
            GameMaster.font_size_x = 8 if not config['font_size_x'] else config['font_size_x']
            GameMaster.font_size_y = 16 if not config['font_size_y'] else config['font_size_y']
            GameMaster.x_to_console = 1
            GameMaster.y_to_console = 30

        else:
            # If the user is using an os i'm not yet supporting
            error_log.warning("Unsupported os:{}".format(os_version))

            # Will default to windows 10 settings
            GameMaster.font_size_x = 8
            GameMaster.font_size_y = 16
            GameMaster.x_to_console = 1
            GameMaster.y_to_console = 30

    return error_log, info_log, debug_log


if __name__ == '__main__':
    # Initiating everything
    player = Player('Tester', 'male')
    player.inventory = player.Inventory(player)
    player.moves = player.Moves(player)

    GameMaster = GameMaster()

    # Initiating colorama so that we can color console output
    colorama.init()

    # Setting some variables to be used during runtime
    # Along with setting up some loggers
    error_logger, info_logger, debug_logger = on_start()

    # Debug
    hen = Animal(1, 'Gullbert the hen', 'male', 'A hen', 15, 40, 2, 0, 3, 20)
    hen.inventory = hen.Inventory(hen)
    hen.moves = hen.Moves(hen)
    player.moves.add_move(player.moves.calming_heal)
    player.moves.add_move(player.moves.intense_heal)
    hen.apply_status(Statuses.stun, 10)
    hen.apply_status(Statuses.apply_bleed, 10)
    player.apply_status(Statuses.apply_bleed, 10)
    player.apply_status("crit", 9, 100)
    player.inventory.add_item(Gold, 10)
    combat(hen)
