# GRAND PAWS PET HOTEL - ลูกค้า + เจ้าของร้านในลิงก์เดียว

import os
import json
import hashlib
import gradio as gr
from datetime import datetime


# =========================================================
# ข้อมูลห้องพัก
# =========================================================

rooms = [
    {
        "name": "Standard Room",
        "price": 850,
        "description": "ห้องพักมาตรฐาน เหมาะสำหรับสัตว์เลี้ยง 1 ตัว",
        "status": "ว่าง"
    },
    {
        "name": "Deluxe Room",
        "price": 1000,
        "description": "ห้องกว้างขึ้น พร้อมพื้นที่พักผ่อนสำหรับสัตว์เลี้ยง",
        "status": "ว่าง"
    },
    {
        "name": "Grand Suite",
        "price": 1200,
        "description": "ห้องพิเศษ พื้นที่กว้าง พร้อมการดูแลเพิ่มเติม",
        "status": "ว่าง"
    }
]


# =========================================================
# บริการเสริม
# =========================================================

services = {
    "อาบน้ำ": 200,
    "ตัดขน": 300,
    "พาเดินเล่น": 100,
    "ให้อาหารพิเศษ": 100,
    "ดูแลเพิ่มเติม": 250
}


# =========================================================
# ข้อมูลระบบ
# =========================================================

bookings = []

user_data = {
    "name": "ผู้ใช้ Grand Paws",
    "phone": "-",
    "email": "-",
    "pets": []
}


# =========================================================
# โฟลเดอร์สำหรับ Render
# =========================================================

# ใช้โฟลเดอร์ภายในโปรเจกต์แทน /content
DATA_FOLDER = os.path.join(os.getcwd(), "Grand_Paws")

OWNER_FILE = os.path.join(DATA_FOLDER, "owner.json")

os.makedirs(DATA_FOLDER, exist_ok=True)


# =========================================================
# เข้ารหัสรหัสผ่าน
# =========================================================

def hash_password(password):
    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


# =========================================================
# สร้างบัญชีเจ้าของร้าน
# =========================================================

def create_owner(name, username, password, confirm):

    if not name:
        return "⚠️ กรุณากรอกชื่อเจ้าของร้าน"

    if not username:
        return "⚠️ กรุณากรอกชื่อผู้ใช้"

    if not password:
        return "⚠️ กรุณากรอกรหัสผ่าน"

    if password != confirm:
        return "⚠️ รหัสผ่านไม่ตรงกัน"

    if len(password) < 6:
        return "⚠️ รหัสผ่านควรมีอย่างน้อย 6 ตัวอักษร"

    if os.path.exists(OWNER_FILE):
        return "⚠️ มีบัญชีเจ้าของร้านอยู่แล้ว กรุณาเข้าสู่ระบบ"

    data = {
        "name": name,
        "username": username,
        "password": hash_password(password)
    }

    with open(
        OWNER_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=2
        )

    return (
        f"# ✅ สร้างบัญชีสำเร็จ\n\n"
        f"ยินดีต้อนรับ **{name}** 🐾\n\n"
        f"ชื่อผู้ใช้: **{username}**"
    )


# =========================================================
# เข้าสู่ระบบเจ้าของร้าน
# =========================================================

