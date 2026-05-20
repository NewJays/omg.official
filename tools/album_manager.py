#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Oh! My Gasrange 앨범 데이터 GUI 편집기

실행 위치:
  - 프로젝트 루트에서: python tools/album_manager.py
  - tools 폴더에서:  python album_manager.py

편집 대상:
  assets/js/albums.js

외부 패키지 없이 Python 표준 라이브러리 tkinter만 사용합니다.
"""
from __future__ import annotations

import copy
import datetime as _dt
import json
import os
import re
import shutil
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    import tkinter as tk
    from tkinter import filedialog, messagebox, ttk
except Exception as exc:  # pragma: no cover
    print("tkinter를 불러올 수 없습니다. Python 설치 옵션에서 Tk/Tcl을 포함해 주세요.")
    raise exc

APP_TITLE = "Oh! My Gasrange 앨범/링크/가사/MV 편집기"
ALBUMS_JS_REL = Path("assets/js/albums.js")
SERVICE_ICON_DIR_REL = Path("assets/images/services")
ALBUM_IMAGE_DIR_REL = Path("assets/images/albums")

JS_HEADER = """/*
  오마이가스레인지 앨범 데이터 파일 v4.1

  이 파일은 JSON 형태의 JavaScript 데이터입니다.
  - 웹사이트는 이 파일을 그대로 읽습니다.
  - tools/album_manager.py GUI 편집기도 이 파일을 읽고 저장합니다.

  아이콘은 SVG뿐 아니라 PNG, JPG, JPEG, WEBP도 사용할 수 있습니다.
  서비스 아이콘을 교체하려면 services[].icon 경로를 바꾸거나 같은 파일명으로 덮어쓰세요.

  링크 입력 위치
  - 앨범 전체 링크: albums[].albumLinks.{serviceId}
  - 곡 바로가기 링크: albums[].tracks[].links.{serviceId}
  - 곡별 뮤직비디오 링크: albums[].tracks[].videoLinks.{serviceId}
  - 가사: albums[].tracks[].lyrics
*/
"""


def slugify(value: str, fallback: str = "item") -> str:
    text = value.strip().lower()
    text = re.sub(r"[^0-9a-z가-힣]+", "-", text)
    text = text.strip("-")
    return text or fallback


def posix_rel(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def find_site_root(start: Path) -> Path:
    cur = start.resolve()
    if cur.is_file():
        cur = cur.parent
    for candidate in [cur] + list(cur.parents):
        if (candidate / ALBUMS_JS_REL).exists():
            return candidate
    return Path.cwd().resolve()


def extract_json_object_from_js(text: str) -> str:
    marker = "window.OHMYGASRANGE_SITE"
    marker_index = text.find(marker)
    if marker_index < 0:
        raise ValueError("window.OHMYGASRANGE_SITE 할당문을 찾을 수 없습니다.")

    start = text.find("{", marker_index)
    if start < 0:
        raise ValueError("데이터 객체 시작 중괄호를 찾을 수 없습니다.")

    depth = 0
    in_string = False
    escape = False
    quote = ""

    for index in range(start, len(text)):
        char = text[index]
        if in_string:
            if escape:
                escape = False
            elif char == "\\":
                escape = True
            elif char == quote:
                in_string = False
        else:
            if char in ('"', "'"):
                in_string = True
                quote = char
            elif char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
                if depth == 0:
                    return text[start : index + 1]

    raise ValueError("데이터 객체 끝 중괄호를 찾을 수 없습니다.")


def load_data(path: Path) -> Dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    object_text = extract_json_object_from_js(text)
    data = json.loads(object_text)
    normalize_data(data)
    return data


def save_data(path: Path, data: Dict[str, Any], make_backup: bool = True) -> None:
    normalize_data(data)
    if make_backup and path.exists():
        stamp = _dt.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup = path.with_suffix(path.suffix + f".bak_{stamp}")
        shutil.copy2(path, backup)
    body = json.dumps(data, ensure_ascii=False, indent=2)
    path.write_text(JS_HEADER + "window.OHMYGASRANGE_SITE = " + body + ";\n", encoding="utf-8")


def service_ids(data: Dict[str, Any]) -> List[str]:
    return [service.get("id", "") for service in data.get("services", []) if service.get("id")]


def blank_links(ids: List[str]) -> Dict[str, str]:
    return {sid: "" for sid in ids}


def normalize_links(links: Any, ids: List[str]) -> Dict[str, str]:
    normalized = blank_links(ids)
    if isinstance(links, dict):
        for sid in ids:
            value = links.get(sid, "")
            normalized[sid] = value if isinstance(value, str) else str(value)
    return normalized


def normalize_data(data: Dict[str, Any]) -> None:
    data.setdefault("version", "4.1.0")
    data.setdefault("contactEmail", "omg.official@byul.me")
    data.setdefault("project", {})
    data["project"].setdefault("nameKo", "오마이가스레인지")
    data["project"].setdefault("nameEn", "Oh! My Gasrange")
    data["project"].setdefault("image", "assets/images/project.jpg")
    data.setdefault("services", [])
    data.setdefault("albums", [])

    ids = service_ids(data)
    for service in data["services"]:
        service.setdefault("id", slugify(service.get("label", "service"), "service"))
        service.setdefault("label", service["id"])
        service.setdefault("short", service["label"][:2].upper())
        service.setdefault("icon", "")

    ids = service_ids(data)
    for album in data["albums"]:
        album.setdefault("id", slugify(album.get("title", "album"), "album"))
        album.setdefault("type", "Album")
        album.setdefault("title", "새 앨범")
        album.setdefault("titleEn", "")
        album.setdefault("status", "released")
        album.setdefault("statusLabel", "발매 완료" if album.get("status") == "released" else "발매 예정")
        album.setdefault("releaseDate", "TBA")
        album.setdefault("genre", "")
        album.setdefault("trackCount", "")
        album.setdefault("cover", "")
        album.setdefault("booklet", "")
        album.setdefault("description", "")
        album.setdefault("tags", [])
        if isinstance(album["tags"], str):
            album["tags"] = [tag.strip() for tag in album["tags"].split(",") if tag.strip()]
        album["albumLinks"] = normalize_links(album.get("albumLinks"), ids)
        album.setdefault("tracks", [])
        for track in album["tracks"]:
            track.setdefault("title", "새 곡")
            track.setdefault("lyrics", "")
            track["links"] = normalize_links(track.get("links"), ids)
            track["videoLinks"] = normalize_links(track.get("videoLinks"), ids)


def new_album(data: Dict[str, Any]) -> Dict[str, Any]:
    ids = service_ids(data)
    return {
        "id": "new-album",
        "type": "Album",
        "title": "새 앨범",
        "titleEn": "New Album",
        "status": "released",
        "statusLabel": "발매 완료",
        "releaseDate": "TBA",
        "genre": "",
        "trackCount": "0곡",
        "cover": "",
        "booklet": "",
        "description": "",
        "tags": [],
        "albumLinks": blank_links(ids),
        "tracks": [],
    }


def new_track(data: Dict[str, Any]) -> Dict[str, Any]:
    ids = service_ids(data)
    return {"title": "새 곡", "lyrics": "", "links": blank_links(ids), "videoLinks": blank_links(ids)}


class ScrollFrame(ttk.Frame):
    def __init__(self, master: tk.Misc, *args: Any, **kwargs: Any) -> None:
        super().__init__(master, *args, **kwargs)
        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.inner = ttk.Frame(self.canvas)
        self.inner.bind("<Configure>", self._on_configure)
        self.window_id = self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.canvas.bind("<Configure>", self._on_canvas_configure)

    def _on_configure(self, _event: tk.Event) -> None:
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event: tk.Event) -> None:
        self.canvas.itemconfigure(self.window_id, width=event.width)


class AlbumManager(tk.Tk):
    def __init__(self, site_root: Path) -> None:
        super().__init__()
        self.site_root = site_root
        self.albums_js_path = site_root / ALBUMS_JS_REL
        self.data: Dict[str, Any] = load_data(self.albums_js_path)
        self.current_album_index: Optional[int] = None
        self.current_track_index: Optional[int] = None
        self.current_service_index: Optional[int] = None
        self._loading = False

        self.title(APP_TITLE)
        self.geometry("1180x760")
        self.minsize(980, 640)
        self._build_vars()
        self._build_ui()
        self.refresh_all()
        if self.data.get("albums"):
            self.select_album(0)
        if self.data.get("services"):
            self.select_service(0)

    def _build_vars(self) -> None:
        self.site_vars = {
            "contactEmail": tk.StringVar(),
            "project.nameKo": tk.StringVar(),
            "project.nameEn": tk.StringVar(),
            "project.image": tk.StringVar(),
        }
        self.album_vars = {key: tk.StringVar() for key in [
            "id", "type", "title", "titleEn", "status", "statusLabel", "releaseDate",
            "genre", "trackCount", "cover", "booklet", "tags"
        ]}
        self.album_link_vars: Dict[str, tk.StringVar] = {}
        self.track_title_var = tk.StringVar()
        self.track_link_vars: Dict[str, tk.StringVar] = {}
        self.track_video_link_vars: Dict[str, tk.StringVar] = {}
        self.service_vars = {key: tk.StringVar() for key in ["id", "label", "short", "icon"]}

    def _build_ui(self) -> None:
        self._build_menu()
        top = ttk.Frame(self, padding=(10, 8))
        top.pack(fill="x")
        ttk.Label(top, text="프로젝트 루트:").pack(side="left")
        ttk.Label(top, text=str(self.site_root), foreground="#555").pack(side="left", padx=(6, 12))
        ttk.Button(top, text="저장", command=self.save).pack(side="right")
        ttk.Button(top, text="다시 불러오기", command=self.reload).pack(side="right", padx=(0, 8))

        paned = ttk.PanedWindow(self, orient="horizontal")
        paned.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        left = ttk.Frame(paned, padding=8)
        paned.add(left, weight=1)
        ttk.Label(left, text="앨범 목록", font=("TkDefaultFont", 11, "bold")).pack(anchor="w")
        self.album_list = tk.Listbox(left, exportselection=False, height=18)
        self.album_list.pack(fill="both", expand=True, pady=(8, 8))
        self.album_list.bind("<<ListboxSelect>>", self._on_album_select)
        album_buttons = ttk.Frame(left)
        album_buttons.pack(fill="x")
        ttk.Button(album_buttons, text="추가", command=self.add_album).grid(row=0, column=0, sticky="ew", padx=2, pady=2)
        ttk.Button(album_buttons, text="복제", command=self.duplicate_album).grid(row=0, column=1, sticky="ew", padx=2, pady=2)
        ttk.Button(album_buttons, text="삭제", command=self.delete_album).grid(row=0, column=2, sticky="ew", padx=2, pady=2)
        ttk.Button(album_buttons, text="위", command=lambda: self.move_album(-1)).grid(row=1, column=0, sticky="ew", padx=2, pady=2)
        ttk.Button(album_buttons, text="아래", command=lambda: self.move_album(1)).grid(row=1, column=1, sticky="ew", padx=2, pady=2)
        ttk.Button(album_buttons, text="ID 자동", command=self.autofill_album_id).grid(row=1, column=2, sticky="ew", padx=2, pady=2)
        for col in range(3):
            album_buttons.columnconfigure(col, weight=1)

        right = ttk.Frame(paned)
        paned.add(right, weight=4)
        self.tabs = ttk.Notebook(right)
        self.tabs.pack(fill="both", expand=True)
        self._build_site_tab()
        self._build_services_tab()
        self._build_album_tab()
        self._build_tracks_tab()

    def _build_menu(self) -> None:
        menu = tk.Menu(self)
        file_menu = tk.Menu(menu, tearoff=False)
        file_menu.add_command(label="저장", command=self.save, accelerator="Ctrl+S")
        file_menu.add_command(label="다시 불러오기", command=self.reload)
        file_menu.add_separator()
        file_menu.add_command(label="JSON 내보내기", command=self.export_json)
        file_menu.add_command(label="JSON 가져오기", command=self.import_json)
        file_menu.add_separator()
        file_menu.add_command(label="종료", command=self.destroy)
        menu.add_cascade(label="파일", menu=file_menu)
        self.config(menu=menu)
        self.bind_all("<Control-s>", lambda _event: self.save())

    def _label_entry(self, parent: ttk.Frame, row: int, label: str, var: tk.StringVar, *, width: int = 50) -> ttk.Entry:
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w", padx=(0, 8), pady=4)
        entry = ttk.Entry(parent, textvariable=var, width=width)
        entry.grid(row=row, column=1, sticky="ew", pady=4)
        parent.columnconfigure(1, weight=1)
        return entry

    def _build_site_tab(self) -> None:
        tab = ScrollFrame(self.tabs)
        self.tabs.add(tab, text="사이트")
        frame = tab.inner
        frame.columnconfigure(1, weight=1)
        self._label_entry(frame, 0, "협업문의 이메일", self.site_vars["contactEmail"])
        self._label_entry(frame, 1, "프로젝트명(한글)", self.site_vars["project.nameKo"])
        self._label_entry(frame, 2, "프로젝트명(영문)", self.site_vars["project.nameEn"])
        self._label_entry(frame, 3, "프로젝트 이미지 경로", self.site_vars["project.image"])
        ttk.Button(frame, text="프로젝트 이미지 선택/복사", command=self.choose_project_image).grid(row=3, column=2, padx=(8, 0), pady=4)
        ttk.Label(frame, text="PNG/JPG 아이콘은 서비스 탭에서 선택할 수 있습니다. 외부 파일을 고르면 프로젝트 폴더로 복사됩니다.", foreground="#555").grid(row=4, column=0, columnspan=3, sticky="w", pady=(16, 4))

    def _build_services_tab(self) -> None:
        tab = ttk.Frame(self.tabs, padding=8)
        self.tabs.add(tab, text="서비스/아이콘")
        tab.columnconfigure(1, weight=1)
        tab.rowconfigure(0, weight=1)

        left = ttk.Frame(tab)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        self.service_list = tk.Listbox(left, width=28, exportselection=False)
        self.service_list.pack(fill="both", expand=True)
        self.service_list.bind("<<ListboxSelect>>", self._on_service_select)
        service_buttons = ttk.Frame(left)
        service_buttons.pack(fill="x", pady=(8, 0))
        ttk.Button(service_buttons, text="추가", command=self.add_service).grid(row=0, column=0, sticky="ew", padx=2)
        ttk.Button(service_buttons, text="삭제", command=self.delete_service).grid(row=0, column=1, sticky="ew", padx=2)
        for col in range(2):
            service_buttons.columnconfigure(col, weight=1)

        form = ttk.Frame(tab)
        form.grid(row=0, column=1, sticky="nsew")
        form.columnconfigure(1, weight=1)
        self._label_entry(form, 0, "서비스 ID", self.service_vars["id"])
        self._label_entry(form, 1, "표시 이름", self.service_vars["label"])
        self._label_entry(form, 2, "짧은 이름", self.service_vars["short"])
        self._label_entry(form, 3, "아이콘 경로", self.service_vars["icon"])
        ttk.Button(form, text="PNG/JPG 아이콘 선택/복사", command=self.choose_service_icon).grid(row=3, column=2, padx=(8, 0), pady=4)
        ttk.Label(form, text="아이콘은 PNG/JPG/JPEG/WEBP/SVG 모두 가능하지만, 정사각형 PNG 또는 JPG를 권장합니다.", foreground="#555").grid(row=4, column=0, columnspan=3, sticky="w", pady=(12, 0))

    def _build_album_tab(self) -> None:
        tab = ScrollFrame(self.tabs)
        self.tabs.add(tab, text="앨범")
        frame = tab.inner
        frame.columnconfigure(1, weight=1)
        rows = [
            ("id", "앨범 ID"), ("type", "구분"), ("title", "앨범명"), ("titleEn", "영문명"),
            ("releaseDate", "발매일"), ("genre", "장르"), ("trackCount", "곡 수"),
            ("cover", "커버 이미지 경로"), ("booklet", "부클렛 이미지 경로"), ("tags", "태그, 쉼표 구분"),
        ]
        row = 0
        for key, label in rows[:4]:
            self._label_entry(frame, row, label, self.album_vars[key])
            row += 1
        ttk.Label(frame, text="상태").grid(row=row, column=0, sticky="w", padx=(0, 8), pady=4)
        status = ttk.Combobox(frame, textvariable=self.album_vars["status"], values=["released", "upcoming"], state="readonly")
        status.grid(row=row, column=1, sticky="ew", pady=4)
        row += 1
        self._label_entry(frame, row, "상태 표시", self.album_vars["statusLabel"])
        row += 1
        for key, label in rows[4:7]:
            self._label_entry(frame, row, label, self.album_vars[key])
            row += 1
        self._label_entry(frame, row, "커버 이미지 경로", self.album_vars["cover"])
        ttk.Button(frame, text="커버 선택/복사", command=lambda: self.choose_album_image("cover")).grid(row=row, column=2, padx=(8, 0), pady=4)
        row += 1
        self._label_entry(frame, row, "부클렛 이미지 경로", self.album_vars["booklet"])
        ttk.Button(frame, text="부클렛 선택/복사", command=lambda: self.choose_album_image("booklet")).grid(row=row, column=2, padx=(8, 0), pady=4)
        row += 1
        self._label_entry(frame, row, "태그, 쉼표 구분", self.album_vars["tags"])
        row += 1
        ttk.Label(frame, text="앨범 설명").grid(row=row, column=0, sticky="nw", padx=(0, 8), pady=4)
        self.album_description = tk.Text(frame, height=5, wrap="word")
        self.album_description.grid(row=row, column=1, columnspan=2, sticky="nsew", pady=4)
        row += 1
        ttk.Label(frame, text="앨범 전체 링크", font=("TkDefaultFont", 10, "bold")).grid(row=row, column=0, columnspan=3, sticky="w", pady=(16, 6))
        row += 1
        self.album_links_frame = ttk.Frame(frame)
        self.album_links_frame.grid(row=row, column=0, columnspan=3, sticky="ew")
        self.album_links_frame.columnconfigure(1, weight=1)

    def _build_tracks_tab(self) -> None:
        tab = ttk.Frame(self.tabs, padding=8)
        self.tabs.add(tab, text="곡 링크/가사/MV")
        tab.columnconfigure(1, weight=1)
        tab.rowconfigure(0, weight=1)

        left = ttk.Frame(tab)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        ttk.Label(left, text="현재 앨범의 곡 목록", font=("TkDefaultFont", 10, "bold")).pack(anchor="w")
        self.track_list = tk.Listbox(left, width=34, exportselection=False)
        self.track_list.pack(fill="both", expand=True, pady=(8, 8))
        self.track_list.bind("<<ListboxSelect>>", self._on_track_select)
        track_buttons = ttk.Frame(left)
        track_buttons.pack(fill="x")
        ttk.Button(track_buttons, text="추가", command=self.add_track).grid(row=0, column=0, sticky="ew", padx=2, pady=2)
        ttk.Button(track_buttons, text="복제", command=self.duplicate_track).grid(row=0, column=1, sticky="ew", padx=2, pady=2)
        ttk.Button(track_buttons, text="삭제", command=self.delete_track).grid(row=0, column=2, sticky="ew", padx=2, pady=2)
        ttk.Button(track_buttons, text="위", command=lambda: self.move_track(-1)).grid(row=1, column=0, sticky="ew", padx=2, pady=2)
        ttk.Button(track_buttons, text="아래", command=lambda: self.move_track(1)).grid(row=1, column=1, sticky="ew", padx=2, pady=2)
        for col in range(3):
            track_buttons.columnconfigure(col, weight=1)

        right_scroll = ScrollFrame(tab)
        right_scroll.grid(row=0, column=1, sticky="nsew")
        frame = right_scroll.inner
        frame.columnconfigure(1, weight=1)
        self._label_entry(frame, 0, "곡 제목", self.track_title_var)
        ttk.Label(frame, text="가사").grid(row=1, column=0, sticky="nw", padx=(0, 8), pady=4)
        self.lyrics_text = tk.Text(frame, height=12, wrap="word")
        self.lyrics_text.grid(row=1, column=1, sticky="nsew", pady=4)
        ttk.Label(frame, text="곡별 서비스 링크", font=("TkDefaultFont", 10, "bold")).grid(row=2, column=0, columnspan=2, sticky="w", pady=(16, 6))
        self.track_links_frame = ttk.Frame(frame)
        self.track_links_frame.grid(row=3, column=0, columnspan=2, sticky="ew")
        self.track_links_frame.columnconfigure(1, weight=1)
        ttk.Label(frame, text="곡별 뮤직비디오 URL", font=("TkDefaultFont", 10, "bold")).grid(row=4, column=0, columnspan=2, sticky="w", pady=(18, 6))
        self.track_video_links_frame = ttk.Frame(frame)
        self.track_video_links_frame.grid(row=5, column=0, columnspan=2, sticky="ew")
        self.track_video_links_frame.columnconfigure(1, weight=1)

    def refresh_all(self) -> None:
        self._loading = True
        self._load_site_fields()
        self._build_dynamic_link_fields()
        self.refresh_album_list()
        self.refresh_service_list()
        self._loading = False

    def _load_site_fields(self) -> None:
        project = self.data.get("project", {})
        self.site_vars["contactEmail"].set(self.data.get("contactEmail", ""))
        self.site_vars["project.nameKo"].set(project.get("nameKo", ""))
        self.site_vars["project.nameEn"].set(project.get("nameEn", ""))
        self.site_vars["project.image"].set(project.get("image", ""))

    def _store_site_fields(self) -> None:
        self.data["contactEmail"] = self.site_vars["contactEmail"].get().strip()
        self.data.setdefault("project", {})
        self.data["project"]["nameKo"] = self.site_vars["project.nameKo"].get().strip()
        self.data["project"]["nameEn"] = self.site_vars["project.nameEn"].get().strip()
        self.data["project"]["image"] = self.site_vars["project.image"].get().strip()

    def _build_dynamic_link_fields(self) -> None:
        for child in self.album_links_frame.winfo_children():
            child.destroy()
        for child in self.track_links_frame.winfo_children():
            child.destroy()
        for child in self.track_video_links_frame.winfo_children():
            child.destroy()
        self.album_link_vars.clear()
        self.track_link_vars.clear()
        self.track_video_link_vars.clear()
        for row, service in enumerate(self.data.get("services", [])):
            sid = service.get("id", "")
            label = service.get("label", sid)
            self.album_link_vars[sid] = tk.StringVar()
            self.track_link_vars[sid] = tk.StringVar()
            self.track_video_link_vars[sid] = tk.StringVar()
            ttk.Label(self.album_links_frame, text=label).grid(row=row, column=0, sticky="w", padx=(0, 8), pady=3)
            ttk.Entry(self.album_links_frame, textvariable=self.album_link_vars[sid]).grid(row=row, column=1, sticky="ew", pady=3)
            ttk.Label(self.track_links_frame, text=label).grid(row=row, column=0, sticky="w", padx=(0, 8), pady=3)
            ttk.Entry(self.track_links_frame, textvariable=self.track_link_vars[sid]).grid(row=row, column=1, sticky="ew", pady=3)
            ttk.Label(self.track_video_links_frame, text=label).grid(row=row, column=0, sticky="w", padx=(0, 8), pady=3)
            ttk.Entry(self.track_video_links_frame, textvariable=self.track_video_link_vars[sid]).grid(row=row, column=1, sticky="ew", pady=3)

    def refresh_album_list(self) -> None:
        self.album_list.delete(0, "end")
        for idx, album in enumerate(self.data.get("albums", []), start=1):
            self.album_list.insert("end", f"{idx:02d}. {album.get('title', 'Untitled')}  [{album.get('status', '')}]")

    def refresh_service_list(self) -> None:
        self.service_list.delete(0, "end")
        for service in self.data.get("services", []):
            self.service_list.insert("end", f"{service.get('label', '')} ({service.get('id', '')})")

    def refresh_track_list(self) -> None:
        self.track_list.delete(0, "end")
        album = self.current_album()
        if not album:
            return
        for idx, track in enumerate(album.get("tracks", []), start=1):
            self.track_list.insert("end", f"{idx:02d}. {track.get('title', 'Untitled')}")

    def current_album(self) -> Optional[Dict[str, Any]]:
        if self.current_album_index is None:
            return None
        albums = self.data.get("albums", [])
        if 0 <= self.current_album_index < len(albums):
            return albums[self.current_album_index]
        return None

    def current_track(self) -> Optional[Dict[str, Any]]:
        album = self.current_album()
        if not album or self.current_track_index is None:
            return None
        tracks = album.get("tracks", [])
        if 0 <= self.current_track_index < len(tracks):
            return tracks[self.current_track_index]
        return None

    def current_service(self) -> Optional[Dict[str, Any]]:
        if self.current_service_index is None:
            return None
        services = self.data.get("services", [])
        if 0 <= self.current_service_index < len(services):
            return services[self.current_service_index]
        return None

    def _on_album_select(self, _event: tk.Event) -> None:
        if self._loading:
            return
        selection = self.album_list.curselection()
        if selection:
            self.select_album(selection[0])

    def select_album(self, index: int) -> None:
        self.store_current_album()
        self.store_current_track()
        self.current_album_index = index
        self.current_track_index = None
        self._loading = True
        self.album_list.selection_clear(0, "end")
        self.album_list.selection_set(index)
        self.album_list.activate(index)
        self.load_album_fields()
        self.refresh_track_list()
        self.clear_track_fields()
        self._loading = False
        if self.current_album() and self.current_album().get("tracks"):
            self.select_track(0)

    def _on_track_select(self, _event: tk.Event) -> None:
        if self._loading:
            return
        selection = self.track_list.curselection()
        if selection:
            self.select_track(selection[0])

    def select_track(self, index: int) -> None:
        self.store_current_track()
        self.current_track_index = index
        self._loading = True
        self.track_list.selection_clear(0, "end")
        self.track_list.selection_set(index)
        self.track_list.activate(index)
        self.load_track_fields()
        self._loading = False

    def _on_service_select(self, _event: tk.Event) -> None:
        if self._loading:
            return
        selection = self.service_list.curselection()
        if selection:
            self.select_service(selection[0])

    def select_service(self, index: int) -> None:
        self.store_current_service()
        self.current_service_index = index
        self._loading = True
        self.service_list.selection_clear(0, "end")
        self.service_list.selection_set(index)
        self.service_list.activate(index)
        service = self.current_service()
        if service:
            for key, var in self.service_vars.items():
                var.set(service.get(key, ""))
        self._loading = False

    def load_album_fields(self) -> None:
        album = self.current_album()
        if not album:
            return
        for key, var in self.album_vars.items():
            if key == "tags":
                var.set(", ".join(album.get("tags", [])))
            else:
                var.set(str(album.get(key, "")))
        self.album_description.delete("1.0", "end")
        self.album_description.insert("1.0", album.get("description", ""))
        for sid, var in self.album_link_vars.items():
            var.set(album.get("albumLinks", {}).get(sid, ""))

    def store_current_album(self) -> None:
        if self._loading:
            return
        album = self.current_album()
        if not album:
            return
        for key, var in self.album_vars.items():
            if key == "tags":
                album["tags"] = [tag.strip() for tag in var.get().split(",") if tag.strip()]
            else:
                album[key] = var.get().strip()
        album["description"] = self.album_description.get("1.0", "end").rstrip("\n")
        album.setdefault("albumLinks", {})
        for sid, var in self.album_link_vars.items():
            album["albumLinks"][sid] = var.get().strip()

    def clear_track_fields(self) -> None:
        self.track_title_var.set("")
        self.lyrics_text.delete("1.0", "end")
        for var in self.track_link_vars.values():
            var.set("")
        for var in self.track_video_link_vars.values():
            var.set("")

    def load_track_fields(self) -> None:
        track = self.current_track()
        if not track:
            self.clear_track_fields()
            return
        self.track_title_var.set(track.get("title", ""))
        self.lyrics_text.delete("1.0", "end")
        self.lyrics_text.insert("1.0", track.get("lyrics", ""))
        for sid, var in self.track_link_vars.items():
            var.set(track.get("links", {}).get(sid, ""))
        for sid, var in self.track_video_link_vars.items():
            var.set(track.get("videoLinks", {}).get(sid, ""))

    def store_current_track(self) -> None:
        if self._loading:
            return
        track = self.current_track()
        if not track:
            return
        track["title"] = self.track_title_var.get().strip() or "Untitled Track"
        track["lyrics"] = self.lyrics_text.get("1.0", "end").rstrip("\n")
        track.setdefault("links", {})
        track.setdefault("videoLinks", {})
        for sid, var in self.track_link_vars.items():
            track["links"][sid] = var.get().strip()
        for sid, var in self.track_video_link_vars.items():
            track["videoLinks"][sid] = var.get().strip()

    def store_current_service(self) -> None:
        if self._loading:
            return
        service = self.current_service()
        if not service:
            return
        old_id = service.get("id", "")
        new_id = self.service_vars["id"].get().strip() or old_id
        service["id"] = new_id
        service["label"] = self.service_vars["label"].get().strip() or new_id
        service["short"] = self.service_vars["short"].get().strip() or service["label"][:2].upper()
        service["icon"] = self.service_vars["icon"].get().strip()
        if old_id and new_id != old_id:
            self.rename_service_id(old_id, new_id)

    def rename_service_id(self, old_id: str, new_id: str) -> None:
        for album in self.data.get("albums", []):
            links = album.setdefault("albumLinks", {})
            if old_id in links and new_id not in links:
                links[new_id] = links.pop(old_id)
            for track in album.get("tracks", []):
                tlinks = track.setdefault("links", {})
                if old_id in tlinks and new_id not in tlinks:
                    tlinks[new_id] = tlinks.pop(old_id)
                vlinks = track.setdefault("videoLinks", {})
                if old_id in vlinks and new_id not in vlinks:
                    vlinks[new_id] = vlinks.pop(old_id)

    def add_album(self) -> None:
        self.store_all_fields()
        album = new_album(self.data)
        album["id"] = self.unique_album_id(album["id"])
        self.data.setdefault("albums", []).append(album)
        self.refresh_album_list()
        self.select_album(len(self.data["albums"]) - 1)

    def duplicate_album(self) -> None:
        album = self.current_album()
        if not album:
            return
        self.store_all_fields()
        clone = copy.deepcopy(album)
        clone["title"] = clone.get("title", "앨범") + " Copy"
        clone["id"] = self.unique_album_id(slugify(clone["title"], "album"))
        self.data["albums"].insert(self.current_album_index + 1, clone)
        self.refresh_album_list()
        self.select_album(self.current_album_index + 1)

    def delete_album(self) -> None:
        album = self.current_album()
        if not album:
            return
        if not messagebox.askyesno("앨범 삭제", f"'{album.get('title')}' 앨범을 삭제할까요?"):
            return
        del self.data["albums"][self.current_album_index]
        self.current_album_index = None
        self.refresh_album_list()
        if self.data["albums"]:
            self.select_album(min(0, len(self.data["albums"]) - 1))
        else:
            self.clear_album_ui()

    def move_album(self, direction: int) -> None:
        if self.current_album_index is None:
            return
        self.store_all_fields()
        albums = self.data["albums"]
        new_index = self.current_album_index + direction
        if not (0 <= new_index < len(albums)):
            return
        albums[self.current_album_index], albums[new_index] = albums[new_index], albums[self.current_album_index]
        self.current_album_index = new_index
        self.refresh_album_list()
        self.select_album(new_index)

    def clear_album_ui(self) -> None:
        for var in self.album_vars.values():
            var.set("")
        self.album_description.delete("1.0", "end")
        for var in self.album_link_vars.values():
            var.set("")
        self.refresh_track_list()
        self.clear_track_fields()

    def add_track(self) -> None:
        album = self.current_album()
        if not album:
            return
        self.store_all_fields()
        album.setdefault("tracks", []).append(new_track(self.data))
        album["trackCount"] = f"{len(album['tracks'])}곡"
        self.refresh_track_list()
        self.select_track(len(album["tracks"]) - 1)
        self.load_album_fields()

    def duplicate_track(self) -> None:
        album = self.current_album()
        track = self.current_track()
        if not album or not track:
            return
        self.store_all_fields()
        clone = copy.deepcopy(track)
        clone["title"] = clone.get("title", "곡") + " Copy"
        album["tracks"].insert(self.current_track_index + 1, clone)
        album["trackCount"] = f"{len(album['tracks'])}곡"
        self.refresh_track_list()
        self.select_track(self.current_track_index + 1)
        self.load_album_fields()

    def delete_track(self) -> None:
        album = self.current_album()
        track = self.current_track()
        if not album or not track:
            return
        if not messagebox.askyesno("곡 삭제", f"'{track.get('title')}' 곡을 삭제할까요?"):
            return
        del album["tracks"][self.current_track_index]
        album["trackCount"] = f"{len(album['tracks'])}곡"
        self.current_track_index = None
        self.refresh_track_list()
        self.load_album_fields()
        if album["tracks"]:
            self.select_track(0)
        else:
            self.clear_track_fields()

    def move_track(self, direction: int) -> None:
        album = self.current_album()
        if not album or self.current_track_index is None:
            return
        self.store_all_fields()
        tracks = album.get("tracks", [])
        new_index = self.current_track_index + direction
        if not (0 <= new_index < len(tracks)):
            return
        tracks[self.current_track_index], tracks[new_index] = tracks[new_index], tracks[self.current_track_index]
        self.current_track_index = new_index
        self.refresh_track_list()
        self.select_track(new_index)

    def add_service(self) -> None:
        self.store_all_fields()
        sid = self.unique_service_id("new-service")
        service = {"id": sid, "label": "New Service", "short": "NS", "icon": ""}
        self.data.setdefault("services", []).append(service)
        normalize_data(self.data)
        self._build_dynamic_link_fields()
        self.refresh_service_list()
        self.refresh_album_list()
        self.select_service(len(self.data["services"]) - 1)
        if self.current_album_index is not None:
            self.load_album_fields()
        if self.current_track_index is not None:
            self.load_track_fields()

    def delete_service(self) -> None:
        service = self.current_service()
        if not service:
            return
        if not messagebox.askyesno("서비스 삭제", f"'{service.get('label')}' 서비스를 삭제할까요? 관련 링크 칸도 함께 제거됩니다."):
            return
        sid = service.get("id")
        del self.data["services"][self.current_service_index]
        for album in self.data.get("albums", []):
            album.get("albumLinks", {}).pop(sid, None)
            for track in album.get("tracks", []):
                track.get("links", {}).pop(sid, None)
                track.get("videoLinks", {}).pop(sid, None)
        self.current_service_index = None
        self._build_dynamic_link_fields()
        self.refresh_service_list()
        if self.data["services"]:
            self.select_service(0)
        if self.current_album_index is not None:
            self.load_album_fields()
        if self.current_track_index is not None:
            self.load_track_fields()

    def autofill_album_id(self) -> None:
        title = self.album_vars["title"].get().strip() or self.album_vars["titleEn"].get().strip() or "album"
        self.album_vars["id"].set(self.unique_album_id(slugify(title, "album")))

    def unique_album_id(self, base: str) -> str:
        used = {a.get("id") for a in self.data.get("albums", []) if a is not self.current_album()}
        candidate = base
        count = 2
        while candidate in used:
            candidate = f"{base}-{count}"
            count += 1
        return candidate

    def unique_service_id(self, base: str) -> str:
        used = {s.get("id") for s in self.data.get("services", [])}
        candidate = base
        count = 2
        while candidate in used:
            candidate = f"{base}-{count}"
            count += 1
        return candidate

    def store_all_fields(self) -> None:
        self._store_site_fields()
        self.store_current_service()
        self.store_current_album()
        self.store_current_track()
        normalize_data(self.data)

    def choose_asset(self, target_dir_rel: Path, suggested_stem: str, var: tk.StringVar) -> None:
        filetypes = [
            ("Image files", "*.png *.jpg *.jpeg *.webp *.svg"),
            ("All files", "*.*"),
        ]
        selected = filedialog.askopenfilename(title="이미지 선택", filetypes=filetypes)
        if not selected:
            return
        source = Path(selected)
        target_dir = self.site_root / target_dir_rel
        target_dir.mkdir(parents=True, exist_ok=True)
        stem = slugify(suggested_stem, "image")
        target = target_dir / f"{stem}{source.suffix.lower()}"
        if source.resolve() != target.resolve():
            shutil.copy2(source, target)
        var.set(posix_rel(target, self.site_root))

    def choose_project_image(self) -> None:
        self.choose_asset(Path("assets/images"), "project", self.site_vars["project.image"])

    def choose_service_icon(self) -> None:
        service = self.current_service()
        stem = service.get("id", "service") if service else "service"
        self.choose_asset(SERVICE_ICON_DIR_REL, stem, self.service_vars["icon"])

    def choose_album_image(self, kind: str) -> None:
        album_id = self.album_vars["id"].get().strip() or slugify(self.album_vars["title"].get(), "album")
        suffix = "cover" if kind == "cover" else "booklet"
        self.choose_asset(ALBUM_IMAGE_DIR_REL, f"{album_id}-{suffix}", self.album_vars[kind])

    def save(self) -> None:
        try:
            self.store_all_fields()
            save_data(self.albums_js_path, self.data, make_backup=True)
            self.refresh_album_list()
            self.refresh_service_list()
            messagebox.showinfo("저장 완료", f"저장했습니다.\n{self.albums_js_path}")
        except Exception as exc:
            messagebox.showerror("저장 실패", str(exc))

    def reload(self) -> None:
        if not messagebox.askyesno("다시 불러오기", "저장하지 않은 변경사항을 버리고 다시 불러올까요?"):
            return
        self.data = load_data(self.albums_js_path)
        self.current_album_index = None
        self.current_track_index = None
        self.current_service_index = None
        self.refresh_all()
        if self.data.get("albums"):
            self.select_album(0)
        if self.data.get("services"):
            self.select_service(0)

    def export_json(self) -> None:
        self.store_all_fields()
        path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json"), ("All files", "*.*")])
        if not path:
            return
        Path(path).write_text(json.dumps(self.data, ensure_ascii=False, indent=2), encoding="utf-8")
        messagebox.showinfo("내보내기 완료", path)

    def import_json(self) -> None:
        path = filedialog.askopenfilename(filetypes=[("JSON", "*.json"), ("All files", "*.*")])
        if not path:
            return
        try:
            data = json.loads(Path(path).read_text(encoding="utf-8"))
            normalize_data(data)
        except Exception as exc:
            messagebox.showerror("가져오기 실패", str(exc))
            return
        self.data = data
        self.current_album_index = None
        self.current_track_index = None
        self.current_service_index = None
        self.refresh_all()
        if self.data.get("albums"):
            self.select_album(0)
        if self.data.get("services"):
            self.select_service(0)


def main() -> int:
    script_path = Path(__file__).resolve()
    site_root = find_site_root(script_path.parent)
    albums_js = site_root / ALBUMS_JS_REL
    if not albums_js.exists():
        message = f"assets/js/albums.js를 찾을 수 없습니다.\n현재 추정 루트: {site_root}"
        print(message)
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("파일 없음", message)
        finally:
            return 1
    app = AlbumManager(site_root)
    app.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
