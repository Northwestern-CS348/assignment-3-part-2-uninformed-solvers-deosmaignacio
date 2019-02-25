
from solver import *

class SolverDFS(UninformedSolver):
	def __init__(self, gameMaster, victoryCondition):
		super().__init__(gameMaster, victoryCondition)

	def solveOneStep(self):
		"""
		Go to the next state that has not been explored. If a
		game state leads to more than one unexplored game states,
		explore in the order implied by the GameMaster.getMovables()
		function.
		If all game states reachable from a parent state has been explored,
		the next explored state should conform to the specifications of
		the Depth-First Search algorithm.

		Returns:
			True if the desired solution state is reached, False otherwise
		"""
		if self.currentState.state == self.victoryCondition:
			return True
		movesToMake = self.gm.getMovables()
		depthOfChild = self.currentState.depth + 1
		currMove = False
		while not currMove:
			curr = self.currentState.nextChildToVisit
			if len(movesToMake) <= curr:
				if self.currentState.parent:
					self.gm.reverseMove(self.currentState.requiredMovable)
					movesToMake = self.gm.getMovables()
					self.currentState = self.currentState.parent
					depthOfChild = self.currentState.depth + 1
					continue
				else:
					return False
			currMoveTry = movesToMake[curr]
			self.gm.makeMove(currMoveTry)
			resultingState = GameState(self.gm.getGameState(), depthOfChild, currMoveTry)
			if resultingState not in self.visited:
				resultingState.parent = self.currentState
				self.currentState.children.append(resultingState)
				self.currentState.nextChildToVisit += 1
				self.currentState = resultingState
				currMove = currMoveTry
			else:
				self.gm.reverseMove(currMoveTry)
				self.currentState.nextChildToVisit += 1
		if self.currentState.state == self.victoryCondition:
			return True
		else:
			self.visited[self.currentState] = True
			return False
		return True


class SolverBFS(UninformedSolver):
	def __init__(self, gameMaster, victoryCondition):
		super().__init__(gameMaster, victoryCondition)

	def solveOneStep(self):
		"""
		Go to the next state that has not been explored. If a
		game state leads to more than one unexplored game states,
		explore in the order implied by the GameMaster.getMovables()
		function.
		If all game states reachable from a parent state has been explored,
		the next explored state should conform to the specifications of
		the Breadth-First Search algorithm.

		Returns:
			True if the desired solution state is reached, False otherwise
		"""
		if self.currentState.state == self.victoryCondition:
			return True

		currDepth = self.currentState.depth
		currMove = False
		while self.currentState.parent:
			self.gm.reverseMove(self.currentState.requiredMovable)
			self.currentState = self.currentState.parent
			counter = self.currentState.nextChildToVisit
			if len(self.currentState.children) > counter:
				currMove = True
				break
		if not currMove:
			for visitedState in self.visited.keys():
				visitedState.nextChildToVisit = 0
			currDepth += 1
			if len(self.visited) == 1:
				possibleMoves = self.gm.getMovables()
				for move in possibleMoves:
					self.gm.makeMove(move)
					newState = GameState(self.gm.getGameState(), currDepth, move)
					newState.parent = self.currentState
					self.visited[newState] = False
					self.currentState.children.append(newState)
					self.gm.reverseMove(move)
		while currDepth != self.currentState.depth:
			counter = self.currentState.nextChildToVisit
			self.currentState.nextChildToVisit += 1
			if len(self.currentState.children) > counter:
				self.currentState = self.currentState.children[counter]
				nextMove = self.currentState.requiredMovable
				self.gm.makeMove(nextMove)
			else:
				currMove = False
				while self.currentState.parent:
					self.gm.reverseMove(self.currentState.requiredMovable)
					self.currentState = self.currentState.parent
					if len(self.currentState.children) > self.currentState.nextChildToVisit:
						currMove = True
						break
				if not currMove:
					return False

		if self.currentState.state != self.victoryCondition:
			self.visited[self.currentState] = True
			possibleMoves = self.gm.getMovables()
			newDepth = currDepth + 1
			for move in possibleMoves:
				self.gm.makeMove(move)
				newState = GameState(self.gm.getGameState(), newDepth, move)
				if newState not in self.visited:
					self.visited[newState] = False
					newState.parent = self.currentState
					self.currentState.children.append(newState)
				self.gm.reverseMove(move)
			return False
		else:
		   return True
