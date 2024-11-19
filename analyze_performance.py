import matplotlib.pyplot as plt
from minesweeper import Minesweeper
from minesweeper_ai import MinesweeperAI

def run_simulations(num_games=100):
    success_count = 0

    for _ in range(num_games):
        game = Minesweeper()
        ai = MinesweeperAI()

        while True:
            move = ai.make_safe_move()
            if move is None:
                move = ai.make_random_move()
                if move is None:
                    # No moves left
                    break

            if game.is_mine(move):
                # AI hit a mine
                break
            else:
                count = game.nearby_mines(move)
                game.reveal(move)
                ai.add_knowledge(move, count)

            if len(ai.moves_made) == game.height * game.width - game.mines:
                # AI cleared the board
                success_count += 1
                break

    success_rate = (success_count / num_games) * 100
    print(f"AI success rate: {success_rate}%")

    # Plot the results
    plt.bar(['Success', 'Failure'], [success_count, num_games - success_count], color=['green', 'red'])
    plt.title('AI Performance over Multiple Games')
    plt.ylabel('Number of Games')
    plt.show()

if __name__ == "__main__":
    run_simulations()
