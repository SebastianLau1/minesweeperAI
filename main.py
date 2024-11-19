from minesweeper import Minesweeper
from minesweeper_ai import MinesweeperAI

def play_game():
    game = Minesweeper()
    ai = MinesweeperAI()

    while True:
        # AI makes a safe move if possible
        move = ai.make_safe_move()
        if move is None:
            # AI makes a random move if no safe move is known
            move = ai.make_random_move()
            if move is None:
                print("No moves left to make.")
                break

        # Make the move and update AI knowledge
        if game.is_mine(move):
            print(f"AI stepped on a mine at {move}!")
            break
        else:
            count = game.nearby_mines(move)
            game.reveal(move)
            ai.add_knowledge(move, count)

        # Check for win condition
        if len(ai.moves_made) == game.height * game.width - game.mines:
            print("AI has successfully cleared the board!")
            break

if __name__ == "__main__":
    play_game()
