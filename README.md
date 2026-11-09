# marshmalloc-photos

Marshmalloc 월드 사진 키오스크의 배포 절차. **사진은 이 저장소에 없다** (비공개 저장소에서 가져와 Pages 로만 배포).

1. `python build.py 목록.txt` (또는 `photos/` 폴더) → `site/<폴더>/` 생성 (최신순 2240장, FHD JPG 95 + 썸네일 판, 세로 사진은 90° 돌림)
2. `python publish.py` → 비공개 저장소에 올리고 이 저장소의 Actions 가 Pages 로 배포

- `site/` 는 비공개 저장소 `marshmalloc-photos-src` 의 작업 폴더 (이 저장소에는 안 올라감)
- 배포 키는 Actions 비밀값 `SRC_DEPLOY_KEY` (비공개 저장소 읽기 전용)
- 검색엔진 수집은 `catpin9791.github.io/robots.txt` 로 막는다
- 사진 주소는 공개라서 월드에 들어온 사람은 얻을 수 있다. 남에게 보여도 되는 사진만 넣을 것
