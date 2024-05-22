from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt
from rich.align import Align

import os

from battleship import Game, GameState, Board


console = Console()
# shrinks window by 2 line to make room for prompt which is not part of the layout
_width, _height = os.get_terminal_size()
console.size = (_width, _height-2)

layout = Layout()
gameMenu = Layout(name="GameMenu")



game = Game()
game.setup()
game.autoPlacePieces()
game.gameLoop()
state = GameState()

# Initial TUI setup
layout.split(
    Layout(Panel(
        Align.center(
            "BattlePy"
        )),
        size=3, name="Title"),
    Layout(ratio=1, name="main"),
    Layout(size=10, name="footer"),
)


layout["main"].split_row(
    Layout(name="side"),
    Layout(name="body", ratio=2),
    Layout(name="right")
)

layout['side'].split(
    Layout(Panel("X input: ", title= "X input"), name="XInput"),
    Layout(Panel("Y input: ", title= "Y input"), name="YInput"),
    Layout(Panel("S = Shoot\nQ = quit\nC = Change", title= "Actions"), name="Actions"),
)

layout['body'].update(Panel(game.board.print()))
layout['right'].update(Panel(f"Block remaining: {game.numOfActiveBoats} "))

layout['footer'].update(Panel(
    '''
" " = WATER 
"#" = BOAT 
"@" = HIT
"_" = MISS
"*" = SELECTED
    '''
))

# console.print(layout)

def validateInput(state: GameState, board: Board):
    # Checks for user input to be inside gameBoard
    if (state.userInputX > board.WIDTH - 1) or (state.userInputY > board.LENGTH - 1) :
        return False
    return True
    

def refreshScreenGameLoop(state: GameState):
    # Refreshes the screen, populates the data from GameState object
    game.gameLoop()
    layout["XInput"].update(Layout(Panel(f"X input: {state.userInputX}")))
    layout["YInput"].update(Layout(Panel(f"Y input: {state.userInputY}")))
    layout['right'].update(Panel(f"Block remaining: {state.blocsRemaining}\nNum of Moves: {state.numOfMove}"))
    if state.showHighlated:
        layout['body'].update(Panel(Align.center(game.board.printHighlighted(), 
                                                 vertical="middle")))
    else:
        layout['body'].update(Panel(Align.center(game.board.print(), 
                                                 vertical="middle")))
    console.clear()
    console.print(layout)

def initScreen():
    # Welcome screen
    gameMenu.split(
        Layout(Panel(
            Align.center(
                "BattlePy The Game"
            )),
            size=3, name="Title"),
        Layout(ratio=1, name="main"),
        Layout(Panel("C = Continue\nQ = quit\n", title= "Actions"), name="Actions", size=10),
    )

    gameMenu['main'].update(Panel("Welcome to the game"))
    console.clear()
    console.print(gameMenu)

def gameTick():
    state.showHighlated = False
    state.userInputX = 0
    state.userInputY = 0
    state.blocsRemaining = game.getActiveBoats()
    refreshScreenGameLoop(state)

    state.userInputX = IntPrompt.ask("X Input: \n", default=0)
    state.showHighlated = True
    if validateInput(state, game.board) is False:
        return 
    refreshScreenGameLoop(state)
    game.board.highlight(int(state.userInputX), None)
    refreshScreenGameLoop(state)
    state.userInputY = IntPrompt.ask("Y Input: \n", default=0)
    if validateInput(state, game.board) is False:
        return
    game.board.highlight(int(state.userInputX), int(state.userInputY))
    state.showHighlated = True
    layout['body'].update(Panel(game.board.printHighlighted()))
    refreshScreenGameLoop(state)
    NextAction = Prompt.ask("Action: \n", default="s")
    NextAction = NextAction.lower()


    if NextAction == 'q':
        exit()

    if NextAction != "c":
        state.showHighlated = False
        state.IncrementMoves()
        game.shoot(int(state.userInputX), int(state.userInputY))
    refreshScreenGameLoop(state)


initScreen()
NextAction = Prompt.ask("Play?: \n", default="y")
if NextAction == 'q':
        exit()
while True:
    gameTick()
    
  




