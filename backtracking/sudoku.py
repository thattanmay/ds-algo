class Position:
    def __init__(self, y, x) -> None:
        self.y = y
        self.x = x
        self.values = []

    def next(self):
        return Position(
            self.y + 1 if self.x == 8 else self.y,
            (self.x + 1) % 9,
        )


class Sudoku():
    # keep a stack for the updated numbers, used to backtrack
    update_stack: list[Position] = []

    def __init__(self, board) -> None:
        self.board = board

    def display(self):
        print('\n\n')
        print(f" {'-' * 23} ")
        for index, row in enumerate(self.board):
            if index and index % 3 == 0:
                print(f"|{'-' * 23}|")
            print(
                f"{' '.join([str(val) if i % 3 != 0 else f'| {str(val)}' for i, val in enumerate(row)])} |"
            )
        print(f" {'-' * 23} \n\n")

    def check(self, val, pos: Position):
        if (val in self.board[pos.y]) or (val
                                          in [r[pos.x] for r in self.board]):
            return False

        for ix in [i for i in ((0, 1, 2), (3, 4, 5), (6, 7, 8))
                   if pos.x in i][0]:
            for iy in [
                    i for i in ((0, 1, 2), (3, 4, 5), (6, 7, 8)) if pos.y in i
            ][0]:
                if val == self.board[iy][ix]:
                    return False

        return True

    def insert_number(self, pos: Position):
        """Place a number from 1-9 after self.check
        Also make sure the number doesn't take previous value when backtracked

        Args:
            pos (Position): current position for number to be placed into

        Returns:
            _type_: value to number placed
        """
        for val in range(1, 10):
            if val not in pos.values and self.check(val, pos):
                self.board[pos.y][pos.x] = val
                return val
        return ""

    def solve(self, pos=Position(0, 0)):
        if pos.y == 9:
            return
        if self.board[pos.y][pos.x] == 0 or (self.update_stack
                                             and pos == self.update_stack[-1]):

            if self.update_stack and pos == self.update_stack[-1]:
                self.update_stack.pop()

            val = self.insert_number(pos)
            if val:
                pos.values.append(val)
                self.update_stack.append(pos)
                self.solve(pos.next())
            else:
                if self.update_stack:
                    self.board[pos.y][pos.x] = 0
                self.solve(self.update_stack[-1])
        else:
            self.solve(pos.next())


board = [
    [int(i) for i in '060158070'],
    [int(i) for i in '008009200'],
    [int(i) for i in '730002018'],
    [int(i) for i in '957020000'],
    [int(i) for i in '020000403'],
    [int(i) for i in '300685007'],
    [int(i) for i in '003040805'],
    [int(i) for i in '604500700'],
    [int(i) for i in '005870064'],
]

sudoku = Sudoku(board)

sudoku.display()

sudoku.solve()

sudoku.display()