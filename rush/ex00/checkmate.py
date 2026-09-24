def checkmate(board):
    # ตรวจสอบว่า input ต้องเป็นสตริงและไม่ว่างเปล่า
    if not isinstance(board, str):
        return
    rows = [r for r in board.strip("\r\n").splitlines() if r]
    if not rows:
        return

    size = len(rows)

    # ตรวจสอบว่าเป็นสี่เหลี่ยมจัตุรัส (N x N) และหาตำแหน่ง King
    king_pos = None
    king_count = 0
    for r in range(size):
        if len(rows[r]) != size:
            return
        for c in range(size):
            if rows[r][c] == 'K':
                king_pos = (r, c)
                king_count += 1

    # ต้องมี King เพียงตัวเดียวเท่านั้น
    if king_count != 1:
        return

    kr, kc = king_pos

    # 1. ตรวจสอบการโจมตีจาก Pawn (P)
    # Pawn เดินกินทแยงขึ้นบน ดังนั้นมองย้อนจาก King ลงมาข้างล่าง 1 แถว ซ้ายและขวา
    for pr, pc in [(kr + 1, kc - 1), (kr + 1, kc + 1)]:
        if 0 <= pr < size and 0 <= pc < size and rows[pr][pc] == 'P':
            print("Success")
            return

    # 2. ตรวจสอบแนวตรง (R, Q) และแนวทแยง (B, Q)
    ray_patterns = [
        # แนวตรง 4 ทิศทาง (บน, ล่าง, ซ้าย, ขวา)
        ([(-1, 0), (1, 0), (0, -1), (0, 1)], ('R', 'Q')),
        # แนวทแยง 4 ทิศทาง
        ([(-1, -1), (-1, 1), (1, -1), (1, 1)], ('B', 'Q'))
    ]

    for directions, dangerous_pieces in ray_patterns:
        for dr, dc in directions:
            r, c = kr + dr, kc + dc
            while 0 <= r < size and 0 <= c < size:
                piece = rows[r][c]
                # ถ้าเจอหมากตัวใดก็ตามขวางทางอยู่
                if piece in 'PBRQK':
                    if piece in dangerous_pieces:
                        print("Success")
                        return
                    # หากเป็นหมากตัวอื่น ให้หยุดตรวจทิศทางนี้ (เพราะมีตัวขวางทาง)
                    break
                r += dr
                c += dc

    # หากตรวจสอบครบแล้วไม่โดนหมากใดคุกคาม
    print("Fail")