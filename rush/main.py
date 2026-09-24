"""
โปรแกรมทดสอบสำหรับ Rush00
"""
from checkmate import checkmate


def main():
    # ตัวอย่างกระดานที่ 1 จากโจทย์
    board = """\
R...
.K..
..P.
....\
"""
    checkmate(board)


if __name__ == "__main__":
    main()
