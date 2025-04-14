from gtts import gTTS
from pydub import AudioSegment
import os
import re
import time
from tqdm import tqdm

file_path = "source.md"
output_dir = "tts_outputs"
final_output = "final_output.mp3"


def generate_tts():
    start = time.time()

    os.makedirs(output_dir, exist_ok=True)

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    sections = re.split(r'# (W\d+)', content)
    sections = list(zip(sections[1::2], sections[2::2]))

    print(f"[INFO] 총 {len(sections)}개의 섹션 발견\n")

    for section_name, section_content in sections:
        print(f"[Progress] {section_name}.mp3 생성중...")
        qnas = re.findall(r'\d+\.\s(.+?)\n\s*<aside>\s*(.*?)\s*</aside>', section_content, re.DOTALL)

        if not qnas:
            print(f"[Skip] {section_name} 섹션에 질문-답변 없음. 건너뜀.\n")
            continue

        combined_text = ''
        for i, (q, a) in enumerate(qnas, 1):
            # 영어 비율 확인
            english_chars = re.findall(r'[a-zA-Z]', a)
            total_chars = len(a.strip())
            english_ratio = len(english_chars) / total_chars if total_chars > 0 else 0

            if english_ratio < 0.3:
                print(f"[Skip] Q{i} 답변에 영어 비율 낮음 → 건너뜀")
                continue

            combined_text += f'Question {i}: {q.strip()} Answer: {a.strip()}.\n'

        if not combined_text.strip():
            print(f"[Skip] {section_name} 섹션 내 영어 답변 없음. 건너뜀.\n")
            continue

        for _ in tqdm(range(100)):
            time.sleep(0.01)

        tts = gTTS(text=combined_text, lang='en')
        tts.save(os.path.join(output_dir, f'{section_name}.mp3'))
        print(f"[Success] {section_name}.mp3 저장완료\n")

    end = time.time()
    print(f"[FINISH] 모든 mp3 파일 생성 완료! 총 소요시간: {int(end - start)}초")


def merge_mp3():
    print(f"[INFO] {output_dir} 내 mp3 파일을 하나로 합치는 중...")

    files = sorted([f for f in os.listdir(output_dir) if f.endswith('.mp3')])

    if not files:
        print("[ERROR] mp3 파일이 없습니다.")
        return

    combined = AudioSegment.empty()

    for f in files:
        print(f"[Add] {f} 추가중...")
        combined += AudioSegment.from_mp3(os.path.join(output_dir, f))

    combined.export(final_output, format='mp3')
    print(f"[Success] {final_output} 파일 생성 완료!")


if __name__ == "__main__":
    print("작업을 선택하세요:")
    print("1. source.md → mp3 파일들 생성")
    print("2. tts_outputs/ → mp3 파일 하나로 합치기")
    choice = input("입력: ")

    if choice == "1":
        generate_tts()
    elif choice == "2":
        merge_mp3()
    else:
        print("잘못된 입력입니다.")
