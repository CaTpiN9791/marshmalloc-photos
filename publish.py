# site/ (비공개 저장소) 를 올리고 공개 저장소의 Pages 배포를 돌린다.
#  - 사진은 매번 번호가 바뀌어 거의 전부 새 파일이 되므로, 기록을 쌓지 않고 커밋 하나로 덮어쓴다 (저장소 용량 유지)
#  - GitHub 토큰은 git credential 에서 꺼내 쓰고 어디에도 저장·출력하지 않는다
import json, os, subprocess, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, "site")
PUBLIC = "CaTpiN9791/marshmalloc-photos"

def git(*a):
    subprocess.run(["git", "-C", SITE, *a], check=True)

def token():
    out = subprocess.run(["git", "credential", "fill"], input="protocol=https\nhost=github.com\n\n",
                         capture_output=True, text=True).stdout
    for l in out.splitlines():
        if l.startswith("password="):
            return l[9:]
    sys.exit("GitHub 로그인 정보를 찾지 못함 (git credential)")

def main():
    git("checkout", "-q", "--orphan", "publish-tmp")
    git("add", "-A")
    git("commit", "-q", "-m", "사진")
    git("branch", "-q", "-M", "main")
    git("push", "-q", "-f", "origin", "main")
    git("reflog", "expire", "--expire=now", "--all")   # 지난 사진 묶음을 내 디스크에서도 지움
    git("gc", "-q", "--prune=now")
    req = urllib.request.Request(f"https://api.github.com/repos/{PUBLIC}/actions/workflows/pages.yml/dispatches",
                                 method="POST", data=json.dumps({"ref": "main"}).encode(),
                                 headers={"Authorization": "Bearer " + token(), "Accept": "application/vnd.github+json",
                                          "User-Agent": "marshmalloc-photos"})
    urllib.request.urlopen(req).close()
    print(f"올림. 배포 진행: https://github.com/{PUBLIC}/actions (1~2분)")

if __name__ == "__main__":
    main()
