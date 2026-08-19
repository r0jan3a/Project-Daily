import customtkinter as ctk
import tkinter as tk
from datetime import datetime
import json
import os
import random


# =========================================================
# 기본 설정
# =========================================================

FILE = "schedule.json"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

FONT = "Malgun Gothic"

BG = "#0B1120"
PANEL = "#111827"
CARD = "#182235"
CARD_HOVER = "#202C42"

TEXT = "#F8FAFC"
SUBTEXT = "#94A3B8"
BORDER = "#263449"

ACCENT = "#4F8CFF"
DANGER = "#EF4444"

TIMER_TRACK = "#263247"

COLORS = [
    "#60A5FA",
    "#34D399",
    "#FB923C",
    "#C084FC",
    "#F87171",
    "#2DD4BF",
]


# =========================================================
# 데이터 관리
# =========================================================

def fix_time(value):
    value = str(value).strip()

    if ":" in value:
        try:
            return datetime.strptime(
                value,
                "%H:%M"
            ).strftime("%H:%M")
        except ValueError:
            return "00:00"

    if len(value) == 1:
        value = f"0{value}00"

    elif len(value) == 2:
        value += "00"

    elif len(value) == 3:
        value = "0" + value

    if len(value) == 4:
        try:
            return datetime.strptime(
                value,
                "%H%M"
            ).strftime("%H:%M")
        except ValueError:
            pass

    return "00:00"


