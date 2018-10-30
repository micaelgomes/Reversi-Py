# Reversi
import random
import sys

def drawBoard(board):
	# Essa funcao desenha o tabuleiro
	HLINE = '  +---+---+---+---+---+---+---+---+'
	VLINE = '  |   |   |   |   |   |   |   |   |'

	print('    1   2   3   4   5   6   7   8')
	print(HLINE)

	for y in range(8):
		print(VLINE)
		print(y+1, end=' ')
		for x in range(8):
			print('| %s' % (board[x][y]), end=' ')
		print('|')
		print(VLINE)
		print(HLINE)

def resetBoard(board):
	#Essa funcao esvazia o tabuleiro
	for x in range(8):
		for y in range(8):
			board[x][y] = ' '
	# Pecas iniciais:
	board[3][3] = 'X'
	board[3][4] = 'O'
	board[4][3] = 'O'
	board[4][4] = 'X'

def getNewBoard():
	# Criar um tabuleiro novo
	board = []
	for i in range(8):
		board.append([' '] * 8)
	return board

def isValidMove(board, tile, xstart, ystart):
	# Retorna False se o movimento em xstart, ystart é invalido
	# Se o movimento é valido, retorna uma lista de casas que devem ser viradas após o movimento
	if board[xstart][ystart] != ' ' or not isOnBoard(xstart, ystart):
		return False
	board[xstart][ystart] = tile 
	if tile == 'X':
		otherTile = 'O'
	else:
		otherTile = 'X'
	tilesToFlip = []
	for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
		x, y = xstart, ystart
		x += xdirection # first step in the direction
		y += ydirection # first step in the direction
		if isOnBoard(x, y) and board[x][y] == otherTile:
			x += xdirection
			y += ydirection
			if not isOnBoard(x, y):
				continue
			while board[x][y] == otherTile:
				x += xdirection
				y += ydirection
				if not isOnBoard(x, y):
					break
			if not isOnBoard(x, y):
				continue
			if board[x][y] == tile:
				while True:
					x -= xdirection
					y -= ydirection
					if x == xstart and y == ystart:
						break
					tilesToFlip.append([x, y])
	board[xstart][ystart] = ' '
	if len(tilesToFlip) == 0:
		return False
	return tilesToFlip
 
def isOnBoard(x, y):
	# Retorna True se a casa está no tabuleiro.
	return x >= 0 and x <= 7 and y >= 0 and y <=7

def getBoardWithValidMoves(board, tile):
	# Retorna um tabuleiro com os movimentos validos
	dupeBoard = getBoardCopy(board)
	for x, y in getValidMoves(dupeBoard, tile):
		dupeBoard[x][y] = '.'
	return dupeBoard

def getValidMoves(board, tile):
	# Retorna uma lista de movimentos validos
	validMoves = []
	for x in range(8):
		for y in range(8):
			if isValidMove(board, tile, x, y) != False:
				validMoves.append([x, y])
	return validMoves

def getScoreOfBoard(board):
	# Determina o score baseado na contagem de 'X' e 'O'.
	xscore = 0
	oscore = 0
	for x in range(8):
		for y in range(8):
			if board[x][y] == 'X':
				xscore += 1
			if board[x][y] == 'O':
				oscore += 1
	return {'X':xscore, 'O':oscore}

def enterPlayerTile():
	# Permite que o player escolha ser X ou O
	tile = ''
	while not (tile == 'X' or tile == 'O'):
		print('Escolha suas peças: X ou O?')
		tile = input().upper()
	if tile == 'X':
		return ['X', 'O']
	else:
	  return ['O', 'X']

def whoGoesFirst():
	# Escolhe aleatóriamente quem começa.
	if random.randint(0, 1) == 0:
		return 'computer'
	else:
		return 'player'

def playAgain():
	# Retorna True se o player quer jogar novamente
	print('Quer jogar novamente? (yes ou no)')
	return input().lower().startswith('y')

