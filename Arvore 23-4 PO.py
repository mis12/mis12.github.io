#Arvore 23-4 Pesquisa Ordenação

class DataItem:

	def __init__(self, dd):	#Metodo de criação de Objetos
	#Estado inicial especifico
		self.dData = dd

	def displayItem(self):	#formato " /27"
		print '/', self.dData,
#fim da class DataItem

class Node:
	_ORDER = 4
	def __init__(self):
		self._numItems = 0
		self._pParent = None
		self._childArray = []	#Ordenar o nó
		self._itemArray = []	#ordenar Data
		for j in xrange(self._ORDER):	#inicializar o ordenador
			self._childArray.append(None)
		for k in xrange(self._ORDER - 1):
			self._itemArray.append(None)

			#Conecta o filho com o nó
	def connectChild(self, childNum, pChild):
		self._childArray[childNum] = pChild
		if pChild:
			pChild._pParent = self

			#Desconecta o filho, e retorna
	def disconnectChild(self, childNum):
		pTempNode = self._childArray[childNum]
		self._childArray[childNum] = None
		return pTempNode

	def getChild(self, childNum):
		return self._childArray[childNum]

	def getParent(self):
		return self._pParent

	def isLeaf(self):
		return not self._childArray[0]

	def getNumItems(self):
		return self._numItems

	def getItem(self, index):	#Retonar o DataItem
		return self._itemArray[index]

	def isFull(self):
		return self._numItems==self._ORDER - 1

	def findItem(self, key):	#Retorna o dado de busca
		for j in xrange(self._ORDER-1):	#Buscando
			if not self._itemArray[j]:	#para busca
				break
			elif self._itemArray[j].dData == key:	#Retorna valor
				return j
		return -1
                                        #Fim da busca

	def insertItem(self, pNewItem):
		#Assume que nó não está cheio
		self._numItems += 1#Adicionando Item novo
		newKey = pNewItem.dData	#Chave do novo item

		for j in reversed(xrange(self._ORDER-1)):	#Começar pela direita,	#examinar os itens
			if self._itemArray[j] == None:	#Se item for nulo,
				pass	#passe para a esquerda
			else:	#Não nulo
				itsKey = self._itemArray[j].dData	#Obtem chave
				if newKey < itsKey:	#Se for maior
					self._itemArray[j+1] = self._itemArray[j]	#Troca para direita
				else:
					self._itemArray[j+1] = pNewItem	#Insere novo valor
					return j+1#Retorna novo indice para o item
			#vim do else para não nulo
		#fim do for	#Trocado todos os valores
		self._itemArray[0] = pNewItem	#Insere novo item
		return 0
	#fim da def>insertItem()

	def removeItem(self):	#Remove o maior item
		#Assume que nó não está vázio
		pTemp = self._itemArray[self._numItems-1]	#Salva o item
		self._itemArray[self._numItems-1] = None	#Retira o item
		self._numItems -= 1 #numero retirado
		return pTemp#returna item

	def displayNode(self):	#formato "/24/56/74"
		for j in xrange(self._numItems):
			self._itemArray[j].displayItem()	#formato "/56"
		print '/'	#final para separa os nos "/"

#fim da class Node