def owner_login(username, password):

    if not os.path.exists(OWNER_FILE):
        return (
            "⚠️ ยังไม่มีบัญชีเจ้าของร้าน "
            "กรุณาสร้างบัญชีก่อน"
        )

    try:

        with open(
            OWNER_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            owner = json.load(file)

    except Exception:
        return "⚠️ ไม่สามารถอ่านข้อมูลบัญชีเจ้าของร้านได้"

    if (
        username == owner["username"]
        and hash_password(password) == owner["password"]
    ):

        return (
            f"# 🟢 เข้าสู่ระบบสำเร็จ\n\n"
            f"ยินดีต้อนรับ **{owner['name']}** 🐾"
        )

    return (
        "# 🔴 เข้าสู่ระบบไม่สำเร็จ\n\n"
        "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง"
    )


# =========================================================
# หน้าแรก
# =========================================================

def home():

    return """
    <div class="welcome">
        <h1>🐾 Grand Paws</h1>
        <h3>PET HOTEL & CARE</h3>
        <h2>ยินดีต้อนรับสู่ Grand Paws</h2>
        <p>
            ดูแลสัตว์เลี้ยงของคุณด้วยความรัก
            เหมือนอยู่บ้าน ❤️
        </p>
    </div>
    """


# =========================================================
# แสดงห้องพัก
# =========================================================

def show_rooms():

    text = "# 🏠 ห้องพัก Grand Paws\n\n"

    for room in rooms:

        text += (
            f"### 🐾 {room['name']}\n"
            f"**ราคา:** {room['price']:,} บาท / คืน\n\n"
            f"{room['description']}\n\n"
            f"สถานะ: 🟢 **{room['status']}**\n\n"
            "---\n"
        )

    return text


# =========================================================
# แสดงบริการเสริม
# =========================================================

def show_services():

    text = "# 🛁 บริการเสริม\n\n"

    for name, price in services.items():

        text += (
            f"### 🐾 {name}\n"
            f"ราคา **{price:,} บาท**\n\n"
        )

    return text


# =========================================================
# คำนวณราคา
# =========================================================

def calc(
    owner,
    phone,
    pet,
    ptype,
    checkin,
    checkout,
    room,
    selected_services
):

    if not owner or not phone or not pet or not ptype:
        return "⚠️ กรุณากรอกข้อมูลให้ครบ"

    if not checkin or not checkout:
        return (
            "⚠️ กรุณาเลือกวันที่เข้าพัก "
            "และวันที่ออก"
        )

    try:

        nights = (
            datetime.strptime(
                checkout,
                "%Y-%m-%d"
            )
            -
            datetime.strptime(
                checkin,
                "%Y-%m-%d"
            )
        ).days

    except ValueError:

        return (
            "⚠️ วันที่ต้องเป็นรูปแบบ YYYY-MM-DD"
        )

    if nights <= 0:

        return (
            "⚠️ วันที่ออกต้องหลังวันที่เข้าพัก"
        )

    room_data = next(
        (
            room
            for room in rooms
            if room["name"] == room
        ),
        None
    )

    # แก้การค้นหาห้องให้ถูกต้อง
    room_data = next(
        (
            item
            for item in rooms
            if item["name"] == room
        ),
        None
    )

    if not room_data:

        return "⚠️ กรุณาเลือกห้องพัก"

    room_total = (
        room_data["price"] * nights
    )

    service_total = sum(
        services[name]
        for name in (selected_services or [])
        if name in services
    )

    total = room_total + service_total

    return (
        "## 🧾 สรุปการจอง\n\n"
        f"**เจ้าของ:** {owner}\n\n"
        f"**เบอร์โทร:** {phone}\n\n"
        f"**สัตว์เลี้ยง:** {pet} ({ptype})\n\n"
        f"**ห้อง:** {room}\n\n"
        f"**วันที่:** {checkin} → {checkout}\n\n"
        f"**จำนวน:** {nights} คืน\n\n"
        f"**ค่าห้อง:** {room_total:,} บาท\n\n"
        f"**บริการเสริม:** {service_total:,} บาท\n\n"
        f"# 💰 รวม {total:,} บาท\n\n"
        "กด **ยืนยันการจอง** "
        "เพื่อส่งรายการให้เจ้าของร้าน"
    )


# =========================================================
# ยืนยันการจอง
# =========================================================

def confirm(
    owner,
    phone,
    pet,
    ptype,
    checkin,
    checkout,
    room,
    selected_services
):

    result = calc(
        owner,
        phone,
        pet,
        ptype,
        checkin,
        checkout,
        room,
        selected_services
    )

    if result.startswith("⚠️"):
        return result

    nights = (
        datetime.strptime(
            checkout,
            "%Y-%m-%d"
        )
        -
        datetime.strptime(
            checkin,
            "%Y-%m-%d"
        )
    ).days

    room_data = next(
        item
        for item in rooms
        if item["name"] == room
    )

    service_total = sum(
        services[name]
        for name in (selected_services or [])
        if name in services
    )

    total = (
        room_data["price"] * nights
        + service_total
    )

    booking_id = (
        f"GP{len(bookings) + 1:04d}"
    )

    bookings.append(
        {
            "id": booking_id,
            "owner": owner,
            "phone": phone,
            "pet": pet,
            "pet_type": ptype,
            "checkin": checkin,
            "checkout": checkout,
            "room": room,
            "services": selected_services or [],
            "total": total,
            "status": "รอยืนยัน"
        }
    )

    user_data["name"] = owner
    user_data["phone"] = phone

    if pet not in user_data["pets"]:
        user_data["pets"].append(pet)

    return (
        "# ✅ จองสำเร็จ!\n\n"
        f"**หมายเลขการจอง:** `{booking_id}`\n\n"
        f"🐾 **สัตว์เลี้ยง:** {pet}\n\n"
        f"🏠 **ห้อง:** {room}\n\n"
        f"📅 **วันที่:** {checkin} → {checkout}\n\n"
        f"💰 **ยอดรวม:** {total:,} บาท\n\n"
        "🟡 **สถานะ:** รอยืนยัน"
    )


# =========================================================
# การจองของฉัน
# =========================================================

def my_bookings():

    if not bookings:

        return (
            "# 📋 การจองของฉัน\n\n"
            "ยังไม่มีรายการจอง"
        )

    text = "# 📋 การจองของฉัน\n\n"

    for booking in bookings:

        text += (
            f"## 🐾 {booking['id']}\n"
            f"**สัตว์เลี้ยง:** {booking['pet']}\n\n"
            f"**ห้อง:** {booking['room']}\n\n"
            f"**วันที่:** "
            f"{booking['checkin']} → "
            f"{booking['checkout']}\n\n"
            f"**ราคา:** "
            f"{booking['total']:,} บาท\n\n"
            f"**สถานะ:** {booking['status']}\n\n"
            "---\n"
        )

    return text


# =========================================================
# แจ้งเตือน
# =========================================================

def notifications():

    if not bookings:

        return (
            "# 🔔 แจ้งเตือน\n\n"
            "ยังไม่มีการแจ้งเตือน"
        )

    text = "# 🔔 แจ้งเตือน\n\n"

    for booking in bookings:

        text += (
            f"🔔 **{booking['id']}** — "
            f"{booking['pet']} — "
            f"**{booking['status']}**\n\n"
        )

    return text


# =========================================================
# บัญชีของฉัน
# =========================================================

def account():

    if user_data["pets"]:

        pets = ", ".join(
            user_data["pets"]
        )

    else:

        pets = "ยังไม่มีข้อมูลสัตว์เลี้ยง"

    return (
        "# 👤 บัญชีของฉัน\n\n"
        f"**ชื่อ:** {user_data['name']}\n\n"
        f"**เบอร์โทร:** {user_data['phone']}\n\n"
        f"**อีเมล:** {user_data['email']}\n\n"
        "### 🐾 สัตว์เลี้ยง\n"
        f"{pets}\n\n"
        "### 📋 การจอง\n"
        f"{len(bookings)} รายการ"
    )


# =========================================================
# รายการจองสำหรับเจ้าของร้าน
# =========================================================

def owner_list():

    if not bookings:

        return (
            "# 📋 รายการจอง\n\n"
            "ยังไม่มีรายการจองจากลูกค้า"
        )

    text = "# 📋 รายการจอง Grand Paws\n\n"

    for booking in bookings:

        text += (
            f"## 🐾 {booking['id']}\n"
            f"👤 **เจ้าของ:** {booking['owner']}\n\n"
            f"📞 **โทร:** {booking['phone']}\n\n"
            f"🐾 **สัตว์เลี้ยง:** "
            f"{booking['pet']} "
            f"({booking['pet_type']})\n\n"
            f"🏠 **ห้อง:** {booking['room']}\n\n"
            f"📅 **วันที่:** "
            f"{booking['checkin']} → "
            f"{booking['checkout']}\n\n"
            f"💰 **ราคา:** "
            f"{booking['total']:,} บาท\n\n"
            f"**สถานะ:** {booking['status']}\n\n"
            "---\n"
        )

    return text


# =========================================================
# ยืนยันการจอง
# =========================================================

def approve(booking_id):

    booking_id = (
        booking_id or ""
    ).strip().upper()

    for booking in bookings:

        if booking["id"].upper() == booking_id:

            booking["status"] = "ยืนยันแล้ว"

            return (
                "# ✅ ยืนยันการจองสำเร็จ\n\n"
                f"**{booking_id}** 🟢 ยืนยันแล้ว"
            )

    return (
        f"❌ ไม่พบหมายเลขการจอง "
        f"**{booking_id}**"
    )


# =========================================================
# ปฏิเสธการจอง
# =========================================================

def reject(booking_id):

    booking_id = (
        booking_id or ""
    ).strip().upper()

    for booking in bookings:

        if booking["id"].upper() == booking_id:

            booking["status"] = "ปฏิเสธ"

            return (
                "# ❌ ปฏิเสธการจอง\n\n"
                f"**{booking_id}** 🔴 ปฏิเสธแล้ว"
            )

    return (
        f"❌ ไม่พบหมายเลขการจอง "
        f"**{booking_id}**"
    )


# =========================================================
# CSS
# =========================================================

css = """
body {
    background: #f7eee3;
}

.gradio-container {
    max-width: 1200px !important;
    background: #fffaf4;
}

h1, h2, h3 {
    color: #654321 !important;
}

button {
    border-radius: 15px !important;
}

.welcome {
    text-align: center;
    background: linear-gradient(
        135deg,
        #fff4df,
        #f5dfc2
    );
    padding: 30px;
    border-radius: 30px;
    border: 2px solid #ead0ad;
    margin-bottom: 20px;
}

.menu {
    min-height: 110px !important;
    font-size: 18px !important;
    font-weight: bold !important;
}

.dev {
    text-align: center;
    background: #fff4df;
    padding: 18px;
    border-radius: 20px;
    margin-top: 20px;
}
"""


# =========================================================
# สร้างแอป
# =========================================================

with gr.Blocks(
    title="Grand Paws - Pet Hotel",
    css=css,
    theme=gr.themes.Soft()
) as app:

    gr.HTML(
        """
        <div class='welcome'>
            <h1>🐾 Grand Paws</h1>
            <h3>PET HOTEL & CARE</h3>
        </div>
        """
    )


    # =====================================================
    # เลือกประเภทการใช้งาน
    # =====================================================

    with gr.Column(visible=True) as role:

        gr.HTML(home())

        gr.Markdown(
            "## 🐾 เลือกประเภทการใช้งาน"
        )

        with gr.Row():

            customer_btn = gr.Button(
                "🐱 ระบบลูกค้า\nจองห้องพักและดูข้อมูล",
                elem_classes="menu"
            )

            owner_btn = gr.Button(
                "🔐 เจ้าของร้าน\nจัดการการจอง",
                elem_classes="menu"
            )

        gr.HTML(
            """
            <div class='dev'>
                <h3>👩‍💻 ผู้พัฒนา</h3>
                <p>นางสาวจุฑาทิพย์ สุวรรณกาจน์</p>
                <p>นางสาวพิชามญชุ์ อักษรกูล</p>
                <p>นางสาวภัทรภร ศรีจำรัส</p>
            </div>
            """
        )


    # =====================================================
    # ระบบลูกค้า
    # =====================================================

    with gr.Column(visible=False) as customer:

        gr.Markdown("# 🐾 ระบบลูกค้า")


        with gr.Column(visible=True) as chome:

            gr.HTML(home())

            with gr.Row():

                bbook = gr.Button(
                    "1 🐾 จองห้องพัก",
                    elem_classes="menu"
                )

                brooms = gr.Button(
                    "2 🏠 ดูห้องพัก",
                    elem_classes="menu"
                )

                bservices = gr.Button(
                    "3 🛁 บริการเสริม",
                    elem_classes="menu"
                )

            with gr.Row():

                bmy = gr.Button(
                    "4 📋 การจองของฉัน",
                    elem_classes="menu"
                )

                bnot = gr.Button(
                    "5 🔔 แจ้งเตือน",
                    elem_classes="menu"
                )

                bacc = gr.Button(
                    "6 👤 บัญชีของฉัน",
                    elem_classes="menu"
                )

            back_c = gr.Button(
                "⬅️ กลับไปเลือกประเภท"
            )


        # =================================================
        # จองห้อง
        # =================================================

        with gr.Column(visible=False) as book:

            gr.Markdown("# 🐾 จองห้องพัก")

            owner = gr.Textbox(
                label="ชื่อเจ้าของ"
            )

            phone = gr.Textbox(
                label="เบอร์โทรศัพท์"
            )

            pet = gr.Textbox(
                label="ชื่อสัตว์เลี้ยง"
            )

            ptype = gr.Radio(
                ["🐶 สุนัข", "🐱 แมว"],
                label="ประเภทสัตว์เลี้ยง"
            )

            with gr.Row():

                ci = gr.Textbox(
                    label="วันที่เข้าพัก",
                    placeholder="YYYY-MM-DD"
                )

                co = gr.Textbox(
                    label="วันที่ออก",
                    placeholder="YYYY-MM-DD"
                )

            roomc = gr.Dropdown(
                [room["name"] for room in rooms],
                label="เลือกห้องพัก"
            )

            svc = gr.CheckboxGroup(
                list(services.keys()),
                label="บริการเสริม"
            )

            with gr.Row():

                calcbtn = gr.Button(
                    "💰 คำนวณราคา"
                )

                confirmbtn = gr.Button(
                    "✅ ยืนยันการจอง",
                    variant="primary"
                )

            result = gr.Markdown()

            back_book = gr.Button(
                "⬅️ กลับระบบลูกค้า"
            )


        # =================================================
        # ห้องพัก
        # =================================================

        with gr.Column(visible=False) as rp:

            rout = gr.Markdown(
                show_rooms()
            )

            back_r = gr.Button(
                "⬅️ กลับระบบลูกค้า"
            )


        # =================================================
        # บริการ
        # =================================================

        with gr.Column(visible=False) as sp:

            sout = gr.Markdown(
                show_services()
            )

            back_s = gr.Button(
                "⬅️ กลับระบบลูกค้า"
            )


        # =================================================
        # การจองของฉัน
        # =================================================

        with gr.Column(visible=False) as mp:

            mout = gr.Markdown()

            ref_m = gr.Button(
                "🔄 อัปเดต"
            )

            back_m = gr.Button(
                "⬅️ กลับระบบลูกค้า"
            )


        # =================================================
        # แจ้งเตือน
        # =================================================

        with gr.Column(visible=False) as np:

            nout = gr.Markdown()

            ref_n = gr.Button(
                "🔄 อัปเดต"
            )

            back_n = gr.Button(
                "⬅️ กลับระบบลูกค้า"
            )


        # =================================================
        # บัญชี
        # =================================================

        with gr.Column(visible=False) as ap:

            aout = gr.Markdown(
                account()
            )

            ref_a = gr.Button(
                "🔄 อัปเดต"
            )

            back_a = gr.Button(
                "⬅️ กลับระบบลูกค้า"
            )


        # =================================================
        # ระบบเปลี่ยนหน้า
        # =================================================

        customer_pages = [
            chome,
            book,
            rp,
            sp,
            mp,
            np,
            ap
        ]


        def change_customer_page(index):

            return tuple(
                gr.update(
                    visible=(i == index)
                )
                for i in range(7)
            )


        bbook.click(
            lambda: change_customer_page(1),
            outputs=customer_pages
        )

        brooms.click(
            lambda: change_customer_page(2),
            outputs=customer_pages
        )

        bservices.click(
            lambda: change_customer_page(3),
            outputs=customer_pages
        )

        bmy.click(
            lambda: change_customer_page(4),
            outputs=customer_pages
        )

        bnot.click(
            lambda: change_customer_page(5),
            outputs=customer_pages
        )

        bacc.click(
            lambda: change_customer_page(6),
            outputs=customer_pages
        )


        for button in [
            back_book,
            back_r,
            back_s,
            back_m,
            back_n,
            back_a
        ]:

            button.click(
                lambda: change_customer_page(0),
                outputs=customer_pages
            )


        # =================================================
        # ปุ่มคำนวณและยืนยัน
        # =================================================

        calcbtn.click(
            calc,
            inputs=[
                owner,
                phone,
                pet,
                ptype,
                ci,
                co,
                roomc,
                svc
            ],
            outputs=result
        )


        confirmbtn.click(
            confirm,
            inputs=[
                owner,
                phone,
                pet,
                ptype,
                ci,
                co,
                roomc,
                svc
            ],
            outputs=result
        )


        ref_m.click(
            my_bookings,
            outputs=mout
        )

        ref_n.click(
            notifications,
            outputs=nout
        )

        ref_a.click(
            account,
            outputs=aout
        )


    # =====================================================
    # ระบบเจ้าของร้าน
    # =====================================================

    with gr.Column(visible=False) as ownerpg:

        gr.Markdown(
            "# 🔐 ระบบเจ้าของร้าน"
        )


        with gr.Tabs():

            # =============================================
            # สร้างบัญชี
            # =============================================

            with gr.Tab("📝 สร้างบัญชี"):

                oname = gr.Textbox(
                    label="ชื่อเจ้าของร้าน"
                )

                ouser = gr.Textbox(
                    label="ชื่อผู้ใช้"
                )

                opass = gr.Textbox(
                    label="รหัสผ่าน",
                    type="password"
                )

                oc = gr.Textbox(
                    label="ยืนยันรหัสผ่าน",
                    type="password"
                )

                cb = gr.Button(
                    "✅ สร้างบัญชี"
                )

                cr = gr.Markdown()

                cb.click(
                    create_owner,
                    inputs=[
                        oname,
                        ouser,
                        opass,
                        oc
                    ],
                    outputs=cr
                )


            # =============================================
            # เข้าสู่ระบบ
            # =============================================

            with gr.Tab("🔐 เข้าสู่ระบบ"):

                lu = gr.Textbox(
                    label="ชื่อผู้ใช้"
                )

                lp = gr.Textbox(
                    label="รหัสผ่าน",
                    type="password"
                )

                lb = gr.Button(
                    "🔐 เข้าสู่ระบบ"
                )

                lr = gr.Markdown()

                lb.click(
                    owner_login,
                    inputs=[
                        lu,
                        lp
                    ],
                    outputs=lr
                )


            # =============================================
            # รายการจอง
            # =============================================

            with gr.Tab("📋 รายการจอง"):

                ol = gr.Markdown(
                    owner_list()
                )

                ref_o = gr.Button(
                    "🔄 รีเฟรช"
                )

                ref_o.click(
                    owner_list,
                    outputs=ol
                )


            # =============================================
            # จัดการการจอง
            # =============================================

            with gr.Tab("📝 จัดการการจอง"):

                bid = gr.Textbox(
                    label="หมายเลขการจอง",
                    placeholder="เช่น GP0001"
                )

                with gr.Row():

                    ab = gr.Button(
                        "✅ ยืนยันการจอง",
                        variant="primary"
                    )

                    rb = gr.Button(
                        "❌ ปฏิเสธการจอง"
                    )

                ar = gr.Markdown()


                ab.click(
                    approve,
                    inputs=bid,
                    outputs=ar
                )

                rb.click(
                    reject,
                    inputs=bid,
                    outputs=ar
                )

                ab.click(
                    owner_list,
                    outputs=ol
                )

                rb.click(
                    owner_list,
                    outputs=ol
                )


        back_o = gr.Button(
            "⬅️ กลับไปเลือกประเภท"
        )


    # =====================================================
    # เปลี่ยนจากหน้าเลือกประเภท
    # =====================================================

    customer_btn.click(
        lambda: (
            gr.update(visible=False),
            gr.update(visible=True),
            gr.update(visible=False)
        ),
        outputs=[
            role,
            customer,
            ownerpg
        ]
    )


    owner_btn.click(
        lambda: (
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=True)
        ),
        outputs=[
            role,
            customer,
            ownerpg
        ]
    )


    back_c.click(
        lambda: (
            gr.update(visible=True),
            gr.update(visible=False),
            gr.update(visible=False)
        ),
        outputs=[
            role,
            customer,
            ownerpg
        ]
    )


    back_o.click(
        lambda: (
            gr.update(visible=True),
            gr.update(visible=False),
            gr.update(visible=False)
        ),
        outputs=[
            role,
            customer,
            ownerpg
        ]
    )


# =========================================================
# เปิดเว็บไซต์
# =========================================================

app.launch(
    server_name="0.0.0.0",
    server_port=int(
        os.environ.get("PORT", 7860)
    )
)
