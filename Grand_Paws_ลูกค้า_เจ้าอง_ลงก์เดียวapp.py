# GRAND PAWS PET HOTEL - ลูกค้า + เจ้าของร้านในลิงก์เดียว
!pip -q install gradio

import os, json, hashlib
import gradio as gr
from datetime import datetime

rooms = [
    {"name":"Standard Room","price":850,"description":"ห้องพักมาตรฐาน เหมาะสำหรับสัตว์เลี้ยง 1 ตัว","status":"ว่าง"},
    {"name":"Deluxe Room","price":1000,"description":"ห้องกว้างขึ้น พร้อมพื้นที่พักผ่อนสำหรับสัตว์เลี้ยง","status":"ว่าง"},
    {"name":"Grand Suite","price":1200,"description":"ห้องพิเศษ พื้นที่กว้าง พร้อมการดูแลเพิ่มเติม","status":"ว่าง"}
]
services = {"อาบน้ำ":200,"ตัดขน":300,"พาเดินเล่น":100,"ให้อาหารพิเศษ":100,"ดูแลเพิ่มเติม":250}
bookings = []
user_data = {"name":"ผู้ใช้ Grand Paws","phone":"-","email":"-","pets":[]}

DATA_FOLDER="/content/Grand_Paws"
OWNER_FILE=os.path.join(DATA_FOLDER,"owner.json")
os.makedirs(DATA_FOLDER,exist_ok=True)

def hash_password(p): return hashlib.sha256(p.encode("utf-8")).hexdigest()

def create_owner(name,username,password,confirm):
    if not name: return "⚠️ กรุณากรอกชื่อเจ้าของร้าน"
    if not username: return "⚠️ กรุณากรอกชื่อผู้ใช้"
    if not password: return "⚠️ กรุณากรอกรหัสผ่าน"
    if password != confirm: return "⚠️ รหัสผ่านไม่ตรงกัน"
    if len(password)<6: return "⚠️ รหัสผ่านควรมีอย่างน้อย 6 ตัวอักษร"
    if os.path.exists(OWNER_FILE): return "⚠️ มีบัญชีเจ้าของร้านอยู่แล้ว กรุณาเข้าสู่ระบบ"
    with open(OWNER_FILE,"w",encoding="utf-8") as f:
        json.dump({"name":name,"username":username,"password":hash_password(password)},f,ensure_ascii=False,indent=2)
    return f"# ✅ สร้างบัญชีสำเร็จ\nยินดีต้อนรับ **{name}**\n\nชื่อผู้ใช้: **{username}**"

def owner_login(username,password):
    if not os.path.exists(OWNER_FILE): return "⚠️ ยังไม่มีบัญชีเจ้าของร้าน กรุณาสร้างบัญชีก่อน"
    with open(OWNER_FILE,"r",encoding="utf-8") as f: o=json.load(f)
    if username==o["username"] and hash_password(password)==o["password"]:
        return f"# 🟢 เข้าสู่ระบบสำเร็จ\nยินดีต้อนรับ **{o['name']}** 🐾"
    return "# 🔴 เข้าสู่ระบบไม่สำเร็จ\nชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง"

def home():
    return """<div class="welcome"><h1>🐾 Grand Paws</h1><h3>PET HOTEL & CARE</h3>
    <h2>ยินดีต้อนรับสู่ Grand Paws</h2><p>ดูแลสัตว์เลี้ยงของคุณด้วยความรัก เหมือนอยู่บ้าน ❤️</p></div>"""

def show_rooms():
    s="# 🏠 ห้องพัก Grand Paws\n\n"
    for r in rooms:
        s+=f"### 🐾 {r['name']}\n**ราคา:** {r['price']:,} บาท / คืน\n\n{r['description']}\n\nสถานะ: 🟢 **{r['status']}**\n\n---\n"
    return s

def show_services():
    return "# 🛁 บริการเสริม\n\n"+"".join(f"### 🐾 {n}\nราคา **{p:,} บาท**\n\n" for n,p in services.items())

