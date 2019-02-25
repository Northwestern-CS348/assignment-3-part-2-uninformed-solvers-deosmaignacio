from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

	def __init__(self):
		super().__init__()

	def produceMovableQuery(self):
		"""
		See overridden parent class method for more information.

		Returns:
			 A Fact object that could be used to query the currently available moves
		"""
		return parse_input('fact: (movable ?disk ?init ?target)')

	def getGameState(self):
		"""
		Returns a representation of the game in the current state.
		The output should be a Tuple of three Tuples. Each inner tuple should
		represent a peg, and its content the disks on the peg. Disks
		should be represented by integers, with the smallest disk
		represented by 1, and the second smallest 2, etc.

		Within each inner Tuple, the integers should be sorted in ascending order,
		indicating the smallest disk stacked on top of the larger ones.

		For example, the output should adopt the following format:
		((1,2,5),(),(3, 4))

		Returns:
			A Tuple of Tuples that represent the game state
		"""
		firstPeg = []
		secondPeg = []
		thirdPeg = []
		inputParse = parse_input("fact: (inst ?peg peg)")
		pegs = self.kb.kb_ask(inputParse)
		for peg in pegs:
			if not Fact(instantiate(Statement(("empty", "?peg")), peg)) in self.kb.facts:
				# if not empty, get list of all disks on it
				disks = self.kb.kb_ask(Fact(instantiate(Statement(("on", "?disk", "?peg")), peg)))
				disksAsInts = []
				for disk in disks:
					entry = int(disk.bindings_dict["?disk"][4])
					disksAsInts.append(entry)
				pegAsInt = int(peg.bindings_dict["?peg"][3])  # get this peg's identity
				if pegAsInt == 1:
					if disksAsInts:
						while disksAsInts:
							smallestDisk = min(disksAsInts)
							firstPeg.append(smallestDisk)
							disksAsInts.remove(smallestDisk)
				elif pegAsInt == 2:
					if disksAsInts:
						while disksAsInts:
							smallestDisk = min(disksAsInts)
							secondPeg.append(smallestDisk)
							disksAsInts.remove(smallestDisk)
				else:
					if disksAsInts:
						while disksAsInts:
							smallestDisk = min(disksAsInts)
							thirdPeg.append(smallestDisk)
							disksAsInts.remove(smallestDisk)
		result = (tuple(firstPeg), tuple(secondPeg), tuple(thirdPeg))
		return result

	def makeMove(self, movable_statement):
		"""
		Takes a MOVABLE statement and makes the corresponding move. This will
		result in a change of the game state, and therefore requires updating
		the KB in the Game Master.

		The statement should come directly from the result of the MOVABLE query
		issued to the KB, in the following format:
		(movable disk1 peg1 peg3)

		Args:
			movable_statement: A Statement object that contains one of the currently viable moves

		Returns:
			None
		"""
		statementTerms = movable_statement.terms
		secondTerm = statementTerms[1]
		lastTerm = statementTerms[2]
		firstTerm = statementTerms[0]

		newFirstDisk = self.kb.kb_ask(Fact(Statement(("onTop", firstTerm, "?obj"))))[0]
		currFirstDisk = self.kb.kb_ask(Fact(Statement(("top", "?obj", lastTerm))))[0]

		newFirstFact = Fact(instantiate(Statement(("onTop", firstTerm, "?obj")), newFirstDisk))
		currFirstFact = Fact(instantiate(Statement(("top", "?obj", lastTerm)), currFirstDisk))

		newTopFact = Fact(instantiate(Statement(("top", "?obj", secondTerm)), newFirstDisk))
		currTopFact = Fact(instantiate(Statement(("onTop", firstTerm, "?obj")), currFirstDisk))

		self.kb.kb_retract(Fact(Statement(("on", firstTerm, secondTerm))))
		self.kb.kb_retract(Fact(Statement(("top", firstTerm, secondTerm))))
		self.kb.kb_retract(newFirstFact)
		self.kb.kb_retract(currFirstFact)
		self.kb.kb_assert(Fact(Statement(("on", firstTerm, lastTerm))))
		self.kb.kb_assert(Fact(Statement(("top", firstTerm, lastTerm))))
		self.kb.kb_assert(newTopFact)
		self.kb.kb_assert(currTopFact)


	def reverseMove(self, movable_statement):
		"""
		See overridden parent class method for more information.

		Args:
			movable_statement: A Statement object that contains one of the previously viable moves

		Returns:
			None
		"""
		pred = movable_statement.predicate
		sl = movable_statement.terms
		newList = [pred, sl[0], sl[2], sl[1]]
		self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

	def __init__(self):
		super().__init__()

	def produceMovableQuery(self):
		"""
		Create the Fact object that could be used to query
		the KB of the presently available moves. This function
		is called once per game.

		Returns:
			 A Fact object that could be used to query the currently available moves
		"""
		return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

	def getGameState(self):
		"""
		Returns a representation of the the game board in the current state.
		The output should be a Tuple of Three Tuples. Each inner tuple should
		represent a row of tiles on the board. Each tile should be represented
		with an integer; the empty space should be represented with -1.

		For example, the output should adopt the following format:
		((1, 2, 3), (4, 5, 6), (7, 8, -1))

		Returns:
			A Tuple of Tuples that represent the game state
		"""
		coordinates = {"pos1": ("pos1", "pos2", "pos3"),
				"pos2": ("pos1", "pos2", "pos3"),
				"pos3": ("pos1", "pos2", "pos3")}
		currState = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
		for yCoord in coordinates:
			y = int(yCoord[3]) - 1
			for xCoord in coordinates[yCoord]:
				x = int(xCoord[3]) - 1
				question = Fact(Statement(["coord", "?tile", xCoord, yCoord]))
				bindings = self.kb.kb_ask(question)[0]
				tile = bindings.bindings_dict["?tile"][4]
				tileAsInt = 0
				if tile == 'y':
					tileAsInt = -1
				else:
					tileAsInt = int(tile)
				currState[y][x] = tileAsInt
		return tuple([tuple(currState[0]), tuple(currState[1]), tuple(currState[2])])

	def makeMove(self, movable_statement):
		"""
		Takes a MOVABLE statement and makes the corresponding move. This will
		result in a change of the game state, and therefore requires updating
		the KB in the Game Master.

		The statement should come directly from the result of the MOVABLE query
		issued to the KB, in the following format:
		(movable tile3 pos1 pos3 pos2 pos3)

		Args:
			movable_statement: A Statement object that contains one of the currently viable moves

		Returns:
			None
		"""
		terms = movable_statement.terms
		currTile = terms[0]
		currXCoord = terms[1]
		newXCoord = terms[3]
		currYCoord = terms[2]
		newYCoord = terms[4]

		self.kb.kb_retract(Fact(Statement(("coordinate", "empty", newXCoord, newYCoord))))
		self.kb.kb_retract(Fact(Statement(("coordinate", currTile, currXCoord, currYCoord))))

		self.kb.kb_assert(Fact(Statement(("coordinate", "empty", currXCoord, currYCoord))))
		self.kb.kb_assert(Fact(Statement(("coordinate", currTile, newXCoord, newYCoord))))

	def reverseMove(self, movable_statement):
		"""
		See overridden parent class method for more information.

		Args:
			movable_statement: A Statement object that contains one of the previously viable moves

		Returns:
			None
		"""
		pred = movable_statement.predicate
		sl = movable_statement.terms
		newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
		self.makeMove(Statement(newList))
