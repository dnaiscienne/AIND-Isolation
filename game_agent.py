"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
import random

class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass

#First heuristic
def pro_self_score(game, player):
    """Evaluation function that gives more weight to conditions where the  player has more moves rather than when the opponent has less moves.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : hashable
        One of the objects registered by the game object as a valid player.
        (i.e., `player` should be either game.__player_1__ or
        game.__player_2__).

    Returns
    ----------
    float
        The heuristic value of the current game state
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")
		
	# TODO: Replace with evaluation function that outputs a score with preference to blocking moves

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    #print(game.get_player_location(player))
    #print(game.get_legal_moves(game.get_opponent(player)))
    #Of course this won't work since this means that the player move cannot be a legal opponent move.
    return own_moves - (opp_moves * .9)

#Second heuristic
def anti_opponent_score(game, player):
    """Evaluation function that gives more weight to conditions where the opponent player has less moves rather than when the player has more moves.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : hashable
        One of the objects registered by the game object as a valid player.
        (i.e., `player` should be either game.__player_1__ or
        game.__player_2__).

    Returns
    ----------
    float
        The heuristic value of the current game state
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")
		
	# TODO: Replace with evaluation function that outputs a score based on the move's distance to the center

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return (own_moves*.9) - opp_moves
	
#Third heuristic
def free_score(game, player):
    """Combination of the pro_self_score and anti_opponent_score functions  being decided by the amount of free spaces on the board compared with the total number of moves for both players.
	
    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : hashable
        One of the objects registered by the game object as a valid player.
        (i.e., `player` should be either game.__player_1__ or
        game.__player_2__).

    Returns
    ----------
    float
        The heuristic value of the current game state
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")
		

    free_space = len(game.get_blank_spaces());
    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    total_moves = own_moves + opp_moves;
    if free_space < total_moves:
        return (own_moves*.9) - opp_moves
    return own_moves - (opp_moves * .9)


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """

    # TODO: finish this function!
    return free_score(game, player)