class Tree234:

	def __init__(self):
		self._pRoot = Node()	#Nó raiz

	def find(self, key):
		pCurNode = self._pRoot	#Começa o nó
		while True:
			childNumber=pCurNode.findItem(key)
			if childNumber != -1:
				return childNumber	#Encontrado
			elif pCurNode.isLeaf():
				return -1 #nao achado, buscar no proximo filho
			else:	#Buscando no proximo filho
				pCurNode = self.getNextChild(pCurNode, key)
		#fim da busca while

	def insert(self, dValue):	#inserir em DataItem
		pCurNode = self._pRoot
		pTempItem = DataItem(dValue)

		while True:
			if pCurNode.isFull():	#Quando o nó estiver lotado
				self.split(pCurNode)	#Divide o nó
				pCurNode = pCurNode.getParent() #copia os dados
                                #procura os dados
				pCurNode = self.getNextChild(pCurNode, dValue)
			#fim if do nó de busca (lotado)

			elif pCurNode.isLeaf():	#nó filhos(folha),
				break   #insere
			#O nó nao está cheio. Faça para o nivel mais abaixo
			else:
				pCurNode = self.getNextChild(pCurNode, dValue)
		#fim do while
		pCurNode.insertItem(pTempItem)	#Insere um novo item
	#fim do insert() o nó mais chato

	def split(self, pThisNode):	#divide o nó
		#Assume que o nó está lotado
		
		pItemC = pThisNode.removeItem()	#Remove o item
		pItemB = pThisNode.removeItem()	#Este nó
		pChild2 = pThisNode.disconnectChild(2)	#Remove o filho
		pChild3 = pThisNode.disconnectChild(3)	#A partid do nó

		pNewRight = Node()	#Faz um novo nó

		if pThisNode == self._pRoot:	#Se esta é a raiz,
			self._pRoot = Node()	#Faça uma nova raiz
			pParent = self._pRoot	#a raiz e o pai
			self._pRoot.connectChild(0, pThisNode)	#Conecta o pai ao filho
		else:	#Este nó não é a raiz
			pParent = pThisNode.getParent()	#Obtem o pai do filho criado

		#deal with parent
		itemIndex = pParent.insertItem(pItemB)
		n = pParent.getNumItems()	#total de itens

		j = n-1#Move o pai
		while j > itemIndex:	#Connecta
			pTemp = pParent.disconnectChild(j)	#Um filho
			pParent.connectChild(j+1, pTemp)	#para a direita
			j -= 1
				#conecta o novo filho da direita ao pai
		pParent.connectChild(itemIndex+1, pNewRight)

		#vá para a direita
		pNewRight.insertItem(pItemC)	#item C da direita
		pNewRight.connectChild(0, pChild2)	#Conecta 0 ou 1
		pNewRight.connectChild(1, pChild3)	#ativa direita
	#fim da split()

	#obtem o filho correto durante este nó
	def getNextChild(self, pNode, theValue):
		#Assume que o nó não está vazio, nem cheio, nem uma folha
		numItems = pNode.getNumItems()
		
		for j in xrange(numItems):	#para cada item do nó
			if theValue < pNode.getItem(j).dData:	
				return pNode.getChild(j)	#returna filho esquerdo
		else:	 	#Valor vamor então 
			return pNode.getChild(j + 1)	#returna filho direito
                #fim do for
	def displayTree(self):
		self.recDisplayTree(self._pRoot, 0, 0)

	def recDisplayTree(self, pThisNode, level, childNumber):
		print 'level=', level, 'filho=', childNumber,
		pThisNode.displayNode()	#Exibir o nó

		numItems = pThisNode.getNumItems()
		for j in xrange(numItems+1):
			pNextNode = pThisNode.getChild(j)
			if pNextNode:
				self.recDisplayTree(pNextNode, level+1, j)
			else:
				return
	#fim da recDisplayTree()
#fim da class Tree234

pTree = Tree234()
pTree.insert(50)
pTree.insert(40)
pTree.insert(60)
pTree.insert(30)
pTree.insert(70)


def show():
	pTree.displayTree()

def insert():
	value = int(raw_input('Entre com o valor: '))
	pTree.insert(value)

def find():
	value = int(raw_input('Enter value to find: '))
	found = pTree.find(value)
	if found != -1:
		print 'Encontrado', value
	else:
		print 'Não encontrado', value

case = { 's' : show,
	'i' : insert,
	'f' : find}

while True:
	print
	choice = raw_input('Entrar com a letra na qual deseja Executar: ')
	if case.get(choice, None):
		case[choice]()
	else:
		print 'Entrada Invalida'
#end while
del pTree
#fim do programa
