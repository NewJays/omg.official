# 링크·가사·뮤직비디오 입력 체크리스트 v7

`assets/js/albums.js`는 JSON 호환 형식입니다. 직접 편집해도 되고, 더 안전하게는 `tools/album_manager.py`를 실행해 GUI에서 수정할 수 있습니다.

```bash
python tools/album_manager.py
```

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

```json
"albumLinks": {
  "youtubeTopic": "https://www.youtube.com/playlist?list=...",
  "youtubeMusic": "https://music.youtube.com/playlist?list=...",
  "apple": "https://music.apple.com/kr/album/...",
  "spotify": "https://open.spotify.com/album/...",
  "melon": "https://www.melon.com/album/detail.htm?albumId=...",
  "genie": "https://www.genie.co.kr/detail/albumInfo?axnm=...",
  "bugs": "https://music.bugs.co.kr/album/...",
  "flo": "https://www.music-flo.com/detail/album/...",
  "vibe": "https://vibe.naver.com/album/...",
  "kakao": "https://music.kakao.com/..."
}
```

## 곡별 링크와 가사 입력 예시

각 음악서비스의 곡 바로가기 링크는 서비스마다 별도 URL입니다. 앨범 링크와 곡 링크도 서로 다릅니다.

```json
{
  "title": "밥먹었송",
  "lyrics": "가사 1행\n가사 2행\n\n두 번째 문단 1행",
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

## 아이콘 교체

현재 아이콘은 PNG 경로를 사용합니다.

```txt
assets/images/services/spotify.png
```

PNG, JPG, JPEG, SVG, WebP 모두 가능합니다. 같은 파일명으로 덮어쓰거나, `services[].icon` 경로를 바꾸면 됩니다.

```json
{
  "id": "spotify",
  "label": "Spotify",
  "short": "SP",
  "icon": "assets/images/services/spotify.png"
}
```

## 잔소리 트랙 체크리스트

- 밥먹었송
- 방정리송
- 눈높이송
- 치카송
- 키즈카페송
- 물놀이송
- 수고했송
- 자러갔숑

각 곡마다 아래 10개 링크 칸을 채우면 됩니다.

```txt
youtubeTopic / youtubeMusic / apple / spotify / melon / genie / bugs / flo / vibe / kakao
```

## 오마이메리크리스마스 트랙 체크리스트

- Oh! my 메리크리스마스
- 눈누난나 신나는 크리스마스
- Oh! my 메리크리스마스 (Jazz Mix Ver.)
- 눈누난나 신나는 크리스마스 (Jazz Mix Ver.)

각 곡마다 아래 10개 링크 칸을 채우면 됩니다.

```txt
youtubeTopic / youtubeMusic / apple / spotify / melon / genie / bugs / flo / vibe / kakao
```


## 곡별 뮤직비디오 URL 입력 예시

`links`는 곡 듣기 URL이고, `videoLinks`는 뮤직비디오 URL입니다.  
플랫폼마다 뮤직비디오 주소가 다르면 아래처럼 서비스 id별로 각각 입력합니다.

```json
{
  "title": "곡 제목",
  "lyrics": "가사 입력",
  "links": {
    "youtubeMusic": "https://music.youtube.com/watch?v=...",
    "apple": "https://music.apple.com/kr/song/...",
    "spotify": "https://open.spotify.com/track/..."
  },
  "videoLinks": {
    "youtubeMusic": "https://music.youtube.com/watch?v=MV_ID",
    "youtubeTopic": "https://www.youtube.com/watch?v=MV_ID",
    "apple": "",
    "spotify": "",
    "melon": "",
    "genie": "",
    "bugs": "",
    "flo": "",
    "vibe": "",
    "kakao": ""
  }
}
```

GUI에서는 `곡 링크/가사/MV` 탭의 `곡별 뮤직비디오 URL` 영역에 입력하면 됩니다.


## 곡별 뮤직비디오 URL

`links`는 곡 듣기 URL이고, `videoLinks`는 뮤직비디오 URL입니다.

```json
"videoLinks": {
  "youtubeTopic": "",
  "youtubeMusic": "",
  "apple": "",
  "spotify": "",
  "melon": "",
  "genie": "",
  "bugs": "",
  "flo": "",
  "vibe": ""
}
```