def calc(owner,phone,pet,ptype,ci,co,room,ss):
    if not owner or not phone or not pet or not ptype: return "⚠️ กรุณากรอกข้อมูลให้ครบ"
    if not ci or not co: return "⚠️ กรุณาเลือกวันที่เข้าพักและวันที่ออก"
    try: nights=(datetime.strptime(co,"%Y-%m-%d")-datetime.strptime(ci,"%Y-%m-%d")).days
    except: return "⚠️ วันที่ต้องเป็นรูปแบบ YYYY-MM-DD"
    if nights<=0: return "⚠️ วันที่ออกต้องหลังวันที่เข้าพัก"
    r=next((x for x in rooms if x["name"]==room),None)
    if not r: return "⚠️ กรุณาเลือกห้องพัก"
    rt=r["price"]*nights; st=sum(services[x] for x in (ss or [])); total=rt+st
    return f"## 🧾 สรุปการจอง\n**เจ้าของ:** {owner}\n\n**เบอร์โทร:** {phone}\n\n**สัตว์เลี้ยง:** {pet} ({ptype})\n\n**ห้อง:** {room}\n\n**วันที่:** {ci} → {co}\n\n**จำนวน:** {nights} คืน\n\n**ค่าห้อง:** {rt:,} บาท\n\n**บริการเสริม:** {st:,} บาท\n\n# 💰 รวม {total:,} บาท\n\nกด **ยืนยันการจอง** เพื่อส่งรายการให้เจ้าของร้าน"

def confirm(owner,phone,pet,ptype,ci,co,room,ss):
    result=calc(owner,phone,pet,ptype,ci,co,room,ss)
    if result.startswith("⚠️"): return result
    nights=(datetime.strptime(co,"%Y-%m-%d")-datetime.strptime(ci,"%Y-%m-%d")).days
    r=next(x for x in rooms if x["name"]==room)
    total=r["price"]*nights+sum(services[x] for x in (ss or []))
    bid=f"GP{len(bookings)+1:04d}"
    bookings.append({"id":bid,"owner":owner,"phone":phone,"pet":pet,"pet_type":ptype,"checkin":ci,"checkout":co,"room":room,"services":ss or [],"total":total,"status":"รอยืนยัน"})
    user_data["name"]=owner; user_data["phone"]=phone
    if pet not in user_data["pets"]: user_data["pets"].append(pet)
    return f"# ✅ จองสำเร็จ!\n\n**หมายเลขการจอง:** `{bid}`\n\n🐾 **สัตว์เลี้ยง:** {pet}\n\n🏠 **ห้อง:** {room}\n\n📅 **วันที่:** {ci} → {co}\n\n💰 **ยอดรวม:** {total:,} บาท\n\n🟡 **สถานะ:** รอยืนยัน"

def my_bookings():
    if not bookings: return "# 📋 การจองของฉัน\n\nยังไม่มีรายการจอง"
    return "# 📋 การจองของฉัน\n\n"+"".join(f"## 🐾 {b['id']}\n**สัตว์เลี้ยง:** {b['pet']}\n\n**ห้อง:** {b['room']}\n\n**วันที่:** {b['checkin']} → {b['checkout']}\n\n**ราคา:** {b['total']:,} บาท\n\n**สถานะ:** {b['status']}\n\n---\n" for b in bookings)

def notifications():
    if not bookings: return "# 🔔 แจ้งเตือน\n\nยังไม่มีการแจ้งเตือน"
    return "# 🔔 แจ้งเตือน\n\n"+"".join(f"🔔 **{b['id']}** — {b['pet']} — **{b['status']}**\n\n" for b in bookings)

def account():
    pets=", ".join(user_data["pets"]) if user_data["pets"] else "ยังไม่มีข้อมูลสัตว์เลี้ยง"
    return f"# 👤 บัญชีของฉัน\n\n**ชื่อ:** {user_data['name']}\n\n**เบอร์โทร:** {user_data['phone']}\n\n**อีเมล:** {user_data['email']}\n\n### 🐾 สัตว์เลี้ยง\n{pets}\n\n### 📋 การจอง\n{len(bookings)} รายการ"

def owner_list():
    if not bookings: return "# 📋 รายการจอง\n\nยังไม่มีรายการจองจากลูกค้า"
    return "# 📋 รายการจอง Grand Paws\n\n"+"".join(f"## 🐾 {b['id']}\n👤 **เจ้าของ:** {b['owner']}\n\n📞 **โทร:** {b['phone']}\n\n🐾 **สัตว์เลี้ยง:** {b['pet']} ({b['pet_type']})\n\n🏠 **ห้อง:** {b['room']}\n\n📅 **วันที่:** {b['checkin']} → {b['checkout']}\n\n💰 **ราคา:** {b['total']:,} บาท\n\n**สถานะ:** {b['status']}\n\n---\n" for b in bookings)

