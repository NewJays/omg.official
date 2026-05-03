# album_manager.py

`assets/js/albums.js`를 안전하게 편집하는 Python GUI 프로그램입니다.

## 실행

프로젝트 루트에서:

```bash
python tools/album_manager.py
```

macOS/Linux에서 필요하면:

```bash
python3 tools/album_manager.py
```

## 기능

- 협업문의 이메일 수정
- 프로젝트 이미지 수정
- 음악서비스 이름과 아이콘 경로 수정
- 앨범 추가/삭제/복제/순서 변경
- 앨범 전체 링크 입력
- 곡 추가/삭제/순서 변경
- 곡별 음악서비스 링크 입력
- 곡별 가사 입력
- JSON 내보내기/가져오기

저장할 때 기존 `assets/js/albums.js`의 백업 파일도 생성됩니다.
