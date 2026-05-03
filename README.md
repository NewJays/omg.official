# Oh! My Gasrange album promo site v4

오마이가스레인지(Oh! My Gasrange) 앨범 홍보용 반응형 정적 웹사이트입니다. 프레임워크 없이 HTML, CSS, JavaScript만 사용하므로 GitHub Pages, Netlify, Vercel, Cafe24, 일반 웹호스팅 어디에나 그대로 올릴 수 있습니다.

## 파일 구조

```txt
index.html
assets/
  css/styles.css
  js/albums.js          ← 프로젝트 정보, 앨범, 곡, 가사, 음악서비스 링크, 아이콘 경로
  js/app.js             ← 화면 렌더링/링크 패널/가사 모달/애니메이션 로직
  fonts/                ← 업로드 폰트용 폴더. OMG-Round.woff2 파일을 넣으면 자동 적용
  images/
    project.jpg         ← 프로젝트 이미지
    services/           ← 음악서비스 PNG 아이콘. PNG/JPG/SVG/WebP 등으로 교체 가능
    albums/
      jansori-cover.jpg
      jansori-booklet.jpg
      merry-cover.jpg
      merry-booklet.jpg
      gil-cover.jpg
      gil-booklet.jpg
tools/
  album_manager.py      ← albums.js를 편집하는 Python GUI 프로그램
LINKS_TEMPLATE.md       ← 링크/가사 입력 예시
```

## 1. GitHub Pages에서 사용 가능 여부

가능합니다. 이 사이트는 정적 사이트라 GitHub Pages 무료 계정의 공개 저장소에서 동작합니다.

사용 가능한 파일:

- `index.html`
- CSS 파일
- JavaScript 파일
- 이미지 파일: JPG, PNG, WebP, SVG 등
- Python 편집기 파일: 배포에는 필요 없지만 저장소에 함께 둘 수 있습니다. 브라우저에서 실행되는 것은 아니고, 내 컴퓨터에서 실행해 `albums.js`를 수정하는 도구입니다.

주의할 점:

- GitHub Pages는 서버 프로그램, 데이터베이스, PHP, Node.js 서버 실행은 지원하지 않습니다.
- 이 사이트의 다이내믹한 동작은 브라우저에서 실행되는 JavaScript로 처리합니다.
- `tools/album_manager.py`는 GitHub Pages 서버에서 실행되는 프로그램이 아니라 로컬 PC에서 실행하는 관리 도구입니다.

## 2. 이미지 교체

아래 파일명을 그대로 유지해서 교체하면 코드 수정 없이 바로 반영됩니다.

- 프로젝트 이미지: `assets/images/project.jpg`
- 잔소리 커버: `assets/images/albums/jansori-cover.jpg`
- 잔소리 부클렛: `assets/images/albums/jansori-booklet.jpg`
- 오마이메리크리스마스 커버: `assets/images/albums/merry-cover.jpg`
- 오마이메리크리스마스 부클렛: `assets/images/albums/merry-booklet.jpg`
- 길 커버: `assets/images/albums/gil-cover.jpg`
- 길 부클렛: `assets/images/albums/gil-booklet.jpg`

권장 이미지 크기:

- 앨범 커버: 3000×3000
- 앨범 소개 부클렛: 2000×2000
- 프로젝트 이미지: 정사각형

웹 로딩을 빠르게 하려면 실제 배포 전 JPG/WebP로 압축하는 것을 권장합니다.

## 3. 음악서비스 아이콘을 PNG/JPG로 교체하기

가능합니다. 현재 기본 경로는 PNG입니다.

```txt
assets/images/services/youtube-topic.png
assets/images/services/youtube-music.png
assets/images/services/apple-music.png
assets/images/services/spotify.png
assets/images/services/melon.png
assets/images/services/genie.png
assets/images/services/bugs.png
assets/images/services/flo.png
assets/images/services/vibe.png
assets/images/services/kakao-music.png
```

같은 파일명으로 PNG 또는 JPG를 덮어쓰면 바로 바뀝니다. 파일명이 다르다면 `assets/js/albums.js`의 `services[].icon` 경로만 바꾸면 됩니다.

```json
{
  "id": "spotify",
  "label": "Spotify",
  "short": "SP",
  "icon": "assets/images/services/spotify.png"
}
```

## 4. 협업문의 이메일

현재 협업문의 이메일은 아래 값입니다.

```json
"contactEmail": "omg.official@byul.me"
```

화면 하단의 `mailto:` 링크도 이 값으로 자동 갱신됩니다.

## 5. 둥근 한글 폰트 적용

GitHub Pages에서도 WOFF2 같은 웹폰트 파일을 직접 호스팅할 수 있습니다.

적용 방법:

1. 사용권이 확인된 한글 폰트 파일을 WOFF2 형식으로 준비합니다.
2. 파일명을 `OMG-Round.woff2`로 바꿉니다.
3. `assets/fonts/OMG-Round.woff2` 위치에 업로드합니다.
4. 별도 코드 수정 없이 `assets/css/styles.css` 상단의 `@font-face`가 해당 폰트를 불러옵니다.