def makeMove(board, tile, xstart, ystart):
	# Coloca a peça no tabuleiro em xstart, ystart, e as peças do oponente
	# Retorna False se for um movimento invalido
	tilesToFlip = isValidMove(board, tile, xstart, ystart)
	if tilesToFlip == False:
		return False
	board[xstart][ystart] = tile
	for x, y in tilesToFlip:
		board[x][y] = tile
	return True

def getBoardCopy(board):
	# Faz uma cópia do tabuleiro e retorna a cópia
	dupeBoard = getNewBoard()
	for x in range(8):
		for y in range(8):
			dupeBoard[x][y] = board[x][y]
	return dupeBoard

def isOnCorner(x, y):
	# Retorna True se a posição x, y é um dos cantos do tabuleiro
	return (x == 0 and y == 0) or (x == 7 and y == 0) or (x == 0 and y == 7) or (x == 7 and y == 7)

def getPlayerMove(board, playerTile):
	# Permite que o player insira sua jogada
	DIGITS1TO8 = '1 2 3 4 5 6 7 8'.split()
	while True:
		print('Insira seu movimento, ou insira quit para sair do jogo, ou hints para ativar/desativar dicas.')
		move = input().lower()
		if move == 'quit':
			return 'quit'
		if move == 'hints':
			return 'hints'
		if len(move) == 2 and move[0] in DIGITS1TO8 and move[1] in DIGITS1TO8:
			x = int(move[0]) - 1
			y = int(move[1]) - 1
			if isValidMove(board, playerTile, x, y) == False:
			  print('Essa não é uma jogada válida')
			  continue
			else:
			  break
		else:
			print('Essa não é uma jogada válida, digite o valor de x (1-8), depois o valor de y (1-8).')
			print('Por exemplo, 81 será o canto superior direito.')
	return [x, y]

def getComputerMove(board, computerTile):
	# Permite ao computador executar seu movimento
	possibleMoves = getValidMoves(board, computerTile)
	# randomiza a ordem dos possíveis movimentos
	random.shuffle(possibleMoves)
	# se for possivel, joga no canto
	for x, y in possibleMoves:
		if isOnCorner(x, y):
			return [x, y]
	# Escolhe a jogada que resulta em mais pontos
	bestScore = -1
	for x, y in possibleMoves:
		dupeBoard = getBoardCopy(board)
		makeMove(dupeBoard, computerTile, x, y)
		score = getScoreOfBoard(dupeBoard)[computerTile]
		if score > bestScore:
			bestMove = [x, y]
			bestScore = score
	return bestMove

def showPoints(playerTile, computerTile):
	# Mostra o score atual
	scores = getScoreOfBoard(mainBoard)
	print('Player1: %s ponto(s). \nComputador: %s ponto(s).' % (scores[playerTile], scores[computerTile]))

############### Minhas Funções #############################
class Tree(object):
	def __init__(self, turn, board, father=None):
		self.father = father
		self.child = []
		self.moves = []
		self.bestChild = None
		self.turn = turn		# Max ou Min
		self.board = board		#
		self.value = None
		self.bestX = None
		self.bestY = None	
			
	
	def addChild(self, turn, board):
		newNode = Tree(turn, board, self)
		self.child.append(newNode)

def minMaxStrategy(turn, tile, board, father, level):
	if level <= 0:
		return None
	if tile == 'X':
		otherTile = 'O'
	else:
		otherTile = 'X'
	if turn == 'computer':
		otherTurn = 'player'
	else:
		otherTurn = 'computer'
	newNode = Tree(turn, board, father)
	possibleMoves = getValidMoves(board, tile)
	if level>1 and possibleMoves != []:
		for x,y in possibleMoves:
			dupeBoard = getBoardCopy(board)
			makeMove(dupeBoard, tile, x, y) #realizando ação possível do turno
			filho = minMaxStrategy(otherTurn, otherTile, dupeBoard, newNode, level-1)
			newNode.child.append(filho)
			if(newNode.child[len(newNode.child)-1]!= None):
				newNode.child[len(newNode.child)-1].x = x
				newNode.child[len(newNode.child)-1].y = y
		if turn == 'computer': #Escolher o filho com maior value (Estado de Max)
			score = -9999999999999
			for node in newNode.child:
				if node != None and node.value > score:
					score = node.value
					newNode.bestX = node.x
					newNode.bestY = node.y
			newNode.value = score
		else: #Escolher o filho de menor value (Estado de Min)
			score = 9999999999999
			for node in newNode.child:
				if node != None and node.value < score:
					score = node.value
					newNode.bestX = node.x
					newNode.bestY = node.y
			newNode.value = score
	else:
		score = getScoreOfBoard(board)
		if(turn == 'player'):
			newNode.value = score[otherTile] - score[tile]
		else:
			newNode.value = score[tile]-score[otherTile]
	return newNode

