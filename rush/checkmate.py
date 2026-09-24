"""
Rush00 - ตรวจสอบสถานะการถูกโจมตีของ King (Checkmate Detection)
โมดูล: checkmate.py

โมดูลนี้ประกอบด้วยฟังก์ชัน checkmate() เพื่อตรวจสอบว่า
King บนกระดานหมากรุกที่กำหนด กำลังถูกหมากของศัตรูโจมตี (In Check) หรือไม่
"""


def parse_and_validate_board(board_input):
    """
    แยกบรรทัดและตรวจสอบความถูกต้องของกระดานหมากรุก

    รูปแบบที่รองรับ:
    - ข้อความแบบหลายบรรทัด (Multiline string เช่น board = \"\"\"R...\\n.K..\"\"\")
    - รายการหรือทูเพิลของแถว (List หรือ Tuple เช่น ['R...', '.K..'])

    เงื่อนไขความถูกต้องที่ตรวจสอบ:
    1. กระดานต้องไม่ว่างเปล่า
    2. กระดานต้องเป็นสี่เหลี่ยมจัตุรัส (N แถว x N คอลัมน์)
    3. ต้องมี King ('K') อยู่บนกระดานเพียงตัวเดียวเท่านั้น

    คืนค่า:
        (rows, king_pos) หากกระดานถูกต้อง, หรือ (None, None) หากกระดานไม่ถูกต้อง
    """
    if isinstance(board_input, str):
        rows = board_input.strip("\r\n").splitlines()
    elif isinstance(board_input, (list, tuple)):
        rows = list(board_input)
    else:
        return None, None

    if not rows:
        return None, None

    size = len(rows)
    king_pos = None

    for r, row in enumerate(rows):
        # ทุกแถวต้องเป็น string และมีความยาวเท่ากับขนาดของกระดาน (สี่เหลี่ยมจัตุรัส N x N)
        if not isinstance(row, str) or len(row) != size:
            return None, None

        for c, piece in enumerate(row):
            if piece == 'K':
                if king_pos is not None:
                    # หากพบ King มากกว่า 1 ตัว ถือว่ากระดานไม่ถูกต้อง
                    return None, None
                king_pos = (r, c)

    # ต้องพบ King อย่างน้อยและแน่นอน 1 ตัว
    if king_pos is None:
        return None, None

    return rows, king_pos


def is_king_in_check(rows, king_pos):
    """
    ตรวจสอบว่า King ณ ตำแหน่ง king_pos กำลังถูกหมากของศัตรูโจมตีหรือไม่

    ประเภทของหมากและกฎการกิน:
    - 'P' (Pawn):   กินทแยงขึ้นด้านบน 1 ช่อง (row - 1)
    - 'R' (Rook):   กินแนวตรง (แนวนอน/แนวตั้ง) ได้ทุกระยะ (ถูกขวางได้)
    - 'B' (Bishop): กินแนวทแยงได้ทุกระยะ (ถูกขวางได้)
    - 'Q' (Queen):  กินได้ทั้งแนวตรงและแนวทแยงทุกระยะ (ถูกขวางได้)

    หมากแต่ละตัวสามารถกินได้เฉพาะหมาก "ตัวแรก" ที่ขวางเส้นทางเดินเท่านั้น (มีหมากบังได้)
    ตัวอักษรอื่น ๆ ทั้งหมดที่ไม่ใช่ 'P', 'B', 'R', 'Q', 'K' จะถือว่าเป็นช่องว่าง

    คืนค่า:
        True หาก King ถูกโจมตี (In Check), False หากปลอดภัย
    """
    size = len(rows)
    kr, kc = king_pos

    # 1. ตรวจสอบเบี้ย ('P')
    # เบี้ยจะเดิน/โจมตีขึ้นด้านบน ดังนั้นเฉพาะ Pawn ที่อยู่ที่ (kr + 1, kc - 1)
    # หรือ (kr + 1, kc + 1) เท่านั้น ที่จะสามารถโจมตี King ที่ (kr, kc) ได้
    pawn_attack_positions = [
        (kr + 1, kc - 1),
        (kr + 1, kc + 1)
    ]
    for r, c in pawn_attack_positions:
        if 0 <= r < size and 0 <= c < size:
            if rows[r][c] == 'P':
                return True

    # 2. ตรวจสอบแนวตรง 4 ทิศทาง (Orthogonal) สำหรับ Rook ('R') หรือ Queen ('Q')
    # ทิศทาง: ขึ้น (-1, 0), ลง (1, 0), ซ้าย (0, -1), ขวา (0, 1)
    straight_directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dr, dc in straight_directions:
        r, c = kr + dr, kc + dc
        while 0 <= r < size and 0 <= c < size:
            cell = rows[r][c]
            # หากเจอหมากตัวใดก็ตาม จะขวางเส้นสายตา (Line of sight)
            if cell in 'PBRQK':
                if cell in ('R', 'Q'):
                    return True  # โดน Rook หรือ Queen โจมตี
                break  # ถูกหมากตัวอื่นบังทางเดิน หยุดค้นหาทิศทางนี้
            r += dr
            c += dc

    # 3. ตรวจสอบแนวทแยง 4 ทิศทาง (Diagonal) สำหรับ Bishop ('B') หรือ Queen ('Q')
    # ทิศทาง: ซ้ายบน (-1, -1), ขวาบน (-1, 1), ซ้ายล่าง (1, -1), ขวาล่าง (1, 1)
    diagonal_directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    for dr, dc in diagonal_directions:
        r, c = kr + dr, kc + dc
        while 0 <= r < size and 0 <= c < size:
            cell = rows[r][c]
            # หากเจอหมากตัวใดก็ตาม จะขวางเส้นสายตา (Line of sight)
            if cell in 'PBRQK':
                if cell in ('B', 'Q'):
                    return True  # โดน Bishop หรือ Queen โจมตี
                break  # ถูกหมากตัวอื่นบังทางเดิน หยุดค้นหาทิศทางนี้
            r += dr
            c += dc

    return False


def checkmate(board, *extra_rows):
    """
    ฟังก์ชันหลักตามที่โจทย์กำหนด เพื่อประเมินว่า King กำลังถูกโจมตีหรือไม่

    อาร์กิวเมนต์:
    - board: ข้อความหลายบรรทัด, รายการของข้อความแถว, หรือข้อความแถวแรก
    - *extra_rows: ข้อความแถวถัดไป (กรณีส่งเข้ามาเป็นหลายอาร์กิวเมนต์)

    การแสดงผล:
    - พิมพ์ 'Success' ตามด้วยขึ้นบรรทัดใหม่ หาก King กำลังถูกโจมตี (In Check)
    - พิมพ์ 'Fail' ตามด้วยขึ้นบรรทัดใหม่ หาก King ปลอดภัย
    - ไม่พิมพ์อะไรเลยและคืนการควบคุมทันที หากเกิดพฤติกรรมที่ไม่ระบุ / บอร์ดไม่ถูกต้อง
    """
    if extra_rows:
        board_input = [board] + list(extra_rows)
    else:
        board_input = board

    rows, king_pos = parse_and_validate_board(board_input)
    if rows is None:
        # บอร์ดไม่ถูกต้อง: ไม่พิมพ์อะไรเลยและคืนการควบคุมให้ผู้ใช้ (ตามข้อกำหนดโจทย์)
        return

    if is_king_in_check(rows, king_pos):
        print("Success")
    else:
        print("Fail")
