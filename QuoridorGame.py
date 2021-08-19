# Author: Lyndon Keeling
# Date: 09Aug2021
# Description: portfolio-project | LastEdit: 09Aug2021 | Quoridor.py | Due 12Aug2021 |
# portfolio project for CS162. Quoridor is a game where each player begins on opposite sides and per turn
# are able to do one of two things, move their pawn, or place a fence. There is a limit of 10 fences which
# may be places. Pawns may move in 4 directions, if a pawn faces each other,  they are able to jump each other
# if the pawn has a fence behind it then an opposing pawn is able to move diagonally relative to its original
# position. The program itself includes validation for all moves, updating the state of the game.

class QuoridorGame:
    """Initializes the data members for the class Quoridorgame."""

    def __init__(self):
        """
        initializes the board with pawns, the turn, the state, the fence ct, the initial fences,
        and where the player pawns are.
        """
        self._board = board = [["E", "E", "E", "E", "P1", "E", "E", "E", "E"],  # row 0, baselines
                               ["E", "E", "E", "E", "E", "E", "E", "E", "E"],  # row 1
                               ["E", "E", "E", "E", "E", "E", "E", "E", "E"],  # row 2
                               ["E", "E", "E", "E", "E", "E", "E", "E", "E"],  # row 3
                               ["E", "E", "E", "E", "E", "E", "E", "E", "E"],  # row 4
                               ["E", "E", "E", "E", "E", "E", "E", "E", "E"],  # row 5
                               ["E", "E", "E", "E", "E", "E", "E", "E", "E"],  # row 6
                               ["E", "E", "E", "E", "E", "E", "E", "E", "E"],  # row 7
                               ["E", "E", "E", "E", "P2", "E", "E", "E", "E"]]  # row 8, baselines

        self._turn = 1  # if odd, p1 turn, if even p2 turn
        self._state = "UNFINISHED"  # If not 1 or 2, then the game is not done
        self._p1_fence_ct = 0  # maximum 10, increments each fence placement
        self._p2_fence_ct = 0  # maximum 10, increments each fence placement
        self._horizontal_fences = []
        self._vertical_fences = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8),
                                 (9, 0), (9, 1), (9, 2), (9, 3), (9, 4), (9, 5), (9, 6), (9, 7),
                                 (9, 8)]  # includes board edge
        self._p1_location = (4, 0)  # change every p1 turn
        self._p2_location = (4, 8)  # change every p2 turn

    def move_pawn(self, player, coords):
        """
        function used to make moves on the board, takes player and coordinates(tuple) as parameters. Will return
        false if the move is invalid and true otherwise.
        validates game state, whether or not coordinates are in range, whether the space designate is empty, whether
        the move is a move which is valid and whether or not fences are in the way.
        If a turn is valid, the turn increments, the pawn is moved, and win conditions are checked.
        """
        player_location = self.set_player_to_location(player)  # sets to pawn location based on which player
        if self.state_check() is False:  # checks state of the game
            return False
        elif self.coordinate_check_pawn(player_location, coords) is False:
            return False
        elif self._board[coords[1]][coords[0]] != "E":  # ensures coordinate space is empty, player has to "jump"
            return False
        elif self.turn_check(player) is False:
            return False
        elif self.pawn_move_length(player_location, coords) is False:
            return False
        elif self.pawn_move_type(player_location, coords) is False:
            return False
        else:
            self._turn += 1
            self.pawn_adjust(player, coords)
            self.win_condition()  # checks to see whether there is a winner after pawn movement
            return True

    def place_fence(self, player, direction, coords):
        """
        function used to place fences on the board, takes player, direction coordinates(tuple) as parameters.
        Will return false if the move is invalid and true otherwise.
        validates game state, whether or not coordinates are in range, whether the player has fences to player,
        whether the fence placement overlaps with another, whether or not it's their turn, and whether or not if a
        baseline wall been created. If the move is valid, the turn increments, the fence is added to the list of fences,
        and the players fence ct is incremented.
        """
        if self.state_check() is False:  # Checks state of the game
            return False
        elif self.coordinate_check_fence(direction, coords) is False:
            return False
        elif self.fence_ct(player) is False:  # false is 10 fences already placed for player
            return False
        elif self.fence_overlap(direction, coords) is False:  # Ensures no overlap
            return False
        elif self.turn_check(player) is False:  # if false, turn not valid
            return False
        elif self.baseline_block(direction, coords) is False:
            return False
        else:
            self._turn += 1  # should work, increments turn
            self.add_fence(direction, coords)  # add fence to private list
            self.increment_fence(player)  # increments fence after turn is found to be valid
            return True

    def set_player_to_location(self, player):
        """Turns player number into their location for functions."""
        if player == 1:
            return self._p1_location
        elif player == 2:
            return self._p2_location

    def set_opposite(self, player):
        """Set opposite player location, according to player."""
        if player == self._p1_location:
            return self._p2_location
        elif player == self._p2_location:
            return self._p1_location

    def state_check(self):
        """Method for move_pawn which checks to see if game has been won yet."""
        if self._state == "UNFINISHED":
            return True
        else:
            return False

    def coordinate_check_pawn(self, player, coords):
        """
        Validates that the coordinates entered are valid and within range on the board.
        Validates that the player is actually moving their piece and not just *staying* for a null move
        Validates that the player is not trying to move on top of already present piece
        """
        opposite = self.set_opposite(player)
        if coords == player:
            return False
        elif coords == opposite:
            return False
        else:
            if 0 <= coords[0] <= 8:
                if 0 <= coords[1] <= 8:
                    return True
                else:
                    return False
            else:
                return False

    def turn_check(self, player):
        """Checks whose turn it is, if it is the correct turn return True, else return False."""
        if player == 1:
            if self._turn % 2 > 0:  # if remainder present, it is in fact player 1 turn
                return True
            else:
                return False
        elif player == 2:
            if self._turn % 2 == 0:  # if remainder not present, it is in fact player 2 turn
                return True
            else:
                return False

    def pawn_move_length(self, player, coords):
        """If a player tries to make a move > 2 spaces in any direction, the move is invalid."""
        if player[0] - coords[0] > 2 or player[0] - coords[0] < -2:
            return False
        elif player[1] - coords[1] > 2 or player[1] - coords[1] < -2:
            return False
        else:
            return True

    def pawn_move_type(self, player, coords):
        """
        Determines what type of move the pawn is making.
        There are 10 different types of moves the pawn may make depending on the state of the board.
        The method will determine what move type is being made, and then go into checking if there
        is a fence in the way.
        """
        if player[0] - coords[0] == 1 or player[0] - coords[0] == -1:  # Tests for horizontal/ diagonal movement
            if player[1] - coords[1] == 1 or player[1] - coords[1] == -1:
                return self.fence_check_diagonal(player, coords)
            elif player[1] - coords[1] == 0:
                return self.fence_check_horizontal(player, coords)
            else:
                return False
        elif player[0] - coords[0] == 0:  # no x movement, implies vertical movement
            if player[1] - coords[1] == 1 or player[1] - coords[1] == -1:
                return self.fence_check_vertical(player, coords)
            elif player[1] - coords[1] == 2 or player[1] - coords[1] == -2:
                return self.fence_check_jump(player, coords)
        else:
            return False  # invalid player movement, only

    def fence_check_horizontal(self, player, coords):
        """
        Checks to see if fence is in the way of the player move in the horizontal direction, if so, returns false.
        The function takes into consideration on the LH side of any pawn a fence can occupy the same coordinate
        as a pawn,due to this, it confirms that a move to the left is okay, unless there is an immediate fence.
        Will return False if there is a fence in the way, and True if not. Check for left to right movement.
        """
        if (player[0] - coords[0]) == 1:  # moves to left are allowed
            if player in self._vertical_fences:  # ... unless there is an immediate fence to left
                return False
            else:
                return True
        elif (player[0] - coords[0]) == -1:
            if (player[0] + 1, player[1]) in self._vertical_fences:  # right check
                return False
            else:
                return True

    def fence_check_vertical(self, player, coords):
        """
        Checks to see if fence is in the way of the player move in the vertical direction, if so, returns false.
        The function takes into consideration on the back side of any pawn a fence can occupy the same coordinate
        as a pawn, due to this, it confirms that a move up on the board is okay, unless there is an immediate fence.
        Will return False if there is a fence in the way, and True if not. Check for up and down movement.
        """
        if (player[1] - coords[1]) == 1:  # moves up on board are allowed
            if player in self._horizontal_fences:  # ... unless there is an immediate fence
                return False
            else:
                return True
        elif (player[1] - coords[1]) == -1:
            if (player[0], player[1] + 1) in self._horizontal_fences:  # tuple == immediate fence down
                return False
            else:
                return True

    def fence_check_diagonal(self, player, coords):
        """
        Determines whether or not a diagonal move is valid. If it is valid, it will determine if it is an up diagonal
        or down diagonal move, and execute appropriate function.
        """
        opposite = self.set_opposite(player)
        x = player[0]
        y_up = player[1] - 1
        y_dn = player[1] + 1
        up_test = (x, y_up)
        dn_test = (x, y_dn)
        if up_test == opposite:  # up case, confirms pawn is there
            return self.up_diagonal_check(player, coords, up_test)
        elif dn_test == opposite:  # down case, confirms pawn is there
            return self.down_diagonal_check(player, coords)
        else:  # no pawn is present, move is invalid
            return False

    def up_diagonal_check(self, player, coords, up_test):
        """
        When moving the pawn in a up left/right move, this method will validate the following things: that there is a
        fence behind the pawn of interest and that there are no fences in the way of the pawn movement per rules.
        """
        if up_test in self._horizontal_fences:  # checks to make sure fence behind pawn
            x_cd = player[0] - 1
            x_rt = player[0] + 1
            x_lt = player[0]
            y = player[1] - 1
            right_test = (x_rt, y)  # used in test to see what movement is made and if vertical fence present
            left_test = (x_lt, y)  # location of fence on left hand side
            cd_test = (x_cd, y)  # used in test to see what movement is made for left hand movement
            if coords == right_test:  # right movement case
                if right_test not in self._vertical_fences:
                    return True
                else:
                    return False
            elif coords == cd_test:  # left movement case
                if left_test not in self._vertical_fences:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def down_diagonal_check(self, player, coords):
        """
        When moving the pawn in a down left/right move, this method will validate the following things: that there is a
        fence behind the pawn of interest and that there are no fences in the way of the pawn movement per rules.
        """
        x = player[0]
        y = player[1] + 2
        dn_fence_check = (x, y)
        if dn_fence_check in self._horizontal_fences:  # makes sure fence is behind pawn
            x_cd = player[0] - 1
            x_rt = player[0] + 1
            x_lt = player[0]
            y = player[1] + 1
            right_test = (x_rt, y)  # used in test to see what movement is made and if vertical fence present
            left_test = (x_lt, y)  # location of fence on left hand side
            cd_test = (x_cd, y)  # used in test to see what movement is made for left hand movement
            if coords == right_test:  # right movement case
                if right_test not in self._vertical_fences:
                    return True
                else:
                    return False
            elif coords == cd_test:  # left movement case
                if left_test not in self._vertical_fences:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def fence_check_jump(self, player, coords):
        """
        Checks if a vertical jump is valid.
        The method determines what kind of jump is being done by the pawn, then creates a "test" piece which
        then compares whether the opposing piece is in fact there, if it passes this first test, then the next
        tests whether or not a fence is behind the piece is being jumped. If there is not, the move is allowed
         to proceed and returns True.
         Checks if there is a horizontal fence in the way of the jump as well.
        """
        opposite = self.set_opposite(player)
        if player[1] - coords[1] == -2:  # jump in down direction on board
            return self.jump_down(player, coords, opposite)
        elif player[1] - coords[1] == 2:  # jump in up direction on board
            return self.jump_up(player, coords, opposite)

    def jump_down(self, player, coords, opposite):
        """Determines if a jump up the board is valid or not."""
        x = player[0]
        y = player[1] + 1
        test = (x, y)
        if opposite == test:  # Checks if p2 piece is there.
            if test not in self._horizontal_fences:
                if coords in self._horizontal_fences:
                    return False
                else:
                    return True
            else:
                return False
        else:
            return False

    def jump_up(self, player, coords, opposite):
        """Determines if a jump down the board is valid or not."""
        x = player[0]
        y = player[1] - 1
        test = (x, y)
        if opposite == test:  # Checks if p2 piece is there.
            if player not in self._horizontal_fences:
                if test in self._horizontal_fences:  # fence would occupy same place as pawn
                    return False
                else:
                    return True
            else:
                return False
        else:
            return False

    def pawn_adjust(self, player, coords):
        """
        Function in move_pawn which actually moves the pawn on the board and updates board and p location.
        This function will only execute if validation passes, hence returning True in scenarios.
        """
        if player == 1:
            old = self._p1_location
            self._board[old[1]][old[0]] = "E"
            self._p1_location = coords
            self._board[coords[1]][coords[0]] = "P1"
            return True
        elif player == 2:
            old = self._p2_location
            self._board[old[1]][old[0]] = "E"
            self._p2_location = coords
            self._board[coords[1]][coords[0]] = "P2"
            return True

    def fence_ct(self, player):
        """After validating that the move is valid, and a fence is placed, it will increment fence count for player."""
        if player == 1:
            if self._p1_fence_ct < 10:
                return True
            else:
                return False
        elif player == 2:
            if self._p2_fence_ct < 10:
                return True
            else:
                return False

    def increment_fence(self, player):
        """
        After assurance/validation there are less than 10 fences in prior methods it will increment
        fence count for player.
        """
        if player == 1:
            self._p1_fence_ct += 1
            return True
        elif player == 2:
            self._p2_fence_ct += 1
            return True

    def add_fence(self, direction, coords):
        """After validation, adds to the current list of fences."""
        if direction == "h":
            self._horizontal_fences.append(coords)
            return True
        elif direction == "v":
            self._vertical_fences.append(coords)
            return True

    def fence_overlap(self, direction, coords):
        """Ensures no fence overlapping occurs, if it does it returns False."""
        if direction == "h":
            if coords in self._horizontal_fences:
                return False
            else:
                return True
        elif direction == "v":
            if coords in self._vertical_fences:
                return False
            else:
                return True

    def baseline_block(self, direction, coords):
        """
        Checks to make sure that there's no solid fence horizontally on board, it this occurs, it returns False.
        The possible horizontal rows are present, it creates a copy of the horizontal fences l
        """
        horizontal_fence_copy = list(self._horizontal_fences)
        horizontal_fence_copy.append(coords)
        row1 = [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1)]
        row2 = [(0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2), (8, 2)]
        row3 = [(0, 3), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (6, 3), (7, 3), (8, 3)]
        row4 = [(0, 4), (1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (6, 4), (7, 4), (8, 4)]
        row5 = [(0, 5), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (7, 5), (8, 5)]
        row6 = [(0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6), (8, 6)]
        row7 = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7), (8, 7)]
        row8 = [(0, 8), (1, 8), (2, 8), (3, 8), (4, 8), (5, 8), (6, 8), (7, 8), (8, 8)]
        row1_result = all(elem in horizontal_fence_copy for elem in row1)
        row2_result = all(elem in horizontal_fence_copy for elem in row2)
        row3_result = all(elem in horizontal_fence_copy for elem in row3)
        row4_result = all(elem in horizontal_fence_copy for elem in row4)
        row5_result = all(elem in horizontal_fence_copy for elem in row5)
        row6_result = all(elem in horizontal_fence_copy for elem in row6)
        row7_result = all(elem in horizontal_fence_copy for elem in row7)
        row8_result = all(elem in horizontal_fence_copy for elem in row8)
        # True value = 1, if any of them are true it will be above 1
        # true = 1, false = 0
        # if horizontal_fence_copy
        test = row1_result + row2_result + row3_result + row4_result + row5_result + row6_result + row7_result + row8_result
        if direction == "v":
            return True
        elif test > 0:
            return False
        else:
            return True

    def coordinate_check_fence(self, direction, coords):
        """Validates that the coordinates entered are valid and within range on the board."""
        if direction == "h":
            if 0 <= coords[0] <= 8:
                if 1 <= coords[1] <= 8:
                    return True
                else:
                    return False
            else:
                return False
        if direction == "v":
            if 1 <= coords[0] <= 8:
                if 0 <= coords[1] <= 8:
                    return True
                else:
                    return False
            else:
                return False

    def win_condition(self):
        """
        Checks if win condition has been fulfilled by either player.
        If a player has reached either baseline, the self._state private class will update to that player number.
        """
        if self._p1_location[1] == 8:
            self._state = 1
            print("Player 1 wins.")
            return True
        elif self._p2_location[1] == 0:
            self._state = 2
            print("Player 2 wins.")
            return True
        else:
            return True

    def is_winner(self, player):
        """Use integer representing the player num and returns True if that player has won and False if not."""
        if player == self._state:
            return True
        else:
            return False

    def print_board(self):
        """
        Generates a board that reflects the placement of pawns and fences.
        The game board is stored within a private class, which contains the 9x9 board. Visually
        this is needed to display the fences and player movement appropriately.
        The tuples are stored within private members, then translated through dictionaries in
        this function. The end result is an up-to-date game board with pieces and fences.
        """
        board = [[" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],  # 0
                 ["+", " ", "+", " ", "+", " ", "+", " ", "+", " ", "+", " ", "+", " ", "+", " ", "+", " ", "+"],  # 1
                 [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],  # 2
                 ["+", " ", "+", " ", "+", " ", "+", " ", "+", " ", "+", " ", "+", " ", "+", " ", "+", " ", "+"],  # 3
                 [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],  # 4
                 ["+", " ", "+", " ", "+", " ", "+", " ", "+", " ", "+", " ", "+", " ", "+", " ", "+", " ", "+"],  # 5
                 [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],  # 6
                 ["+", " ", "+", " ", "+", " ", "+", " ", "+", " ", "+", " ", "+", " ", "+", " ", "+", " ", "+"],  # 7
                 [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],  # 8
                 ["+", " ", "+", " ", "+", " ", "+", " ", "+", " ", "+", " ", "+", " ", "+", " ", "+", " ", "+"],  # 9
                 [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],  # 10
                 ["+", " ", "+", " ", "+", " ", "+", " ", "+", " ", "+", " ", "+", " ", "+", " ", "+", " ", "+"],  # 11
                 [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],  # 12
                 ["+", " ", "+", " ", "+", " ", "+", " ", "+", " ", "+", " ", "+", " ", "+", " ", "+", " ", "+"],  # 13
                 [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],  # 14
                 ["+", " ", "+", " ", "+", " ", "+", " ", "+", " ", "+", " ", "+", " ", "+", " ", "+", " ", "+"],  # 15
                 [" ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "]]  # 16

        bounds = ["+", "=", "+", "=", "+", "=", "+", "=", "+", "=", "+", "=", "+", "=", "+", "=", "+", "=", "+"]

        pawn_dict_x = {
            0: 1,
            1: 3,
            2: 5,
            3: 7,
            4: 9,
            5: 11,
            6: 13,
            7: 15,
            8: 17
        }

        pawn_dict_y = {
            0: 0,
            1: 2,
            2: 4,
            3: 6,
            4: 8,
            5: 10,
            6: 12,
            7: 14,
            8: 16
        }

        # Generates p1 pawn location
        if self._p1_location[0] in pawn_dict_x:
            x = pawn_dict_x[self._p1_location[0]]
            if self._p1_location[1] in pawn_dict_y:
                y = pawn_dict_y[self._p1_location[1]]
        p1_new = (x, y)
        board[p1_new[1]][p1_new[0]] = "1"

        # Generates P2 pawn location
        if self._p2_location[0] in pawn_dict_x:
            x = pawn_dict_x[self._p2_location[0]]
            if self._p2_location[1] in pawn_dict_y:
                y = pawn_dict_y[self._p2_location[1]]
        p2_new = (x, y)
        board[p2_new[1]][p2_new[0]] = "2"

        vert_fence_x = {
            0: 0,
            1: 2,
            2: 4,
            3: 6,
            4: 8,
            5: 10,
            6: 12,
            7: 14,
            8: 16,
            9: 18
        }

        vert_fence_y = {
            0: 0,
            1: 2,
            2: 4,
            3: 6,
            4: 8,
            5: 10,
            6: 12,
            7: 14,
            8: 16,
            9: 18
        }

        # generates vertical fences for game board
        for fence in self._vertical_fences:
            if fence[0] in vert_fence_x:
                x = vert_fence_x[fence[0]]
                if fence[1] in vert_fence_y:
                    y = vert_fence_y[fence[1]]
            fence_new = (x, y)
            board[fence_new[1]][fence_new[0]] = "|"

        hori_fence_x = {
            0: 1,
            1: 3,
            2: 5,
            3: 7,
            4: 9,
            5: 11,
            6: 13,
            7: 15,
            8: 17
        }

        hori_fence_y = {
            1: 1,
            2: 3,
            3: 5,
            4: 7,
            5: 9,
            6: 11,
            7: 13,
            8: 15
        }

        # generates horizontal fences for game board
        for fence in self._horizontal_fences:
            if fence[0] in hori_fence_x:
                x = hori_fence_x[fence[0]]
                if fence[1] in hori_fence_y:
                    y = hori_fence_y[fence[1]]
            fence_new = (x, y)
            board[fence_new[1]][fence_new[0]] = "="

        print((" ".join(bounds)))
        for i in range(len(board)):
            print(" ".join(board[i]))
        print((" ".join(bounds)))


# program tests
# q = QuoridorGame()
# print(q.move_pawn(1, (4,1)))
# print(q.move_pawn(2, (4,7)))
# print(q.move_pawn(1, (4,2)))
# print(q.move_pawn(2, (4,6)))
# print(q.move_pawn(1, (4,3)))
# print(q.move_pawn(2, (4,5)))
# print(q.move_pawn(1, (4,4)))

# print(q.place_fence(2, "h", (4,6)))
# print(q.place_fence(1, "v", (7,5)))
# print(q.place_fence(2, "v", (6,5)))

# print(q.move_pawn(1, (5,5)))
# q.print_board()

# p1 cannot move through horizontal fences,
# p2 cannot move through horizontal fences, check

# p2 cannot cross vertical fences, check
# p1 cannot cross vertical fences

# p2 can jump over p1, but cannot jump over if fence present. this works properly, check
# p1 can over over p2, but cannot jump over if fence present. this works properly, check

# win condition properly prints for both players

# p2 can move diagonally up w/ no fence, works properly
# p2 will not move if fences in way on right side, works properly
# p2 will not move if fence in way on left side, works properly

# p1 can move diagonally up w/ no fence, works properly
# p1 will not move if fences in way on right side, works properly
# p1 will not move if fence in way on left side, works properly


# p1 moves down diagonally both ways fine, works properly, works properly
# p1 will not move if fences are in the way on a diagonal move, works properly

# pawn movement does appear to work, so does fence placement

# implement a play game function.
