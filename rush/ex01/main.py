"""
โปรแกรมทดสอบสำหรับ Rush00 Bonus (ex01)
รองรับการรับไฟล์กระดานหมากรุก (.chess) ผ่าน command-line arguments
"""
import sys
import os
from checkmate import evaluate_board, visual_explain


def process_file(file_path, visual_mode=False):
    """
    อ่านไฟล์ .chess และประเมินผลกระดานหมากรุก
    """
    if not os.path.isfile(file_path):
        if visual_mode:
            print(f"Error: ไม่พบไฟล์ '{file_path}'")
        else:
            print("Error")
        return

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        if visual_mode:
            print(f"Error: ไม่สามารถอ่านไฟล์ '{file_path}' ได้")
        else:
            print("Error")
        return

    if visual_mode:
        print(f"\n=== ผลการวิเคราะห์กระดาน: {file_path} ===")
        print(visual_explain(content))
    else:
        result = evaluate_board(content)
        print(result)


def main():
    args = sys.argv[1:]
    if not args:
        return

    visual_mode = False
    files = []

    for arg in args:
        if arg in ("--visual", "-v", "--explain"):
            visual_mode = True
        else:
            files.append(arg)

    for file_path in files:
        process_file(file_path, visual_mode)


if __name__ == "__main__":
    main()
