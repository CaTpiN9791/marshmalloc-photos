# marshmalloc-photos

Marshmalloc 월드 사진 키오스크가 읽는 사진.

1. `photos/` 에 사진(VRChat 스크린샷)을 넣는다 (git 에는 안 올라감)
2. `python build.py` → `site/` 가 만들어짐 (최신순, FHD JPG 95 + 출력용 768 + 썸네일 판)
3. `git add site && git commit -m "사진" && git push` → Actions 가 Pages 로 배포

주소: https://catpin9791.github.io/marshmalloc-photos/index.json
사진은 공개 주소로 올라가므로 남에게 보여도 되는 사진만 넣을 것.