폰트 파일이 없을 때는 `Pretendard`, `SUIT`, `NanumSquareRound`, `Apple SD Gothic Neo`, `Noto Sans KR` 순서로 대체됩니다.

## 6. Python GUI 편집기 사용법

Python 3가 설치되어 있다면 아래 명령으로 실행합니다.

```bash
python tools/album_manager.py
```

macOS/Linux에서 `python` 명령이 Python 2를 가리키면 다음처럼 실행합니다.

```bash
python3 tools/album_manager.py
```

편집기에서 할 수 있는 일:

- 협업문의 이메일 수정
- 프로젝트 이미지 경로 수정
- 앨범 추가/삭제
- 앨범 커버/부클렛 경로 수정
- 앨범별 서비스 링크 입력
- 곡 추가/삭제/순서 변경
- 곡별 가사 입력
- 곡별 음악서비스 바로가기 링크 입력
- 음악서비스 아이콘 경로 수정
- JSON 내보내기/가져오기

수정 후 반드시 상단의 **저장** 버튼을 눌러야 `assets/js/albums.js`에 반영됩니다.

## 7. 앨범 전체 링크 구조

`assets/js/albums.js`의 각 앨범 객체 안에 `albumLinks`가 있습니다. 서비스별 URL을 입력하면 버튼이 자동 활성화됩니다.

```json
"albumLinks": {
  "youtubeTopic": "",
  "youtubeMusic": "",
  "apple": "https://music.apple.com/kr/album/jansori/1828367407",
  "spotify": "",
  "melon": "",
  "genie": "",
  "bugs": "",
  "flo": "",
  "vibe": "",
  "kakao": ""
}
```

## 8. 곡별 링크와 가사 구조

각 곡은 `tracks` 배열에 들어갑니다. 곡별 링크는 서비스마다 다르게 넣어야 합니다. 예를 들어 Spotify의 곡 링크와 Apple Music의 곡 링크는 서로 다른 URL입니다.

```json
{
  "title": "밥먹었송",
  "lyrics": "1절 가사\n2절 가사",
  "links": {
    "youtubeTopic": "https://www.youtube.com/watch?v=...",
    "youtubeMusic": "https://music.youtube.com/watch?v=...",
    "apple": "https://music.apple.com/kr/song/...",
    "spotify": "https://open.spotify.com/track/...",
    "melon": "https://www.melon.com/song/detail.htm?songId=...",
    "genie": "https://www.genie.co.kr/detail/songInfo?xgnm=...",
    "bugs": "https://music.bugs.co.kr/track/...",
    "flo": "https://www.music-flo.com/detail/track/...",
    "vibe": "https://vibe.naver.com/track/...",
    "kakao": "https://music.kakao.com/..."
  }
}
```

사용자가 서비스 아이콘을 누르면 해당 서비스의 앨범 링크와 모든 곡별 링크가 같은 패널에 표시됩니다. 링크가 비어 있는 곡은 “준비 중”으로 표시되고, 가사는 `가사보기` 버튼으로 따로 열립니다.

## 9. 서비스 id

| 서비스 | 코드에서 쓰는 id |
|---|---|
| YouTube 주제채널 | `youtubeTopic` |
| YouTube Music | `youtubeMusic` |
| Apple Music | `apple` |
| Spotify | `spotify` |
| Melon | `melon` |
| Genie Music | `genie` |
| Bugs | `bugs` |
| FLO | `flo` |
| Naver VIBE | `vibe` |
| KakaoMusic | `kakao` |

## 10. 새 앨범 추가

가장 쉬운 방법은 `tools/album_manager.py`에서 **앨범 추가**를 누르는 것입니다.

직접 수정하려면 `assets/js/albums.js`의 `albums` 배열에 앨범 객체를 추가합니다. `albums.js`는 JSON 호환 형식이므로 큰따옴표와 쉼표 규칙을 지켜야 합니다.

## 11. 로컬에서 확인

폴더에서 바로 `index.html`을 열어도 됩니다. 더 안정적으로 보려면 아래처럼 로컬 서버를 실행하세요.

```bash
python3 -m http.server 8000
```

브라우저에서 `http://localhost:8000`으로 접속하면 됩니다.

## 12. GitHub Pages 배포

1. GitHub에서 새 공개 저장소를 만듭니다.
2. 이 폴더의 모든 파일과 폴더를 저장소 루트에 업로드합니다.
3. 저장소의 `Settings` → `Pages`로 이동합니다.
4. Source를 `Deploy from a branch`로 선택합니다.
5. Branch를 `main`, 폴더를 `/root`로 선택합니다.
6. 저장하면 `https://계정명.github.io/저장소명/` 주소로 공개됩니다.

사용자 사이트 형태로 쓰려면 저장소 이름을 `계정명.github.io`로 만들면 `https://계정명.github.io/` 주소를 사용할 수 있습니다.
