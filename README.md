# Oh! My Gasrange album promo site

오마이가스레인지(Oh! My Gasrange) 앨범 홍보용 반응형 정적 웹사이트입니다. 프레임워크 없이 HTML, CSS, JavaScript만 사용하므로 GitHub Pages, Netlify, Vercel, Cafe24, 일반 웹호스팅 어디에나 그대로 올릴 수 있습니다.

## 파일 구조

```txt
index.html
assets/
  css/styles.css
  js/albums.js      ← 앨범, 곡, 음악서비스 링크, 이메일 수정은 주로 여기에서 합니다.
  js/app.js         ← 화면 렌더링/모달/애니메이션 로직
  images/
    artist.jpg
    albums/
      jansori-cover.jpg
      jansori-booklet.jpg
      merry-cover.jpg
      merry-booklet.jpg
      gil-cover.jpg
      gil-booklet.jpg
LINKS_TEMPLATE.md   ← 링크 입력용 체크리스트
```

## 1. GitHub Pages에서 사용 가능 여부

가능합니다. 이 사이트는 정적 사이트라 GitHub Pages 무료 계정의 공개 저장소에서 동작합니다.

사용 가능한 파일:

- `index.html`
- CSS 파일
- JavaScript 파일
- 이미지 파일: JPG, PNG, WebP, SVG 등
- 폴더 구조: `assets/css`, `assets/js`, `assets/images` 그대로 가능

주의할 점:

- GitHub Pages는 서버 프로그램, 데이터베이스, PHP, Node.js 서버 실행은 지원하지 않습니다.
- 이 사이트의 다이내믹한 동작은 브라우저에서 실행되는 JavaScript로 처리합니다.
- 무료 계정에서는 공개 저장소로 배포하는 것이 일반적입니다.

## 2. 이미지 교체

현재 이미지는 자리표시자입니다. 아래 파일명을 그대로 유지해서 교체하면 코드 수정 없이 바로 반영됩니다.

- 아티스트 이미지: `assets/images/artist.jpg`
- 잔소리 커버: `assets/images/albums/jansori-cover.jpg`
- 잔소리 부클렛: `assets/images/albums/jansori-booklet.jpg`
- 오마이메리크리스마스 커버: `assets/images/albums/merry-cover.jpg`
- 오마이메리크리스마스 부클렛: `assets/images/albums/merry-booklet.jpg`
- 길 커버: `assets/images/albums/gil-cover.jpg`
- 길 부클렛: `assets/images/albums/gil-booklet.jpg`

권장 이미지 크기:

- 앨범 커버: 3000×3000
- 앨범 소개 부클렛: 2000×2000
- 아티스트 이미지: 정사각형

웹 로딩을 빠르게 하려면 실제 배포 전 JPG/WebP로 압축하는 것을 권장합니다. 원본 3000px 이미지를 그대로 써도 되지만 모바일 초기 로딩이 느려질 수 있습니다.

## 3. 협업문의 이메일 수정

`assets/js/albums.js` 상단에서 아래 값을 실제 이메일로 바꾸세요.

```js
contactEmail: "your-email@example.com",
```

## 4. 앨범 전체 링크 추가

`assets/js/albums.js`의 각 앨범 객체 안에 `albumLinks`가 있습니다. 서비스별 URL을 입력하면 버튼이 자동 활성화됩니다.

```js
albumLinks: blankLinks({
  youtubeTopic: "",
  youtubeMusic: "",
  apple: "https://music.apple.com/kr/album/jansori/1828367407",
  spotify: "",
  melon: "",
  genie: "",
  bugs: "",
  flo: "",
  vibe: "",
  kakao: ""
}),
```

## 5. 곡별 링크 추가

곡별 링크는 `tracks` 배열에서 각 곡의 `links`에 넣습니다.

```js
tracks: [
  track("밥먹었송", {
    youtubeTopic: "",
    youtubeMusic: "",
    apple: "",
    spotify: "",
    melon: "",
    genie: "",
    bugs: "",
    flo: "",
    vibe: "",
    kakao: ""
  })
]
```

사용자가 서비스 아이콘을 누르면 해당 서비스의 앨범 링크와 곡별 링크가 같은 패널에 표시됩니다. 앨범 링크만 있어도 되고, 곡별 링크만 있어도 됩니다.

## 6. 서비스 id 목록

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

## 7. 새 앨범 추가

`albums` 배열에 객체 하나를 복사해서 추가하면 됩니다.

```js
{
  id: "new-album-id",
  type: "EP 3집",
  title: "새 앨범명",
  titleEn: "New Album",
  status: "upcoming", // released 또는 upcoming
  statusLabel: "발매 예정",
  releaseDate: "TBA",
  genre: "Coming Soon",
  trackCount: "TBA",
  cover: "assets/images/albums/new-cover.jpg",
  booklet: "assets/images/albums/new-booklet.jpg",
  description: "앨범 설명",
  tags: ["EP", "Coming Soon"],
  albumLinks: blankLinks(),
  tracks: []
}
```

발매 후에는 `status`를 `released`로 바꾸고 `albumLinks`, `tracks`에 링크를 채우면 됩니다.

## 8. 로컬에서 확인

폴더에서 바로 `index.html`을 열어도 됩니다. 더 안정적으로 보려면 아래처럼 로컬 서버를 실행하세요.

```bash
python3 -m http.server 8000
```

브라우저에서 `http://localhost:8000`으로 접속하면 됩니다.

## 9. GitHub Pages 배포

1. GitHub에서 새 공개 저장소를 만듭니다.
2. 이 폴더의 모든 파일과 폴더를 저장소 루트에 업로드합니다.
3. 저장소의 `Settings` → `Pages`로 이동합니다.
4. Source를 `Deploy from a branch`로 선택합니다.
5. Branch를 `main`, 폴더를 `/root`로 선택합니다.
6. 저장하면 `https://계정명.github.io/저장소명/` 주소로 공개됩니다.

사용자 사이트 형태로 쓰려면 저장소 이름을 `계정명.github.io`로 만들면 `https://계정명.github.io/` 주소를 사용할 수 있습니다.