def approve(bid):
    bid=(bid or "").strip().upper()
    for b in bookings:
        if b["id"].upper()==bid:
            b["status"]="ยืนยันแล้ว"; return f"# ✅ ยืนยันการจองสำเร็จ\n\n**{bid}** 🟢 ยืนยันแล้ว"
    return f"❌ ไม่พบหมายเลขการจอง **{bid}**"

def reject(bid):
    bid=(bid or "").strip().upper()
    for b in bookings:
        if b["id"].upper()==bid:
            b["status"]="ปฏิเสธ"; return f"# ❌ ปฏิเสธการจอง\n\n**{bid}** 🔴 ปฏิเสธแล้ว"
    return f"❌ ไม่พบหมายเลขการจอง **{bid}**"

css="""body{background:#f7eee3}.gradio-container{max-width:1200px!important;background:#fffaf4}h1,h2,h3{color:#654321!important}button{border-radius:15px!important}.welcome{text-align:center;background:linear-gradient(135deg,#fff4df,#f5dfc2);padding:30px;border-radius:30px;border:2px solid #ead0ad;margin-bottom:20px}.menu{min-height:110px!important;font-size:18px!important;font-weight:bold!important}.dev{text-align:center;background:#fff4df;padding:18px;border-radius:20px;margin-top:20px}"""

