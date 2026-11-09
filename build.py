# 사진 키오스크용 사이트 만들기: photos/ 의 사진 → site/ (index.json, p_0000.jpg..., thumbs_00.jpg...)
#  - 최신순 (VRChat 스크린샷 파일 이름의 날짜, 없으면 파일 수정 시각)
#  - 크게 보기 p_0000.jpg = 1920×1080 JPG 95, 출력용 s_0000.jpg = 768×432 JPG 90 (16:9 가운데 자르기)
#  - 썸네일 256×144 를 2048×2048 판에 8열 × 14행 (판 하나 112장)
#  - 월드에는 사진 1000장, 판 10장까지 주소가 들어 있다
# 쓰는 법: python build.py            (photos/ 폴더)
#         python build.py D:\어딘가\사진폴더
import json, os, re, sys, glob, datetime
from PIL import Image, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "photos")
OUT = os.path.join(HERE, "site")
MAX_PHOTOS, PER_ATLAS, COLS, ATLAS = 1000, 112, 8, 2048
FW, FH, SW, SH, TW, TH = 1920, 1080, 768, 432, 256, 144
VRC = re.compile(r"(\d{4})-(\d{2})-(\d{2})_(\d{2})-(\d{2})-(\d{2})")

def when(path):
    m = VRC.search(os.path.basename(path))
    if m:
        return datetime.datetime(*map(int, m.groups()))
    return datetime.datetime.fromtimestamp(os.path.getmtime(path))

def fit(img, w, h):
    return ImageOps.fit(img, (w, h), Image.LANCZOS, centering=(0.5, 0.5))

def main():
    files = [p for p in glob.glob(os.path.join(SRC, "**", "*"), recursive=True)
             if p.lower().endswith((".png", ".jpg", ".jpeg", ".webp"))]
    files.sort(key=when, reverse=True)
    if len(files) > MAX_PHOTOS:
        print(f"사진이 {len(files)}장이라 최신 {MAX_PHOTOS}장만 씁니다.")
        files = files[:MAX_PHOTOS]
    os.makedirs(OUT, exist_ok=True)
    for old in glob.glob(os.path.join(OUT, "p_*.jpg")) + glob.glob(os.path.join(OUT, "s_*.jpg")) + glob.glob(os.path.join(OUT, "thumbs_*.jpg")):
        os.remove(old)
    dates, atlas, ai = [], None, -1
    for i, path in enumerate(files):
        with Image.open(path) as im:
            im = ImageOps.exif_transpose(im).convert("RGB")
            big = fit(im, FW, FH)
            big.save(os.path.join(OUT, f"p_{i:04d}.jpg"), quality=95, optimize=True, progressive=False)
            fit(big, SW, SH).save(os.path.join(OUT, f"s_{i:04d}.jpg"), quality=90, optimize=True, progressive=False)
            if i // PER_ATLAS != ai:
                if atlas is not None:
                    atlas.save(os.path.join(OUT, f"thumbs_{ai:02d}.jpg"), quality=85, optimize=True)
                ai = i // PER_ATLAS
                atlas = Image.new("RGB", (ATLAS, ATLAS), (26, 28, 32))
            c = i % PER_ATLAS
            atlas.paste(fit(im, TW, TH), ((c % COLS) * TW, (c // COLS) * TH))
        dates.append(when(path).strftime("%Y.%m.%d"))
        if (i + 1) % 50 == 0:
            print(f"{i + 1}/{len(files)}")
    if atlas is not None:
        atlas.save(os.path.join(OUT, f"thumbs_{ai:02d}.jpg"), quality=85, optimize=True)
    with open(os.path.join(OUT, "index.json"), "w", encoding="utf-8") as f:
        json.dump({"count": len(files), "dates": dates}, f, ensure_ascii=False, separators=(",", ":"))
    size = sum(os.path.getsize(p) for p in glob.glob(os.path.join(OUT, "*")))
    print(f"완료: {len(files)}장, 판 {ai + 1}장, site/ {size / 1e6:.1f}MB")

if __name__ == "__main__":
    main()
