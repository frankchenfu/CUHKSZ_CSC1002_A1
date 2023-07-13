import random


"""
Print the puzzle map.
@param puzzle_map
	The puzzle map in the form of list[list]
"""
def print_puzzle(puzzle_map: list) -> None:
	for line in puzzle_map:
		print(end='\t')
		for i in line:
			print("%3d" % i, end='') if i >= 0 else print("   ", end='')
		print()


"""
Check whether the moving is valid.
@param puzzle_dimension
	The dimension of the puzzle.
@param space_x
	The x coordinate of the space.
@param space_y
	The y coordinate of the space.
@return
	Return True for valid and False for invalid.
"""
def check_moving(puzzle_dimension: int, space_x: int, space_y: int) -> bool:
	return 0 <= space_x < puzzle_dimension and 0 <= space_y < puzzle_dimension


"""
Get integer for dimension from user input.
@return
	Returns a integer representing the dimension of the puzzle,
	or returns None if the user quits.
"""
def get_dimension() -> int:
	puzzle_dimension: int  # dimension for the puzzle
	while True:
		puzzle_dimension = input("Enter \"1\" for 8-puzzle, \"2\" for "
			"15-puzzle or \"q\" to end the game (quotes excluded): ")
		puzzle_dimension = puzzle_dimension.strip().casefold()
		if puzzle_dimension == "q":
			return None
		elif puzzle_dimension == "1":
			return 3
		elif puzzle_dimension == "2":
			return 4
		else:
			print("Please follow the hint above. Try again.")


"""
Get characters for direction from user input.
@return
	Returns a tuple representing the directions of left, right,
	up and down, respectively.
"""
def get_options() -> tuple:
	# the characters for 4 directions
	moving_options: tuple[str, str, str, str]
	while True:
		moving_options = input("Enter four characters for left, right, "
			"up and down directions (separate by single white space):\n")
		moving_options = moving_options.casefold().split()
		# to support case insensitive inputs
		moving_options = [s for s in moving_options if s]
		# remove the white spaces from the list of options

		if len(moving_options) != 4:
			print("Got %d characters, four characters are needed. Try again."
				  % len(moving_options))
		else:
			option_set = set()  # Exist directions
			for ch in moving_options:
				if len(ch) != 1 or ch[0] in option_set:
					break
				if ord(ch[0]) < ord('a') or ord(ch[0]) > ord('z'):
					break
				option_set.add(ch[0])
			else:
				moving_options = tuple(moving_options)
				break
			print("Directions should be represented by "
				  "four different English characters. Try again.")
	return moving_options


"""
Get the current move from user input.
@param puzzle_dimension
	The dimension of the puzzle.
@param space_x
	The x coordinate of the space.
@param space_y
	The y coordinate of the space.
@param moving_options
	The characters representing the directions.
@return
	Return the tuple representing the moving option,
	or return None if the user quits.
"""
def get_moving(
		puzzle_dimension: int,
		space_x: int,
		space_y: int,
		moving_options: tuple
		) -> tuple:
	hint_info: str = "exit - ex, "	# List all possible directions in string
	available_option: list = ["ex"]	# List all possible directions in list
	option: str						# Record the chosen direction
	for i in range(4):
		dx, dy = [(0, 1), (0, -1), (1, 0), (-1, 0)][i]
		direction = ["left", "right", "up", "down"][i]
		if check_moving(puzzle_dimension, space_x + dx, space_y + dy):
			hint_info += direction + " - " + moving_options[i] + ", "
			available_option.append(moving_options[i])
	while True:
		option = input("Enter your move (%s): " % hint_info[:-2])
		option = option.strip().casefold()
		if option in available_option:
			break
		print("The direction is unavailable. Try again.")
	if option == "ex":
		return None
	else:
		return [(0, 1), (0, -1), (1, 0), (-1, 0)][moving_options.index(option)]


"""
Set a new solvable game with dimension $puzzle_dimension$.
First set it to the final (ordered) state, then use a DFS
algorithm to randomly rearrange the game.
@param puzzle_dimension
	The dimension of the puzzle.
@return
	Return a 2D matrix (implemented by list[list]) representing
	the initial state. Note that -1 stands for the space.
"""
def reset_new_game(puzzle_dimension: int) -> tuple:
	puzzle_map = [
		[i*puzzle_dimension + j + 1 for j in range(puzzle_dimension)]
		for i in range(puzzle_dimension)
	]
	puzzle_map[-1][-1] = -1
	# To set the game into the final order, the bottom-right should be space.

	epoch = puzzle_dimension ** 4
	# The steps used to rearrange the map.
	space_x = space_y = puzzle_dimension - 1  # The space's initial postion.
	for i in range(epoch):
		dx, dy = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
		while not check_moving(puzzle_dimension, space_x + dx, space_y + dy):
			dx, dy = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
		# Find a possible moving direction

		terminal_x = space_x + dx
		terminal_y = space_y + dy
		puzzle_map[space_x][space_y], puzzle_map[terminal_x][terminal_y] = \
			puzzle_map[terminal_x][terminal_y], puzzle_map[space_x][space_y]
		space_x = terminal_x
		space_y = terminal_y
	return puzzle_map, space_x, space_y


