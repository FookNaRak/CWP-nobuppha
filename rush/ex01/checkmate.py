"""
Rush00 Bonus - ตรวจสอบสถานะการถูกโจมตีของ King (Checkmate Detection)
โมดูล: checkmate.py (ex01)

ประกอบด้วยฟังก์ชันตรวจสอบความถูกต้องของกระดาน ประเมินสถานะการถูกโจมตีของ King
และฟังก์ชันแสดงผลกระดานพร้อมคำอธิบายแบบละเอียด (Visual Explanation)
"""


def parse_and_validate_board(board_input):
    """
    แยกบรรทัดและตรวจสอบความถูกต้องของกระดานหมากรุก

    เงื่อนไขความถูกต้องที่ตรวจสอบ:
    1. อินพุตต้องเป็น string หรือ list/tuple ของข้อความแต่ละแถว
    2. กระดานต้องไม่ว่างเปล่า
    3. กระดานต้องเป็นสี่เหลี่ยมจัตุรัส (N แถว x N คอลัมน์)
    4. ต้องมี King ('K') อยู่บนกระดานเพียงตัวเดียวเท่านั้น

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
        if not isinstance(row, str) or len(row) != size:
            return None, None

        for c, piece in enumerate(row):
            if piece == 'K':
                if king_pos is not None:
                    # หากพบ King มากกว่า 1 ตัว ถือว่ากระดานไม่ถูกต้อง
                    return None, None
                king_pos = (r, c)

    # ต้องพบ King อย่างแน่นอน 1 ตัว
    if king_pos is None:
        return None, None

    return rows, king_pos


def find_threats(rows, king_pos):
    """
    ค้นหาหมากศัตรูทั้งหมดที่กำลังโจมตี King อยู่ในขณะนั้น

    คืนค่า:
        รายการของ tuple: (ตัวอักษรหมาก, (แถว, คอลัมน์), คำอธิบายรูปแบบการโจมตี)
    """
    size = len(rows)
    kr, kc = king_pos
    threats = []

    # 1. ตรวจสอบเบี้ย ('P')
    pawn_attack_positions = [
        (kr + 1, kc - 1),
        (kr + 1, kc + 1)
    ]
    for r, c in pawn_attack_positions:
        if 0 <= r < size and 0 <= c < size:
            if rows[r][c] == 'P':
                threats.append(('P', (r, c), "กินทแยงขึ้นด้านบน (Pawn attack)"))

    # 2. ตรวจสอบแนวตรง 4 ทิศทาง สำหรับ Rook ('R') หรือ Queen ('Q')
    straight_directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dr, dc in straight_directions:
        r, c = kr + dr, kc + dc
        while 0 <= r < size and 0 <= c < size:
            cell = rows[r][c]
            if cell in 'PBRQK':
                if cell in ('R', 'Q'):
                    threats.append((cell, (r, c), "โจมตีแนวตรง (Straight line)"))
                break  # ถูกหมากตัวอื่นบังทางเดิน
            r += dr
            c += dc

    # 3. ตรวจสอบแนวทแยง 4 ทิศทาง สำหรับ Bishop ('B') หรือ Queen ('Q')
    diagonal_directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    for dr, dc in diagonal_directions:
        r, c = kr + dr, kc + dc
        while 0 <= r < size and 0 <= c < size:
            cell = rows[r][c]
            if cell in 'PBRQK':
                if cell in ('B', 'Q'):
                    threats.append((cell, (r, c), "โจมตีแนวทแยง (Diagonal)"))
                break  # ถูกหมากตัวอื่นบังทางเดิน
            r += dr
            c += dc

    return threats


def evaluate_board(board_content):
    """
    ประเมินข้อความกระดานหมากรุกและส่งคืนผลลัพธ์:
    - 'Success': กระดานถูกต้อง และ King กำลังถูกโจมตี (In Check)
    - 'Fail':    กระดานถูกต้อง และ King ปลอดภัย (ไม่อยู่ใน Check)
    - 'Error':   กระดานไม่ถูกต้อง (ไม่เป็นสี่เหลี่ยมจัตุรัส, ไม่มี King หรือมีมากกว่า 1 ตัว)
    """
    rows, king_pos = parse_and_validate_board(board_content)
    if rows is None:
        return "Error"

    threats = find_threats(rows, king_pos)
    if threats:
        return "Success"
    return "Fail"


def visual_explain(board_content):
    """
    ฟังก์ชันเสริมโบนัสสร้างสรรค์ (Creative Bonus Feature):
    แสดงผลแผนผังกระดานหมากรุกพร้อมระบุตำแหน่ง King และหมากศัตรูที่กำลังโจมตี
    """
    rows, king_pos = parse_and_validate_board(board_content)
    if rows is None:
        return "Error: รูปแบบกระดานไม่ถูกต้อง (ต้องเป็นสี่เหลี่ยมจัตุรัสและมี King เพียง 1 ตัว)"

    size = len(rows)
    kr, kc = king_pos
    threats = find_threats(rows, king_pos)

    threat_coords = {pos for _, pos, _ in threats}

    output = []
    output.append(f"ขนาดกระดาน: {size}x{size}")
    output.append(f"ตำแหน่ง King: แถว {kr}, คอลัมน์ {kc}")
    output.append("   " + " ".join(f"{c}" for c in range(size)))
    output.append("  +" + "--" * size + "+")

    for r in range(size):
        row_str = []
        for c in range(size):
            cell = rows[r][c]
            if (r, c) == (kr, kc):
                row_str.append("[K]")
            elif (r, c) in threat_coords:
                row_str.append(f"*{cell}*")
            else:
                row_str.append(f" {cell} ")
        output.append(f"{r} |{''.join(row_str)}|")

    output.append("  +" + "--" * size + "+")

    if threats:
        output.append(f"สถานะ: SUCCESS (King กำลังถูกโจมตี!)")
        output.append(f"พบหมากที่โจมตี ({len(threats)} ตัว):")
        for piece, (pr, pc), attack_type in threats:
            output.append(f"  - หมาก '{piece}' ที่พิกัด ({pr}, {pc}) ด้วยรูปแบบ {attack_type}")
    else:
        output.append("สถานะ: FAIL (King ปลอดภัย / ไม่อยู่ใน Check)")

    return "\n".join(output)