def load_data():

    if not os.path.exists(FILE):
        return []

    try:
        with open(
            FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        if not isinstance(data, list):
            return []

    except (
        OSError,
        json.JSONDecodeError
    ):
        return []

    changed = False
    valid_data = []

    for item in data:

        if not isinstance(item, dict):
            continue

        if not {
            "start",
            "end",
            "name"
        }.issubset(item):
            continue

        new_start = fix_time(
            item["start"]
        )

        new_end = fix_time(
            item["end"]
        )

        if new_start != item["start"]:
            item["start"] = new_start
            changed = True

        if new_end != item["end"]:
            item["end"] = new_end
            changed = True

        if "color" not in item:
            item["color"] = random.choice(
                COLORS
            )
            changed = True

        valid_data.append(item)

    valid_data.sort(
        key=lambda item: item["start"]
    )

    if changed:
        write_data(valid_data)

    return valid_data


def write_data(data):

    try:
        with open(
            FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=4
            )

    except OSError as error:
        print(
            f"저장 실패: {error}"
        )


def save_data():
    write_data(schedules)


schedules = load_data()


# =========================================================
# 시간 목록
# =========================================================

times = [
    f"{hour:02}:{minute:02}"
    for hour in range(24)
    for minute in (0, 30)
]


# =========================================================
# 메인 창
# =========================================================

app = ctk.CTk()

app.title("Project Daily")

app.geometry(
    "920x900"
)

app.minsize(
    760,
    760
)

app.configure(
    fg_color=BG
)

app.grid_columnconfigure(
    0,
    weight=1
)

app.grid_rowconfigure(
    2,
    weight=1
)


# =========================================================
# Header
# =========================================================

header = ctk.CTkFrame(
    app,
    fg_color="transparent"
)

header.grid(
    row=0,
    column=0,
    sticky="ew",
    padx=36,
    pady=(28, 18)
)

header.grid_columnconfigure(
    0,
    weight=1
)


title = ctk.CTkLabel(
    header,
    text="Project Daily",
    font=(
        FONT,
        30,
        "bold"
    ),
    text_color=TEXT
)

title.grid(
    row=0,
    column=0,
    sticky="w"
)


subtitle = ctk.CTkLabel(
    header,
    text="오늘의 시간을 계획하고 집중해 보세요.",
    font=(
        FONT,
        14
    ),
    text_color=SUBTEXT
)

subtitle.grid(
    row=1,
    column=0,
    sticky="w",
    pady=(4, 0)
)


clock = ctk.CTkLabel(
    header,
    text="",
    font=(
        FONT,
        15,
        "bold"
    ),
    text_color="#CBD5E1"
)

clock.grid(
    row=0,
    column=1,
    rowspan=2,
    sticky="e"
)


# =========================================================
# 현재 일정 카드
# =========================================================

current_frame = ctk.CTkFrame(
    app,
    fg_color=PANEL,
    corner_radius=20,
    border_width=1,
    border_color=BORDER
)

current_frame.grid(
    row=1,
    column=0,
    sticky="ew",
    padx=36,
    pady=(0, 22)
)

current_frame.grid_columnconfigure(
    0,
    weight=1
)


# =========================================================
# NOW
# =========================================================

current_caption = ctk.CTkLabel(
    current_frame,
    text="NOW",
    font=(
        FONT,
        12,
        "bold"
    ),
    text_color=ACCENT
)

current_caption.grid(
    row=0,
    column=0,
    pady=(20, 0)
)


# =========================================================
# 원형 타이머
# =========================================================

TIMER_SIZE = 300

CENTER = TIMER_SIZE // 2

RING_MARGIN = 35
RING_WIDTH = 16

ARC_BOX = (
    RING_MARGIN,
    RING_MARGIN,
    TIMER_SIZE - RING_MARGIN,
    TIMER_SIZE - RING_MARGIN
)


timer_canvas = tk.Canvas(
    current_frame,
    width=TIMER_SIZE,
    height=TIMER_SIZE,
    bg=PANEL,
    highlightthickness=0
)

timer_canvas.grid(
    row=1,
    column=0,
    pady=(8, 8)
)


# =========================================================
# 원형 배경
# =========================================================

timer_canvas.create_arc(
    ARC_BOX,
    start=90,
    extent=-359.9,
    style=tk.ARC,
    outline=TIMER_TRACK,
    width=RING_WIDTH
)


# =========================================================
# 진행 원
# =========================================================

progress_arc = timer_canvas.create_arc(
    ARC_BOX,
    start=90,
    extent=-359.9,
    style=tk.ARC,
    outline=ACCENT,
    width=RING_WIDTH
)


# =========================================================
# 중앙 영역
# =========================================================

INNER_RADIUS = 94

timer_canvas.create_oval(
    CENTER - INNER_RADIUS,
    CENTER - INNER_RADIUS,
    CENTER + INNER_RADIUS,
    CENTER + INNER_RADIUS,
    fill=PANEL,
    outline=""
)


# =========================================================
# 중앙 시간
# =========================================================

timer_text = timer_canvas.create_text(
    CENTER,
    CENTER - 10,
    text="00:00",
    fill=TEXT,
    font=(
        FONT,
        32,
        "bold"
    )
)


# =========================================================
# 중앙 상태
# =========================================================

timer_status = timer_canvas.create_text(
    CENTER,
    CENTER + 28,
    text="NO SCHEDULE",
    fill=SUBTEXT,
    font=(
        FONT,
        11,
        "bold"
    )
)


# =========================================================
# 현재 일정 이름
# =========================================================

current_label = ctk.CTkLabel(
    current_frame,
    text="현재 일정 없음",
    font=(
        FONT,
        18,
        "bold"
    ),
    text_color=TEXT
)

current_label.grid(
    row=2,
    column=0,
    pady=(0, 3)
)


# =========================================================
# 현재 일정 시간
# =========================================================

current_time_label = ctk.CTkLabel(
    current_frame,
    text="",
    font=(
        FONT,
        13
    ),
    text_color=SUBTEXT
)

current_time_label.grid(
    row=3,
    column=0,
    pady=(0, 20)
)


# =========================================================
# 전체화면 변수
# =========================================================

fullscreen_window = None

fullscreen_canvas = None

fullscreen_progress_arc = None
fullscreen_timer_text = None
fullscreen_timer_status = None
fullscreen_name_text = None
fullscreen_time_text = None


# =========================================================
# 전체화면 버튼
# =========================================================

def open_fullscreen_timer():
    global fullscreen_window
    global fullscreen_canvas
    global fullscreen_progress_arc
    global fullscreen_timer_text
    global fullscreen_timer_status
    global fullscreen_name_text
    global fullscreen_time_text

    # 이미 전체화면이 열려 있으면 새로 만들지 않음
    if fullscreen_window is not None:

        try:

            if fullscreen_window.winfo_exists():

                fullscreen_window.focus_force()

                return

        except tk.TclError:
            pass


    # -----------------------------------------------------
    # 새 창
    # -----------------------------------------------------

    fullscreen_window = tk.Toplevel(
        app
    )

    fullscreen_window.configure(
        bg=BG
    )

    fullscreen_window.attributes(
        "-fullscreen",
        True
    )

    fullscreen_window.protocol(
        "WM_DELETE_WINDOW",
        close_fullscreen_timer
    )

    fullscreen_window.bind(
        "<Escape>",
        lambda event:
            close_fullscreen_timer()
    )


    # -----------------------------------------------------
    # Canvas
    # -----------------------------------------------------

    fullscreen_canvas = tk.Canvas(
        fullscreen_window,
        bg=BG,
        highlightthickness=0
    )

    fullscreen_canvas.pack(
        fill="both",
        expand=True
    )


    # 화면 크기 계산
    fullscreen_window.update_idletasks()

    width = fullscreen_window.winfo_width()
    height = fullscreen_window.winfo_height()

    center_x = width // 2
    center_y = height // 2


    # -----------------------------------------------------
    # 전체화면 타이머 크기
    # -----------------------------------------------------

    timer_size = int(
        min(width, height) * 0.55
    )

    margin = 35

    x1 = (
        center_x
        - timer_size // 2
        + margin
    )

    y1 = (
        center_y
        - timer_size // 2
        + margin
    )

    x2 = (
        center_x
        + timer_size // 2
        - margin
    )

    y2 = (
        center_y
        + timer_size // 2
        - margin
    )


    # -----------------------------------------------------
    # 배경 원
    # -----------------------------------------------------

    fullscreen_canvas.create_oval(
        x1,
        y1,
        x2,
        y2,
        outline=TIMER_TRACK,
        width=18
    )


    # -----------------------------------------------------
    # 진행 원
    # -----------------------------------------------------

    fullscreen_progress_arc = (
        fullscreen_canvas.create_arc(
            x1,
            y1,
            x2,
            y2,
            start=90,
            extent=-359.9,
            style=tk.ARC,
            outline=ACCENT,
            width=18
        )
    )


    # -----------------------------------------------------
    # 중앙 영역
    # -----------------------------------------------------

    inner_radius = int(
        timer_size * 0.30
    )

    fullscreen_canvas.create_oval(
        center_x - inner_radius,
        center_y - inner_radius,
        center_x + inner_radius,
        center_y + inner_radius,
        fill=BG,
        outline=""
    )


    # -----------------------------------------------------
    # 시간
    # -----------------------------------------------------

    fullscreen_timer_text = (
        fullscreen_canvas.create_text(
            center_x,
            center_y - 20,
            text="00:00",
            fill=TEXT,
            font=(
                FONT,
                55,
                "bold"
            )
        )
    )


    # -----------------------------------------------------
    # 상태
    # -----------------------------------------------------

    fullscreen_timer_status = (
        fullscreen_canvas.create_text(
            center_x,
            center_y + 55,
            text="NO SCHEDULE",
            fill=SUBTEXT,
            font=(
                FONT,
                16,
                "bold"
            )
        )
    )


    # -----------------------------------------------------
    # 일정 이름
    # -----------------------------------------------------

    fullscreen_name_text = (
        fullscreen_canvas.create_text(
            center_x,
            center_y
            + timer_size // 2
            + 55,
            text="현재 일정 없음",
            fill=TEXT,
            font=(
                FONT,
                24,
                "bold"
            )
        )
    )


    # -----------------------------------------------------
    # 일정 시간
    # -----------------------------------------------------

    fullscreen_time_text = (
        fullscreen_canvas.create_text(
            center_x,
            center_y
            + timer_size // 2
            + 90,
            text="",
            fill=SUBTEXT,
            font=(
                FONT,
                14
            )
        )
    )


    # -----------------------------------------------------
    # 종료 버튼
    # -----------------------------------------------------

    fullscreen_canvas.create_text(
        width - 45,
        height - 40,
        text="⛶",
        fill=SUBTEXT,
        font=(
            FONT,
            20,
            "bold"
        ),
        tags="close_button"
    )

    fullscreen_canvas.tag_bind(
        "close_button",
        "<Button-1>",
        lambda event:
            close_fullscreen_timer()
    )


def close_fullscreen_timer():

    global fullscreen_window
    global fullscreen_canvas

    if fullscreen_window is not None:

        try:
            fullscreen_window.destroy()

        except tk.TclError:
            pass

    fullscreen_window = None
    fullscreen_canvas = None


fullscreen_button = ctk.CTkButton(
    current_frame,
    text="⛶",
    width=38,
    height=32,
    corner_radius=8,
    font=(
        FONT,
        16,
        "bold"
    ),
    fg_color=CARD,
    hover_color=CARD_HOVER,
    text_color=SUBTEXT,
    command=open_fullscreen_timer
)

fullscreen_button.place(
    relx=1.0,
    rely=1.0,
    anchor="se",
    x=-14,
    y=-14
)


# =========================================================
# 일정 목록
# =========================================================

content = ctk.CTkFrame(
    app,
    fg_color="transparent"
)

content.grid(
    row=2,
    column=0,
    sticky="nsew",
    padx=36
)

content.grid_columnconfigure(
    0,
    weight=1
)

content.grid_rowconfigure(
    1,
    weight=1
)


# =========================================================
# 일정 목록 Header
# =========================================================

list_header = ctk.CTkFrame(
    content,
    fg_color="transparent"
)

list_header.grid(
    row=0,
    column=0,
    sticky="ew",
    pady=(0, 10)
)

list_header.grid_columnconfigure(
    0,
    weight=1
)


list_title = ctk.CTkLabel(
    list_header,
    text="오늘의 일정",
    font=(
        FONT,
        21,
        "bold"
    ),
    text_color=TEXT
)

list_title.grid(
    row=0,
    column=0,
    sticky="w"
)


count_label = ctk.CTkLabel(
    list_header,
    text="0개의 일정",
    font=(
        FONT,
        13
    ),
    text_color=SUBTEXT
)

count_label.grid(
    row=0,
    column=1,
    sticky="e"
)


# =========================================================
# Scrollable 일정 영역
# =========================================================

schedule_frame = ctk.CTkScrollableFrame(
    content,
    fg_color=PANEL,
    corner_radius=16,
    border_width=1,
    border_color=BORDER,
    scrollbar_button_color="#334155",
    scrollbar_button_hover_color="#475569"
)

schedule_frame.grid(
    row=1,
    column=0,
    sticky="nsew"
)

schedule_frame.grid_columnconfigure(
    0,
    weight=1
)


# =========================================================
# 입력 영역
# =========================================================

input_frame = ctk.CTkFrame(
    app,
    fg_color=PANEL,
    corner_radius=16,
    border_width=1,
    border_color=BORDER
)

input_frame.grid(
    row=3,
    column=0,
    sticky="ew",
    padx=36,
    pady=24
)

input_frame.grid_columnconfigure(
    2,
    weight=1
)


# =========================================================
# 시작 시간
# =========================================================

start_menu = ctk.CTkOptionMenu(
    input_frame,
    values=times,
    width=125,
    height=42,
    font=(
        FONT,
        14
    ),
    fg_color=CARD,
    button_color="#334155",
    button_hover_color="#475569"
)

start_menu.grid(
    row=0,
    column=0,
    padx=(18, 7),
    pady=(18, 8)
)

start_menu.set(
    "09:00"
)


# =========================================================
# 종료 시간
# =========================================================

end_menu = ctk.CTkOptionMenu(
    input_frame,
    values=times,
    width=125,
    height=42,
    font=(
        FONT,
        14
    ),
    fg_color=CARD,
    button_color="#334155",
    button_hover_color="#475569"
)

end_menu.grid(
    row=0,
    column=1,
    padx=7,
    pady=(18, 8)
)

end_menu.set(
    "10:00"
)


# =========================================================
# 일정 이름
# =========================================================

name_entry = ctk.CTkEntry(
    input_frame,
    height=42,
    placeholder_text="일정 이름을 입력하세요",
    font=(
        FONT,
        14
    ),
    fg_color=CARD,
    border_color="#334155"
)

name_entry.grid(
    row=0,
    column=2,
    sticky="ew",
    padx=7,
    pady=(18, 8)
)


# =========================================================
# 추가 버튼
# =========================================================

add_button = ctk.CTkButton(
    input_frame,
    text="＋ 일정 추가",
    width=130,
    height=42,
    font=(
        FONT,
        14,
        "bold"
    ),
    fg_color=ACCENT,
    hover_color="#3977E8"
)

add_button.grid(
    row=0,
    column=3,
    padx=(7, 18),
    pady=(18, 8)
)


# =========================================================
# 메시지
# =========================================================

message_label = ctk.CTkLabel(
    input_frame,
    text="",
    font=(
        FONT,
        12
    ),
    text_color="#F87171"
)

message_label.grid(
    row=1,
    column=0,
    columnspan=4,
    pady=(0, 12)
)


# =========================================================
# 일정 목록 갱신
# =========================================================

def refresh_list():

    for widget in schedule_frame.winfo_children():
        widget.destroy()

    count_label.configure(
        text=f"{len(schedules)}개의 일정"
    )

    if not schedules:

        empty_label = ctk.CTkLabel(
            schedule_frame,
            text=(
                "등록된 일정이 없습니다.\n"
                "아래에서 새로운 일정을 추가해 보세요."
            ),
            font=(
                FONT,
                14
            ),
            text_color=SUBTEXT,
            justify="center"
        )

        empty_label.grid(
            row=0,
            column=0,
            pady=65
        )

        return


    for index, item in enumerate(schedules):

        card = ctk.CTkFrame(
            schedule_frame,
            fg_color=CARD,
            corner_radius=12,
            border_width=1,
            border_color=BORDER
        )

        card.grid(
            row=index,
            column=0,
            sticky="ew",
            padx=10,
            pady=(
                9 if index == 0 else 4,
                4
            )
        )

        card.grid_columnconfigure(
            2,
            weight=1
        )


        # -------------------------------------------------
        # 색상 바
        # -------------------------------------------------

        color_bar = ctk.CTkFrame(
            card,
            width=6,
            height=55,
            corner_radius=4,
            fg_color=item["color"]
        )

        color_bar.grid(
            row=0,
            column=0,
            padx=(12, 14),
            pady=12
        )


        # -------------------------------------------------
        # 시간
        # -------------------------------------------------

        time_label = ctk.CTkLabel(
            card,
            text=(
                f"{item['start']}\n"
                f"{item['end']}"
            ),
            width=70,
            font=(
                FONT,
                13,
                "bold"
            ),
            text_color=item["color"],
            justify="left"
        )

        time_label.grid(
            row=0,
            column=1,
            sticky="w"
        )


        # -------------------------------------------------
        # 이름
        # -------------------------------------------------

        name_label = ctk.CTkLabel(
            card,
            text=item["name"],
            font=(
                FONT,
                16,
                "bold"
            ),
            text_color=TEXT,
            anchor="w"
        )

        name_label.grid(
            row=0,
            column=2,
            sticky="ew",
            padx=15
        )


        # -------------------------------------------------
        # 삭제
        # -------------------------------------------------

        delete_button = ctk.CTkButton(
            card,
            text="삭제",
            width=62,
            height=32,
            corner_radius=8,
            font=(
                FONT,
                12
            ),
            fg_color="#2A1B24",
            hover_color=DANGER,
            text_color="#FCA5A5",
            command=lambda i=index:
                delete_schedule(i)
        )

        delete_button.grid(
            row=0,
            column=3,
            padx=14
        )


# =========================================================
# 일정 추가
# =========================================================

def add_schedule():

    name = name_entry.get().strip()

    start = start_menu.get()
    end = end_menu.get()


    if not name:

        show_message(
            "일정 이름을 입력해 주세요."
        )

        return


    start_time = datetime.strptime(
        start,
        "%H:%M"
    )

    end_time = datetime.strptime(
        end,
        "%H:%M"
    )


    if end_time <= start_time:

        show_message(
            "종료 시간은 시작 시간보다 늦어야 합니다."
        )

        return


    # -----------------------------------------------------
    # 일정 겹침 검사
    # -----------------------------------------------------

    for item in schedules:

        item_start = datetime.strptime(
            item["start"],
            "%H:%M"
        )

        item_end = datetime.strptime(
            item["end"],
            "%H:%M"
        )


        if (
            start_time < item_end
            and end_time > item_start
        ):

            show_message(
                f"‘{item['name']}’ 일정과 시간이 겹칩니다."
            )

            return


    # -----------------------------------------------------
    # 추가
    # -----------------------------------------------------

    schedules.append(
        {
            "start": start,
            "end": end,
            "name": name,
            "color": random.choice(
                COLORS
            )
        }
    )


    schedules.sort(
        key=lambda item: item["start"]
    )

    save_data()

    refresh_list()

    name_entry.delete(
        0,
        "end"
    )

    show_message(
        "일정이 추가되었습니다.",
        success=True
    )


# =========================================================
# 일정 삭제
# =========================================================

def delete_schedule(index):

    schedules.pop(index)

    save_data()

    refresh_list()

    show_message(
        "일정이 삭제되었습니다.",
        success=True
    )


# =========================================================
# 메시지
# =========================================================

def show_message(
    message,
    success=False
):

    message_label.configure(
        text=message,
        text_color=(
            "#34D399"
            if success
            else "#F87171"
        )
    )

    app.after(
        2500,
        lambda:
            message_label.configure(
                text=""
            )
    )


# =========================================================
# 버튼 이벤트
# =========================================================

add_button.configure(
    command=add_schedule
)

name_entry.bind(
    "<Return>",
    lambda event:
        add_schedule()
)


# =========================================================
# 원형 타이머 업데이트
# =========================================================

def update_circular_timer(
    ratio,
    color
):

    ratio = min(
        max(
            ratio,
            0
        ),
        1
    )


    # -----------------------------------------------------
    # 남은 시간 비율
    # -----------------------------------------------------

    remaining_ratio = 1 - ratio


    # -----------------------------------------------------
    # 원호 각도
    # -----------------------------------------------------

    extent = (
        -359.9
        * remaining_ratio
    )


    # -----------------------------------------------------
    # 기본 화면 원형 타이머
    # -----------------------------------------------------

    timer_canvas.itemconfigure(
        progress_arc,
        extent=extent,
        outline=color
    )


    # -----------------------------------------------------
    # 전체화면 타이머
    # -----------------------------------------------------

    if fullscreen_canvas is not None:

        try:

            fullscreen_canvas.itemconfigure(
                fullscreen_progress_arc,
                extent=extent,
                outline=color
            )

        except tk.TclError:
            pass


# =========================================================
# 현재 일정 업데이트
# =========================================================

def update():

    now = datetime.now()


    # -----------------------------------------------------
    # 현재 시각
    # -----------------------------------------------------

    clock.configure(
        text=now.strftime(
            "%Y.%m.%d  %H:%M:%S"
        )
    )


    current = None

    start_datetime = None
    end_datetime = None


    # =====================================================
    # 현재 일정 찾기
    # =====================================================

    for item in schedules:

        start = datetime.strptime(
            item["start"],
            "%H:%M"
        ).replace(
            year=now.year,
            month=now.month,
            day=now.day
        )


        end = datetime.strptime(
            item["end"],
            "%H:%M"
        ).replace(
            year=now.year,
            month=now.month,
            day=now.day
        )


        if start <= now < end:

            current = item

            start_datetime = start

            end_datetime = end

            break


    # =====================================================
    # 현재 일정 있음
    # =====================================================

    if current:

        # -------------------------------------------------
        # 남은 시간
        # -------------------------------------------------

        remaining_seconds = max(
            0,
            int(
                (
                    end_datetime - now
                ).total_seconds()
            )
        )


        hours = (
            remaining_seconds
            // 3600
        )

        minutes = (
            remaining_seconds
            % 3600
        ) // 60

        seconds = (
            remaining_seconds
            % 60
        )


        # -------------------------------------------------
        # 전체 시간
        # -------------------------------------------------

        total = (
            end_datetime
            - start_datetime
        ).total_seconds()


        # -------------------------------------------------
        # 진행 시간
        # -------------------------------------------------

        passed = (
            now
            - start_datetime
        ).total_seconds()


        # -------------------------------------------------
        # 진행률
        # -------------------------------------------------

        ratio = min(
            max(
                passed / total,
                0
            ),
            1
        )


        # -------------------------------------------------
        # NOW
        # -------------------------------------------------

        current_caption.configure(
            text=(
                "NOW · "
                f"{current['start']} — "
                f"{current['end']}"
            ),
            text_color=current["color"]
        )


        # -------------------------------------------------
        # 타이머 텍스트
        # -------------------------------------------------

        if hours > 0:

            time_text = (
                f"{hours:02}:"
                f"{minutes:02}:"
                f"{seconds:02}"
            )

        else:

            time_text = (
                f"{minutes:02}:"
                f"{seconds:02}"
            )


        timer_canvas.itemconfigure(
            timer_text,
            text=time_text,
            fill=TEXT
        )


        # -------------------------------------------------
        # 상태
        # -------------------------------------------------

        timer_canvas.itemconfigure(
            timer_status,
            text="FOCUS",
            fill=current["color"]
        )


        # -------------------------------------------------
        # 원형 게이지
        # -------------------------------------------------

        update_circular_timer(
            ratio,
            current["color"]
        )


        # -------------------------------------------------
        # 일정 이름
        # -------------------------------------------------

        current_label.configure(
            text=current["name"]
        )


        # -------------------------------------------------
        # 일정 시간
        # -------------------------------------------------

        current_time_label.configure(
            text=(
                f"{current['start']}  —  "
                f"{current['end']}"
            )
        )


        # =================================================
        # 전체화면 타이머 갱신
        # =================================================

        if fullscreen_canvas is not None:

            try:

                fullscreen_canvas.itemconfigure(
                    fullscreen_timer_text,
                    text=time_text,
                    fill=TEXT
                )

                fullscreen_canvas.itemconfigure(
                    fullscreen_timer_status,
                    text="FOCUS",
                    fill=current["color"]
                )

                fullscreen_canvas.itemconfigure(
                    fullscreen_name_text,
                    text=current["name"],
                    fill=TEXT
                )

                fullscreen_canvas.itemconfigure(
                    fullscreen_time_text,
                    text=(
                        f"{current['start']}  —  "
                        f"{current['end']}"
                    ),
                    fill=SUBTEXT
                )

            except tk.TclError:
                pass


    # =====================================================
    # 현재 일정 없음
    # =====================================================

    else:

        current_caption.configure(
            text="NOW",
            text_color=ACCENT
        )


        timer_canvas.itemconfigure(
            timer_text,
            text="00:00",
            fill=TEXT
        )


        timer_canvas.itemconfigure(
            timer_status,
            text="NO SCHEDULE",
            fill=SUBTEXT
        )


        update_circular_timer(
            1,
            ACCENT
        )


        current_label.configure(
            text="현재 일정 없음"
        )


        current_time_label.configure(
            text=""
        )


        # =================================================
        # 전체화면 일정 없음
        # =================================================

        if fullscreen_canvas is not None:

            try:

                fullscreen_canvas.itemconfigure(
                    fullscreen_timer_text,
                    text="00:00",
                    fill=TEXT
                )

                fullscreen_canvas.itemconfigure(
                    fullscreen_timer_status,
                    text="NO SCHEDULE",
                    fill=SUBTEXT
                )

                fullscreen_canvas.itemconfigure(
                    fullscreen_name_text,
                    text="현재 일정 없음",
                    fill=TEXT
                )

                fullscreen_canvas.itemconfigure(
                    fullscreen_time_text,
                    text="",
                    fill=SUBTEXT
                )

            except tk.TclError:
                pass


    # ----------------------------------------------------- 
    # 1초 후 갱신
    # -----------------------------------------------------

    app.after(
        1000,
        update
    )


# =========================================================
# 실행
# =========================================================

refresh_list()

update()

app.mainloop()