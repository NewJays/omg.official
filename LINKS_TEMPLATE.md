# 링크 입력 체크리스트

`assets/js/albums.js`에서 아래 서비스 id에 맞춰 URL을 넣으면 됩니다.

## 서비스 id

| 서비스 | id |
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

## 앨범 전체 링크 입력 예시

```js
albumLinks: blankLinks({
  youtubeTopic: "https://www.youtube.com/playlist?list=...",
  youtubeMusic: "https://music.youtube.com/playlist?list=...",
  apple: "https://music.apple.com/kr/album/...",
  spotify: "https://open.spotify.com/album/...",
  melon: "https://www.melon.com/album/detail.htm?albumId=...",
  genie: "https://www.genie.co.kr/detail/albumInfo?axnm=...",
  bugs: "https://music.bugs.co.kr/album/...",
  flo: "https://www.music-flo.com/detail/album/...",
  vibe: "https://vibe.naver.com/album/...",
  kakao: "https://music.kakao.com/..."
}),
```

## 곡별 링크 입력 예시

```js
track("밥먹었송", {
  youtubeTopic: "https://www.youtube.com/watch?v=...",
  youtubeMusic: "https://music.youtube.com/watch?v=...",
  apple: "https://music.apple.com/kr/song/...",
  spotify: "https://open.spotify.com/track/...",
  melon: "https://www.melon.com/song/detail.htm?songId=...",
  genie: "https://www.genie.co.kr/detail/songInfo?xgnm=...",
  bugs: "https://music.bugs.co.kr/track/...",
  flo: "https://www.music-flo.com/detail/track/...",
  vibe: "https://vibe.naver.com/track/...",
  kakao: "https://music.kakao.com/..."
})
```

## 잔소리 트랙 링크 입력칸

```js
tracks: [
  track("밥먹었송", { apple: "", spotify: "", youtubeMusic: "", youtubeTopic: "", melon: "", genie: "", bugs: "", flo: "", vibe: "", kakao: "" }),
  track("방정리송", { apple: "", spotify: "", youtubeMusic: "", youtubeTopic: "", melon: "", genie: "", bugs: "", flo: "", vibe: "", kakao: "" }),
  track("눈높이송", { apple: "", spotify: "", youtubeMusic: "", youtubeTopic: "", melon: "", genie: "", bugs: "", flo: "", vibe: "", kakao: "" }),
  track("치카송", { apple: "", spotify: "", youtubeMusic: "", youtubeTopic: "", melon: "", genie: "", bugs: "", flo: "", vibe: "", kakao: "" }),
  track("키즈카페송", { apple: "", spotify: "", youtubeMusic: "", youtubeTopic: "", melon: "", genie: "", bugs: "", flo: "", vibe: "", kakao: "" }),
  track("물놀이송", { apple: "", spotify: "", youtubeMusic: "", youtubeTopic: "", melon: "", genie: "", bugs: "", flo: "", vibe: "", kakao: "" }),
  track("수고했송", { apple: "", spotify: "", youtubeMusic: "", youtubeTopic: "", melon: "", genie: "", bugs: "", flo: "", vibe: "", kakao: "" }),
  track("자러갔숑", { apple: "", spotify: "", youtubeMusic: "", youtubeTopic: "", melon: "", genie: "", bugs: "", flo: "", vibe: "", kakao: "" })
]
```

## 오마이메리크리스마스 트랙 링크 입력칸

```js
tracks: [
  track("Oh! my 메리크리스마스", { apple: "", spotify: "", youtubeMusic: "", youtubeTopic: "", melon: "", genie: "", bugs: "", flo: "", vibe: "", kakao: "" }),
  track("눈누난나 신나는 크리스마스", { apple: "", spotify: "", youtubeMusic: "", youtubeTopic: "", melon: "", genie: "", bugs: "", flo: "", vibe: "", kakao: "" }),
  track("Oh! my 메리크리스마스 (Jazz Mix Ver.)", { apple: "", spotify: "", youtubeMusic: "", youtubeTopic: "", melon: "", genie: "", bugs: "", flo: "", vibe: "", kakao: "" }),
  track("눈누난나 신나는 크리스마스 (Jazz Mix Ver.)", { apple: "", spotify: "", youtubeMusic: "", youtubeTopic: "", melon: "", genie: "", bugs: "", flo: "", vibe: "", kakao: "" })
]
```
