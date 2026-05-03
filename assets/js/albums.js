/*
  오마이가스레인지 앨범 데이터 파일 v3

  이 파일만 수정해도 사이트의 앨범 카드, 음악서비스 버튼, 앨범 링크, 곡별 링크가 자동 갱신됩니다.

  링크 입력 위치
  - 앨범 전체 링크: 각 앨범 객체의 albumLinks
  - 곡별 링크: 각 앨범 객체의 tracks 안 links

  서비스 id
  - youtubeTopic : YouTube 주제채널 또는 YouTube Topic 영상/플레이리스트
  - youtubeMusic : YouTube Music 앨범/곡
  - apple        : Apple Music
  - spotify      : Spotify
  - melon        : Melon
  - genie        : Genie Music
  - bugs         : Bugs
  - flo          : FLO
  - vibe         : Naver VIBE
  - kakao        : KakaoMusic

  새 앨범 추가
  - albums 배열에 앨범 객체 하나를 복사해 추가하면 됩니다.
  - 발매 전 앨범은 status: "upcoming", 발매 후는 status: "released"를 사용하세요.
*/
(function () {
  function blankLinks(overrides) {
    var links = {
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
    };

    if (overrides) {
      for (var key in overrides) {
        if (Object.prototype.hasOwnProperty.call(overrides, key)) {
          links[key] = overrides[key];
        }
      }
    }

    return links;
  }

  function track(title, links) {
    return {
      title: title,
      links: blankLinks(links)
    };
  }

  window.OHMYGASRANGE_SITE = {
    contactEmail: "omg.official@byul.me",
    project: {
      nameKo: "오마이가스레인지",
      nameEn: "Oh! My Gasrange",
      image: "assets/images/project.jpg"
    },
    services: [
      { id: "youtubeTopic", label: "YouTube Topic", short: "YT", icon: "assets/images/services/youtube-topic.svg" },
      { id: "youtubeMusic", label: "YouTube Music", short: "YM", icon: "assets/images/services/youtube-music.svg" },
      { id: "apple", label: "Apple Music", short: "AM", icon: "assets/images/services/apple-music.svg" },
      { id: "spotify", label: "Spotify", short: "SP", icon: "assets/images/services/spotify.svg" },
      { id: "melon", label: "Melon", short: "ML", icon: "assets/images/services/melon.svg" },
      { id: "genie", label: "Genie Music", short: "GN", icon: "assets/images/services/genie.svg" },
      { id: "bugs", label: "Bugs", short: "BG", icon: "assets/images/services/bugs.svg" },
      { id: "flo", label: "FLO", short: "FL", icon: "assets/images/services/flo.svg" },
      { id: "vibe", label: "Naver VIBE", short: "VB", icon: "assets/images/services/vibe.svg" },
      { id: "kakao", label: "KakaoMusic", short: "KK", icon: "assets/images/services/kakao-music.svg" }
    ],
    albums: [
      {
        id: "jansori",
        type: "정규 1집",
        title: "잔소리",
        titleEn: "Jansori",
        status: "released",
        statusLabel: "발매 완료",
        releaseDate: "2025.07.27",
        genre: "일렉트로니카",
        trackCount: "8곡",
        cover: "assets/images/albums/jansori-cover.jpg",
        booklet: "assets/images/albums/jansori-booklet.jpg",
        description: "오마이가스레인지의 정규 1집. 유쾌한 생활감, 반복되는 말맛, 전자음악의 밝은 에너지를 어두운 네온 비주얼로 대비시킨 앨범 카드입니다.",
        tags: ["Regular Album", "Released", "8 Tracks", "Global Streaming"],
        albumLinks: blankLinks({
          apple: "https://music.apple.com/kr/album/jansori/1828367407"
        }),
        tracks: [
          track("밥먹었송"),
          track("방정리송"),
          track("눈높이송"),
          track("치카송"),
          track("키즈카페송"),
          track("물놀이송"),
          track("수고했송"),
          track("자러갔숑")
        ]
      },
      {
        id: "merry-christmas",
        type: "EP 1집",
        title: "오마이메리크리스마스",
        titleEn: "Oh! my Merry Christmas - EP",
        status: "released",
        statusLabel: "발매 완료",
        releaseDate: "2026.01.15",
        genre: "댄스",
        trackCount: "4곡",
        cover: "assets/images/albums/merry-cover.jpg",
        booklet: "assets/images/albums/merry-booklet.jpg",
        description: "오마이가스레인지의 EP 1집. 크리스마스 무드를 다이내믹한 팝/댄스 질감으로 보여주는 시즌형 앨범 카드입니다.",
        tags: ["EP", "Released", "4 Tracks", "Holiday Mood"],
        albumLinks: blankLinks({
          apple: "https://music.apple.com/kr/album/oh-my-merry-christmas-ep/1867121511"
        }),
        tracks: [
          track("Oh! my 메리크리스마스"),
          track("눈누난나 신나는 크리스마스"),
          track("Oh! my 메리크리스마스 (Jazz Mix Ver.)"),
          track("눈누난나 신나는 크리스마스 (Jazz Mix Ver.)")
        ]
      },
      {
        id: "gil",
        type: "EP 2집",
        title: "길",
        titleEn: "Gil",
        status: "upcoming",
        statusLabel: "발매 예정",
        releaseDate: "TBA",
        genre: "Coming Soon",
        trackCount: "TBA",
        cover: "assets/images/albums/gil-cover.jpg",
        booklet: "assets/images/albums/gil-booklet.jpg",
        description: "발매 예정 EP 2집. 발매일, 플랫폼 링크, 곡별 링크가 확정되면 이 데이터 파일에 URL만 넣어 사이트를 갱신할 수 있습니다.",
        tags: ["EP", "Coming Soon", "길", "To Be Announced"],
        albumLinks: blankLinks(),
        tracks: []
      }
    ]
  };
})();