def update(strategy, x, y):
	for node in strategy.child:
		if node != None and (node.x == x and node.y == y):
			return node
	return None
###########################################################
print('Welcome to Reversi!')
while True:
	# Reseta o jogo e o tabuleiro
	level = input("Escolha o level desejado:\n 1 -> Dummy\n 2 -> ok\n 3 -> hard\n 4 -> expert\n")
	mainBoard = getNewBoard()
	resetBoard(mainBoard)
	playerTile, computerTile = enterPlayerTile()
	showHints = False
	turn = whoGoesFirst()

	print('O ' + turn + ' começa o jogo.')
	if turn == 'player':
		char = playerTile
	else:
		char = computerTile
	#strategy = minMaxStrategy(turn, char, getBoardCopy(mainBoard), None, 4)
	x, y = None, None
	if(level == '1'):
		level = 2
	elif level == '2':
		level = 3
	elif level == '3':
		level = 4
	else:
		level = 5
	while True:
		if turn == 'computer':
			# Player's turn.
			if showHints:
				validMovesBoard = getBoardWithValidMoves(mainBoard, playerTile)
				drawBoard(validMovesBoard)
			else:
				drawBoard(mainBoard)
			showPoints(playerTile, computerTile)
			#Alterar o move para o da minMax
			#if x != None: #Computer fez ação
			#	strategy = update(strategy, x, y)
			#if strategy == None:
			strategy = minMaxStrategy(turn, computerTile, getBoardCopy(mainBoard), None, level)
			
			moveComputer = [strategy.bestX, strategy.bestY]
			strategy = update(strategy, moveComputer[0], moveComputer[1]) #
			
			#move = getPlayerMove(mainBoard, playerTile)
			if moveComputer == 'quit':
				print('Obrigado por jogar!')
				sys.exit() # terminate the program
			elif moveComputer == 'hints':
				showHints = not showHints
				continue
			else:
				makeMove(mainBoard, computerTile, moveComputer[0], moveComputer[1])
			if getValidMoves(mainBoard, playerTile) == []:
				break
			else:
				turn = 'player'
		else:
			# Player's turn.
			if showHints:
				validMovesBoard = getBoardWithValidMoves(mainBoard, playerTile)
				drawBoard(validMovesBoard)
			else:
				drawBoard(mainBoard)
			showPoints(playerTile, computerTile)
			move = getPlayerMove(mainBoard, playerTile)
			if move == 'quit':
				print('Obrigado por jogar!')
				sys.exit() # terminate the program
			elif move == 'hints':
				showHints = not showHints
				continue
			else:
				makeMove(mainBoard, playerTile, move[0], move[1])
			if getValidMoves(mainBoard, computerTile) == []:
				break
			else:
				turn = 'computer'
	# Mostra o resultado final.
	drawBoard(mainBoard)
	scores = getScoreOfBoard(mainBoard)
	print('X: %s ponto(s) \nO: %s ponto(s).' % (scores['X'], scores['O']))
	if scores[playerTile] > scores[computerTile]:
		print('Você venceu o computador por %s ponto(s)! \nParabéns!' % (scores[playerTile] - scores[computerTile]))
	elif scores[playerTile] < scores[computerTile]:
		print('Você perdeu!\nO computador venceu você por %s ponto(s).' % (scores[computerTile] - scores[playerTile]))
	else:
		print('Empate!')
	if not playAgain():
		break