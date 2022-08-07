from Board import Board

ROWS, COLUMNS = 21, 21


def main():
    b = Board(ROWS, COLUMNS)
    print(f"END GAME\n\nSCORE: {b.play()}")


if __name__ == '__main__':
    main()
