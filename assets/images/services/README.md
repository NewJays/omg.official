# 음악서비스 아이콘 교체 안내

이 폴더의 PNG 아이콘은 교체용 자리표시자입니다. 실제 공식 로고 파일을 보유하고 있거나 사용 허가 범위가 명확하다면 같은 파일명으로 덮어쓰면 됩니다.

권장 형식:
- PNG 또는 JPG 모두 가능
- 정사각형 이미지 권장: 512×512, 1024×1024 등
- 파일명은 `assets/js/albums.js`의 `services[].icon` 경로와 맞추면 됩니다.

예: Spotify 아이콘을 JPG로 바꾸는 경우
1. `assets/images/services/spotify.jpg` 파일을 넣습니다.
2. `assets/js/albums.js`에서 Spotify 서비스의 `icon` 값을 `assets/images/services/spotify.jpg`로 바꿉니다.

Python GUI 편집기 `tools/album_manager.py`의 `서비스/아이콘` 탭에서도 아이콘 파일을 선택해 복사할 수 있습니다.