"""
Check whether the game is end.
@param puzzle_map
	The state current puzzle.
@return
	Return True is the game is end, false otherwise.
"""
def checkmate(puzzle_map: list) -> bool:
	puzzle = sum(puzzle_map, [])  # Flatten the map to one dimension list.
	return sorted(puzzle[:-1]) == puzzle[:-1] and puzzle[-1] == -1


"""
Organize a single game.
@param puzzle_dimension
	The dimension of the puzzle.
@param moving_option
	The characters for each direction.
@return
	Return -1 if the user quits in one game.
	Return the steps to solve if the user succeeds.
"""
def new_game(puzzle_dimension: int, moving_options: tuple) -> int:
	puzzle, space_x, space_y = reset_new_game(puzzle_dimension)  # information
	step_counter: int = 0	# used step before puzzle is solved
	while not checkmate(puzzle):
		print_puzzle(puzzle)
		option = get_moving(puzzle_dimension, space_x, space_y, moving_options)
		if not option:
			print("Sorry, you fail this puzzle. Try again.\n")
			return -1
		terminal_x = space_x + option[0]
		terminal_y = space_y + option[1]
		puzzle[space_x][space_y], puzzle[terminal_x][terminal_y] = \
			puzzle[terminal_x][terminal_y], puzzle[space_x][space_y]
		space_x = terminal_x
		space_y = terminal_y
		step_counter += 1
	print_puzzle(puzzle)
	print("Congratulations! You solved the puzzle in %d steps!\n"
		% step_counter)
	return step_counter


"""
Organize multiple games.
Give statistics analysis when the game ends.
"""
def main() -> None:
	print("""\tWelcome to the puzzle game!\n
\tThis is an interactive sliding puzzle game for both 8 and 15 numbers.
An 8-number puzzle has a square-framed board consisting of 8 square tiles,
numbered 1 to 8, initially placed in random order, while a 15-number puzzle
there are 15 numbered square tiles, from 1 to 15.
\tThe game board has an empty space where one of adjacent tiles slides to.
The objective of the game is to re-arrange the tiles into a sequential order
by their numbers (left to right, top to bottom) by repeatedly making
sliding moves (left, right, up or down). The following figure shows an example
of one 8-number puzzle where \"INITIAL\" is the starting point of the game, and
the player needs to repeatedly slide one adjacent tile, one at a time,
to the unoccupied space (the empty space) until all numbers appear sequentially,
ordered from left to right, top to bottom, shown as \"FINAL\".
\t   1 3 \t\t 1 2 3
\t 4 2 5 \t\t 4 5 6
\t 7 8 6 \t\t 7 8  
\tINITIAL\t\t FINAL\n
Now let's get started!
""")

	try:
		moving_options = get_options()		# direction for the movings
		stat = [[0, 0, 0], [0, 0, 0]]
		# stat[0]: The total of game, winning game and steps (if win) for dim 3.
		# stat[1]: The total of game, winning game and steps (if win) for dim 4.
		while True:
			puzzle_dimension = get_dimension()  # dimension for the puzzle
			if not puzzle_dimension:
				break
			result = new_game(puzzle_dimension, moving_options)
			stat[puzzle_dimension - 3][0] += 1
			if result >= 0:
				stat[puzzle_dimension - 3][1] += 1
				stat[puzzle_dimension - 3][2] += result
	except:
		print("\nThere's an unknown error. Please restart this program.")
	else:
		print("\nThank you for your playing.\n")
		if stat[0][0] > 0:
			if stat[0][1] > 0:
				print("* In the 8-puzzles, you tried for %d times.\n"
					"(The winning percentage is %.2f%% and the average steps"
					" you used in the winning games is %.2f.)" % (stat[0][0],
					stat[0][1] / stat[0][0] * 100, stat[0][2] / stat[0][1]))
			else:
				print("* In the 8-puzzles, you tried for %d times."
					% stat[0][0])
		if stat[1][0] > 0:
			if stat[1][1] > 0:
				print("* In the 15-puzzles, you tried for %d times.\n"
					"(The winning percentage is %.2f%% and the average steps"
					" you used in the winning games is %.2f.)" % (stat[1][0],
					stat[1][1] / stat[1][0] * 100, stat[1][2] / stat[1][1]))
			else:
				print("* In the 15-puzzles, you tried for %d times."
					% stat[1][0])
		print("\nSee you next time. Good bye!")


if __name__ == "__main__":
	main()