class CustomPlayer:
    """Game-playing agent that chooses a move using your evaluation function
    and a depth-limited minimax algorithm with alpha-beta pruning. You must
    finish and test this player to make sure it properly uses minimax and
    alpha-beta to return a good move before the search time limit expires.

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    iterative : boolean (optional)
        Flag indicating whether to perform fixed-depth search (False) or
        iterative deepening search (True).

    method : {'minimax', 'alphabeta'} (optional)
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score,
                 iterative=True, method='minimax', timeout=10.):
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.method = method
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    def get_move(self, game, legal_moves, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        This function must perform iterative deepening if self.iterative=True,
        and it must use the search method (minimax or alphabeta) corresponding
        to the self.method value.

        **********************************************************************
        NOTE: If time_left < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        legal_moves : list<(int, int)>
            A list containing legal moves. Moves are encoded as tuples of pairs
            of ints defining the next (row, col) for the agent to occupy.

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """

        self.time_left = time_left

        # TODO: finish this function!
		
		# Perform any required initializations, including selecting an initial
        # move from the game board (i.e., an opening book), or returning
        # immediately if there are no legal moves

		
		# Assigns  (-1, -1) as default representing no available legal moves
        best_move = (-1, -1)
		
		# Checks if there are still legal moves. If there are no legal moves return (-1, -1)
        if not legal_moves:
            return best_move
		
		# First move :  Return center position. Assumes that the board is a square and that there is a center (odd square)
        if game.move_count in (0, 1):
            return (game.height//2, game.width//2)
		
		# Get the method to be used. Minimax or Alpha-beta
        method = self.minimax if self.method=='minimax' else self.alphabeta
        
        try:
            # The search method call (alpha beta or minimax) should happen in
            # here in order to avoid timeout. The try/except block will
            # automatically catch the exception raised by the search method
            # when the timer gets close to expiring
            if self.iterative:
                iterative_depth = 1
                while True:
                    best_score, best_move = method(game, iterative_depth)
                    iterative_depth  += 1
			
			
            else:
			# Select best move based on evaluation
                best_score, best_move  = method(game, self.search_depth)
			

        except Timeout:
            # Handle any actions required at timeout, if necessary
            pass

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth, maximizing_player=True):
        """Implement the minimax search algorithm as described in the lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        # TODO: finish this function!
		# Assigns  (-1, -1) as default representing no available legal moves and +/- inf for upper and lower boundary of lowest and highest score
        legal_moves = game.get_legal_moves()
        best_move = (-1, -1)
        low_score, high_score = float("inf"), float("-inf")
		    	
        if maximizing_player:
		#No more legal moves
            if not legal_moves:
                return high_score, best_move
					
			# Reached target depth
            if depth == 1:
			
                for move in legal_moves:
			        # Evaluate the move's score
                    score = self.score(game.forecast_move(move), self)
				    # Check if winning move
                    if score == float("inf"):
            	        return score, move
                    if score > high_score:
                        high_score = score
                        best_move = move
                return high_score, best_move
			
			# Need to go deeper
            for move in legal_moves:
                score, _ = self.minimax(game.forecast_move(move), depth - 1, maximizing_player = False)
				# Check if winning move
                if score == float("inf"):
                    return score, move
                if score > high_score:
                    high_score = score
                    best_move = move
            return high_score, best_move
				
        else:
		    #No more legal moves
            if not legal_moves:
                return low_score, best_move
		# Reached target depth
            if depth == 1:
			
                for move in legal_moves:
			        # Evaluate the move's score
                    score = self.score(game.forecast_move(move), self)
				    # Check if losing move
                    if score == float("-inf"):
                        return score, move
                    if score < low_score:
                        low_score = score
                        best_move = move
                return low_score, best_move
			
			# Need to go deeper
            for move in legal_moves:
                score, _ = self.minimax(game.forecast_move(move), depth - 1, maximizing_player = True)
				# Check if losing move
                if score == float("-inf"):
                    return score, move
                if score < low_score:
                        low_score = score
                        best_move = move
            return low_score, best_move
		


    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        """Implement minimax search with alpha-beta pruning as described in the
        lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        # TODO: finish this function!
        # Assigns  (-1, -1) as default representing no available legal moves and +/- inf for upper and lower boundary of lowest and highest score
        legal_moves = game.get_legal_moves()
        best_move = (-1, -1)
        low_score, high_score = float("inf"), float("-inf")
		    	
        if maximizing_player:
		#No more legal moves
            if not legal_moves:
                return high_score, best_move
					
			# Reached target depth
            if depth == 1:
			
                for move in legal_moves:
			        # Evaluate the move's score
                    score = self.score(game.forecast_move(move), self)
				    # Check if winning move
                    if score == float("inf"):
                        return score, move
                    if score >= beta:
                        return score, move
                    if score > high_score:
                        high_score = score
                        best_move = move
                return high_score, best_move
			
			# Need to go deeper
            for move in legal_moves:
                score, _ = self.alphabeta(game.forecast_move(move), depth - 1, alpha, beta, maximizing_player = False)
				# Check if winning move
                if score == float("inf"):
                    return score, move
                if score >= beta:
                    return score, move
                if score > high_score:
                    high_score = score
                    best_move = move
                alpha = max(alpha, high_score)
            return high_score, best_move
				
        else:
		    #No more legal moves
            if not legal_moves:
                return low_score, best_move
		# Reached target depth
            if depth == 1:
			
                for move in legal_moves:
			        # Evaluate the move's score
                    score = self.score(game.forecast_move(move), self)
				    # Check if losing move
                    if score == float("-inf"):
                        return score, move
                    if score <= alpha:
                        return score, move
                    if score < low_score:
                        low_score = score
                        best_move = move
                return low_score, best_move
			
			# Need to go deeper
            for move in legal_moves:
                score, _ = self.alphabeta(game.forecast_move(move), depth - 1, alpha, beta, maximizing_player=True)
				# Check if losing move
                if score == float("-inf"):
                    return score, move
                if score <= alpha:
                    return score, move
                if score < low_score:
                    low_score = score
                    best_move = move
                beta = min(beta, low_score)
            return low_score, best_move
		