with gr.Blocks(title="Grand Paws - Pet Hotel",css=css,theme=gr.themes.Soft()) as app:
    gr.HTML("<div class='welcome'><h1>🐾 Grand Paws</h1><h3>PET HOTEL & CARE</h3></div>")
    with gr.Column(visible=True) as role:
        gr.HTML(home())
        gr.Markdown("## 🐾 เลือกประเภทการใช้งาน")
        with gr.Row():
            customer_btn=gr.Button("🐱 ระบบลูกค้า\nจองห้องพักและดูข้อมูล",elem_classes="menu")
            owner_btn=gr.Button("🔐 เจ้าของร้าน\nจัดการการจอง",elem_classes="menu")
        gr.HTML("<div class='dev'><h3>👩‍💻 ผู้พัฒนา</h3><p>นางสาวจุฑาทิพย์ สุวรรณกาจน์</p><p>นางสาวพิชามญชุ์ อักษรกูล</p><p>นางสาวภัทรภร ศรีจำรัส</p></div>")

    with gr.Column(visible=False) as customer:
        gr.Markdown("# 🐾 ระบบลูกค้า")
        with gr.Column(visible=True) as chome:
            gr.HTML(home())
            with gr.Row():
                bbook=gr.Button("1 🐾 จองห้องพัก",elem_classes="menu"); brooms=gr.Button("2 🏠 ดูห้องพัก",elem_classes="menu"); bservices=gr.Button("3 🛁 บริการเสริม",elem_classes="menu")
            with gr.Row():
                bmy=gr.Button("4 📋 การจองของฉัน",elem_classes="menu"); bnot=gr.Button("5 🔔 แจ้งเตือน",elem_classes="menu"); bacc=gr.Button("6 👤 บัญชีของฉัน",elem_classes="menu")
            back_c=gr.Button("⬅️ กลับไปเลือกประเภท")
        with gr.Column(visible=False) as book:
            gr.Markdown("# 🐾 จองห้องพัก")
            owner=gr.Textbox(label="ชื่อเจ้าของ"); phone=gr.Textbox(label="เบอร์โทรศัพท์"); pet=gr.Textbox(label="ชื่อสัตว์เลี้ยง"); ptype=gr.Radio(["🐶 สุนัข","🐱 แมว"],label="ประเภทสัตว์เลี้ยง")
            with gr.Row(): ci=gr.Textbox(label="วันที่เข้าพัก",placeholder="YYYY-MM-DD"); co=gr.Textbox(label="วันที่ออก",placeholder="YYYY-MM-DD")
            roomc=gr.Dropdown([r["name"] for r in rooms],label="เลือกห้องพัก"); svc=gr.CheckboxGroup(list(services.keys()),label="บริการเสริม")
            with gr.Row(): calcbtn=gr.Button("💰 คำนวณราคา"); confirmbtn=gr.Button("✅ ยืนยันการจอง",variant="primary")
            result=gr.Markdown(); back_book=gr.Button("⬅️ กลับระบบลูกค้า")
        with gr.Column(visible=False) as rp: rout=gr.Markdown(show_rooms()); back_r=gr.Button("⬅️ กลับระบบลูกค้า")
        with gr.Column(visible=False) as sp: sout=gr.Markdown(show_services()); back_s=gr.Button("⬅️ กลับระบบลูกค้า")
        with gr.Column(visible=False) as mp: mout=gr.Markdown(); ref_m=gr.Button("🔄 อัปเดต"); back_m=gr.Button("⬅️ กลับระบบลูกค้า")
        with gr.Column(visible=False) as np: nout=gr.Markdown(); ref_n=gr.Button("🔄 อัปเดต"); back_n=gr.Button("⬅️ กลับระบบลูกค้า")
        with gr.Column(visible=False) as ap: aout=gr.Markdown(account()); ref_a=gr.Button("🔄 อัปเดต"); back_a=gr.Button("⬅️ กลับระบบลูกค้า")
        cps=[chome,book,rp,sp,mp,np,ap]
        def cv(i):
            return tuple(gr.update(visible=j==i) for j in range(7))
        bbook.click(lambda:cv(1),outputs=cps); brooms.click(lambda:cv(2),outputs=cps); bservices.click(lambda:cv(3),outputs=cps); bmy.click(lambda:cv(4),outputs=cps); bnot.click(lambda:cv(5),outputs=cps); bacc.click(lambda:cv(6),outputs=cps)
        for x in [back_book,back_r,back_s,back_m,back_n,back_a]: x.click(lambda:cv(0),outputs=cps)
        calcbtn.click(calc,[owner,phone,pet,ptype,ci,co,roomc,svc],result); confirmbtn.click(confirm,[owner,phone,pet,ptype,ci,co,roomc,svc],result)
        ref_m.click(my_bookings,mout); ref_n.click(notifications,nout); ref_a.click(account,aout)

    with gr.Column(visible=False) as ownerpg:
        gr.Markdown("# 🔐 ระบบเจ้าของร้าน")
        with gr.Tabs():
            with gr.Tab("📝 สร้างบัญชี"):
                oname=gr.Textbox(label="ชื่อเจ้าของร้าน"); ouser=gr.Textbox(label="ชื่อผู้ใช้"); opass=gr.Textbox(label="รหัสผ่าน",type="password"); oc=gr.Textbox(label="ยืนยันรหัสผ่าน",type="password"); cb=gr.Button("✅ สร้างบัญชี"); cr=gr.Markdown()
                cb.click(create_owner,[oname,ouser,opass,oc],cr)
            with gr.Tab("🔐 เข้าสู่ระบบ"):
                lu=gr.Textbox(label="ชื่อผู้ใช้"); lp=gr.Textbox(label="รหัสผ่าน",type="password"); lb=gr.Button("🔐 เข้าสู่ระบบ"); lr=gr.Markdown()
                lb.click(owner_login,[lu,lp],lr)
            with gr.Tab("📋 รายการจอง"):
                ol=gr.Markdown(owner_list()); ref_o=gr.Button("🔄 รีเฟรช"); ref_o.click(owner_list,outputs=ol)
            with gr.Tab("📝 จัดการการจอง"):
                bid=gr.Textbox(label="หมายเลขการจอง",placeholder="เช่น GP0001")
                with gr.Row(): ab=gr.Button("✅ ยืนยันการจอง",variant="primary"); rb=gr.Button("❌ ปฏิเสธการจอง")
                ar=gr.Markdown()
                ab.click(approve,bid,ar); rb.click(reject,bid,ar); ab.click(owner_list,outputs=ol); rb.click(owner_list,outputs=ol)
        back_o=gr.Button("⬅️ กลับไปเลือกประเภท")

    customer_btn.click(lambda:(gr.update(visible=False),gr.update(visible=True),gr.update(visible=False)),outputs=[role,customer,ownerpg])
    owner_btn.click(lambda:(gr.update(visible=False),gr.update(visible=False),gr.update(visible=True)),outputs=[role,customer,ownerpg])
    back_c.click(lambda:(gr.update(visible=True),gr.update(visible=False),gr.update(visible=False)),outputs=[role,customer,ownerpg])
    back_o.click(lambda:(gr.update(visible=True),gr.update(visible=False),gr.update(visible=False)),outputs=[role,customer,ownerpg])

app.launch(share=True)
