import random


class Sentence:
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells and a count of the number of those cells which are mines.
    """
    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return set(self.cells)
        return set()

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if self.count == len(self.cells):
            return set(self.cells)
        return set()

    def remove_knowns(self, safes, mines):
        """
        Removes any cells known to be safe or mines from the sentence.
        """
        self.cells -= safes
        self.cells -= mines

class MinesweeperAI:
    """
    Minesweeper game player
    """
    def __init__(self, height=16, width=16):
        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of moves made
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        self.mines.add(cell)
        self.update_knowledge_with_cell(cell, is_mine=True)

    def mark_safe(self, cell):
        self.safes.add(cell)
        self.update_knowledge_with_cell(cell, is_mine=False)

    def update_knowledge_with_cell(self, cell, is_mine):
        """
        Updates all sentences in knowledge base with the information that
        a cell is known to be a mine or known to be safe.
        """
        for sentence in self.knowledge:
            if cell in sentence.cells:
                sentence.cells.remove(cell)
                if is_mine:
                    sentence.count -= 1

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines.
        """
        # Mark the cell as a move made
        self.moves_made.add(cell)

        # Mark the cell as safe
        self.mark_safe(cell)

        # Add a new sentence to the AI's knowledge base
        neighbors = self.get_neighbors(cell)
        new_sentence = Sentence(neighbors, count)
        self.knowledge.append(new_sentence)

        # Update knowledge base
        self.update_knowledge()

    def get_neighbors(self, cell):
        """
        Returns a set of neighboring cells that are not yet known to be safe or mines.
        """
        neighbors = set()
        for i in range(max(0, cell[0] - 1), min(self.height, cell[0] + 2)):
            for j in range(max(0, cell[1] - 1), min(self.width, cell[1] + 2)):
                if (i, j) != cell and (i, j) not in self.safes and (i, j) not in self.mines:
                    neighbors.add((i, j))
        return neighbors

    def update_knowledge(self):
        """
        Updates the AI's knowledge base by marking additional cells as safe or as mines
        when it can be concluded based on the AI's knowledge base.
        """
        changed = True
        while changed:
            changed = False

            # Collect all safes and mines identified in this iteration
            safes = set()
            mines = set()

            # Check all sentences in the knowledge base
            for sentence in self.knowledge:
                # Identify known safes and mines
                safes.update(sentence.known_safes())
                mines.update(sentence.known_mines())

            # Mark any new cells as safe
            if safes:
                changed = True
                for cell in safes:
                    if cell not in self.safes:
                        self.mark_safe(cell)

            # Mark any new cells as mines
            if mines:
                changed = True
                for cell in mines:
                    if cell not in self.mines:
                        self.mark_mine(cell)

            # Remove empty sentences
            self.knowledge = [s for s in self.knowledge if s.cells]

            # Infer new sentences by comparing pairs of sentences
            for sentence1 in self.knowledge:
                for sentence2 in self.knowledge:
                    if sentence1 != sentence2 and sentence1.cells and sentence2.cells:
                        if sentence1.cells.issubset(sentence2.cells):
                            new_cells = sentence2.cells - sentence1.cells
                            new_count = sentence2.count - sentence1.count
                            new_sentence = Sentence(new_cells, new_count)
                            if new_sentence not in self.knowledge:
                                self.knowledge.append(new_sentence)
                                changed = True

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        """
        for move in self.safes:
            if move not in self.moves_made:
                return move
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that have not yet been chosen
        and are not known to be mines, using probabilistic reasoning.
        """
        possible_moves = [(i, j) for i in range(self.height) for j in range(self.width)
                          if (i, j) not in self.moves_made and (i, j) not in self.mines]
        if not possible_moves:
            return None

        # Implement probabilistic reasoning to choose the best move
        probabilities = {}
        for cell in possible_moves:
            probabilities[cell] = self.calculate_mine_probability(cell)

        # Choose the cell with the lowest probability of being a mine
        min_prob = min(probabilities.values())
        best_moves = [cell for cell in probabilities if probabilities[cell] == min_prob]
        return random.choice(best_moves)

    def calculate_mine_probability(self, cell):
        """
        Calculates the probability of a cell being a mine based on the AI's knowledge base.
        """
        total_prob = 0
        count = 0
        for sentence in self.knowledge:
            if cell in sentence.cells:
                total_prob += sentence.count / len(sentence.cells)
                count += 1
        return total_prob / count if count > 0 else 1  # Assume max probability if no information
