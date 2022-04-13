import random
import time
import math
import copy
from board import Board


class node:
 
    def __init__(self, pos, parent):
        self.pos = pos
        self.children = []
        self.parent= parent
        self.depth =1
        self.win=0
        self.times=0
 
    def add(self, node):
        self.children.append(node)
        node.depth=self.depth+1
 
    
class HumanPlayer:
    """
    人类玩家
    """

    def __init__(self, color):
        """
        玩家初始化
        :param color: 下棋方，'X' - 黑棋，'O' - 白棋
        """
        self.color = color
    

    def get_move(self, board):
        """
        根据当前棋盘输入人类合法落子位置
        :param board: 棋盘
        :return: 人类下棋落子位置
        """
        # 如果 self.color 是黑棋 "X",则 player 是 "黑棋"，否则是 "白棋"
        if self.color == "X":
            player = "黑棋"
        else:
            player = "白棋"

        # 人类玩家输入落子位置，如果输入 'Q', 则返回 'Q'并结束比赛。
        # 如果人类玩家输入棋盘位置，e.g. 'A1'，
        # 首先判断输入是否正确，然后再判断是否符合黑白棋规则的落子位置
        while True:
            action = input(
                    "请'{}-{}'方输入一个合法的坐标(e.g. 'D3'，若不想进行，请务必输入'Q'结束游戏。): ".format(player,
                                                                                 self.color))

            # 如果人类玩家输入 Q 则表示想结束比赛
            if action == "Q" or action == 'q':
                return "Q"
            else:
                row, col = action[1].upper(), action[0].upper()

                # 检查人类输入是否正确
                if row in '12345678' and col in 'ABCDEFGH':
                    # 检查人类输入是否为符合规则的可落子位置
                    if action in board.get_legal_actions(self.color):
                        return action
                else:
                    print("你的输入不合法，请重新输入!")





class AIPlayer:
    """
    AI 玩家
    """

    def __init__(self, color):
        """
        玩家初始化
        :param color: 下棋方，'X' - 黑棋，'O' - 白棋
        """

        self.color = color
    #---------------------------------------------
    
    def random_choice(self, board):
        """
        从合法落子位置中随机选一个落子位置
        :param board: 棋盘
        :return: 随机合法落子位置, e.g. 'A1' 
        """
        # 用 list() 方法获取所有合法落子位置坐标列表
        action_list = list(board.get_legal_actions(self.color))

        # 如果 action_list 为空，则返回 None,否则从中选取一个随机元素，即合法的落子坐标
        if len(action_list) == 0:
            return None
        else:
            return random.choice(action_list)
    #-----------------------------------------------

    def get_move(self, board):
        """
        根据当前棋盘状态获取最佳落子位置
        :param board: 棋盘
        :return: action 最佳落子位置, e.g. 'A1'
        """
        if self.color == 'X':
            player_name = '黑棋'
        else:
            player_name = '白棋'
        print("请等一会，对方 {}-{} 正在思考中...".format(player_name, self.color))

        # -----------------请实现你的算法代码--------------------------------------
        
        action = None
        action = self.uctsearch(board)
        return action
    
    def select(self,parent,board1):
        maxucb=float('-inf')
        for children in parent.children:
            #print(children.pos,end='')
            if children.times==0:
                ucb=float('inf')
            else:
                c=math.sqrt(2)/2
                ucb=children.win/children.times+c*math.sqrt(2*math.log(parent.times)/children.times)
            if ucb>maxucb:
                nextnode=children
        if parent.depth%2==1:
            nextcolor=self.color
        else:
            if self.color=='X':
                nextcolor='O'
            else:
                nextcolor='X'
        board1._move(nextnode.pos,nextcolor)
        #board1.display()
        l=nextnode.children
        #print(nextnode.depth,nextcolor)
        #board1.display()
        if len(l)==0:
            #print(nextnode.pos)
            return nextnode
        else:
            return self.select(nextnode,board1)
        
    def expand(self,vselect,board1):
        if vselect.depth%2==1:
            color=self.color
        else:
            if self.color=='X':
                color='O'
            else:
                color='X'
        v0=board1.get_legal_actions(color)
        for i in v0:
            vselect.add(node(i,vselect))
        if len(list(v0)) ==0:
            return vselect
        choice = random.choice(vselect.children)
        board1._move(choice.pos,color)
        return choice
    
    
    def simulate(self,vexpand,board1):
        
        d=vexpand.depth%2
        if d==1:
            color=self.color
        else:
            if self.color=='X':
                color='O'
            else:
                color='X'
        nextmove=list(board1.get_legal_actions(color))
        while len(nextmove)!=0:
            board1._move(random.choice(nextmove),color)
            if color=='X':
                color='O'
            else:
                color='X'
            nextmove=list(board1.get_legal_actions(color))
            #print(1)
        winner=board1.get_winner()
        if self.color=='X':
            b=0
        else:
            b=1
        if winner==b:
            return 1
        elif winner==2:
            return 0
        else:
            return -1
    
    
    def backpropagate(self,vexpand,sresult):
        v=vexpand
        while v!=None:
            v.times=v.times+1
            if v.depth%2==0:
                v.win=v.win+sresult
            else:
                v.win=v.win-sresult
            v=v.parent
        
    def uctsearch(self,board):
        root=node('0',None)
        c=math.sqrt(2)/2
        v0=board.get_legal_actions(self.color)
        for i in v0:
            root.add(node(i,root))
        
        t0=t1=time.time()
        board1=Board()
        while t1-t0<5:
            
            board1._board=copy.deepcopy(board._board)
            #board1.display()
            vselect=self.select(root,board1)
            #print(type(vselect))
            #print(1)
            vexpand=self.expand(vselect,board1)
            #print(2)
            if vexpand==vselect:
                sresult=self.simulate(vexpand,board1)
            else:
                winner=board1.get_winner()
                if self.color=='X':
                    b=0
                else:
                    b=1
                if winner==b:
                    sresult=1
                elif winner==2:
                    sresult=0
                else:
                    sresult=-1
            #print(3)
            self.backpropagate(vexpand,sresult)
            #print(4)
            t1=time.time()
        max=float('-inf')
        for item in root.children:
            if item.times==0:
                ucb=float('inf')
            else:
                c=math.sqrt(2)/2
                ucb=item.win/item.times+c*math.sqrt(2*math.log(root.times)/item.times)
            if ucb>max:
                a=item.pos
        return a
        # ------------------------------------------------------------------------

    
    
from game import Game  

# 人类玩家黑棋初始化
black_player =  HumanPlayer("X")

# AI 玩家 白棋初始化
white_player = AIPlayer("O")

# 游戏初始化，第一个玩家是黑棋，第二个玩家是白棋
game = Game(black_player, white_player)

# 开始下棋
game.run()
