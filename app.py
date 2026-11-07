
import streamlit as st

st.set_page_config(page_title="쉬운 키오스크", page_icon="🩵", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;600;700;800&display=swap');
* {font-family:'Noto Sans KR',sans-serif;}
.stApp {background:#F2F8FE;}
.block-container {max-width:1100px;padding-top:2rem;}
h1,h2,h3 {color:#294766;}
p,label {font-size:19px;}
.stButton>button {
    width:100%; min-height:65px; border-radius:15px;
    background:white; border:2px solid #B8D8F2;
    color:#315A7D; font-size:20px; font-weight:700;
}
.stButton>button:hover {background:#DCEEFF;color:#244B70;}
[data-testid="stVerticalBlockBorderWrapper"] {
    background:white;border-radius:18px;border-color:#D6E8F8;
}
</style>
""", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "home"
if "store" not in st.session_state:
    st.session_state.store = ""
if "cart" not in st.session_state:
    st.session_state.cart = []
if "selected" not in st.session_state:
    st.session_state.selected = ""
if "guide" not in st.session_state:
    st.session_state.guide = False
if "payment" not in st.session_state:
    st.session_state.payment = ""

stores = {
    "🍔 햄버거": {
        "name":"행복버거",
        "menus":{"치즈버거":4500,"불고기버거":5000,"감자튀김":2500,"콜라":2000,"치킨너겟":3000}
    },
    "☕ 카페": {
        "name":"따뜻한 카페",
        "menus":{"아메리카노":3000,"카페라떼":4000,"바닐라라떼":4500,"녹차라떼":4500,"딸기주스":5000}
    },
    "🍜 분식점": {
        "name":"맛있는 분식",
        "menus":{"떡볶이":4000,"김밥":3500,"라면":4000,"순대":4500,"튀김":3500}
    }
}

guides = {
    "home":("체험 시작하기","원하는 매장을 선택해 주세요. 햄버거 가게, 카페, 분식점의 키오스크 주문 과정을 직접 체험할 수 있습니다. 실제 결제는 발생하지 않습니다."),
    "menu":("메뉴 선택하기","원하는 음식이나 음료를 선택하는 화면입니다. 메뉴 이름과 가격을 확인한 뒤 선택 버튼을 눌러주세요."),
    "option":("수량과 옵션 선택하기","주문할 음식의 개수와 옵션을 선택하는 화면입니다. 선택을 마치면 장바구니에 담아주세요."),
    "cart":("장바구니 확인하기","내가 선택한 음식들이 모여 있는 공간입니다. 메뉴와 수량, 총금액을 확인하고 결제하기를 누르세요."),
    "payment":("결제 방법 선택하기","카드, 현금, 간편결제 중 원하는 방법을 선택하는 화면입니다. 교육용 가상 체험이므로 실제 돈은 결제되지 않습니다."),
    "done":("주문 완료하기","주문이 완료되었습니다! 주문 내역과 금액을 확인할 수 있습니다. 처음으로 돌아가 다른 매장도 체험해 보세요.")
}

def move(page):
    st.session_state.page = page
    st.session_state.guide = False
    st.rerun()

def total():
    return sum(x["price"]*x["qty"] for x in st.session_state.cart)

def help_button():
    st.divider()
    _, right = st.columns([4,2])
    with right:
        if not st.session_state.guide:
            if st.button("💡 설명 보기"):
                st.session_state.guide = True
                st.rerun()
        else:
            if st.button("✖ 설명 닫기"):
                st.session_state.guide = False
                st.rerun()

    if st.session_state.guide:
        title, desc = guides[st.session_state.page]
        st.markdown(f"""
        <div style="background:#DDEEFF;border:2px solid #9BC9ED;
        border-radius:18px;padding:25px;margin-top:10px;">
        <h2>💡 {title}</h2>
        <p style="font-size:21px;line-height:2;">{desc}</p>
        </div>
        """,unsafe_allow_html=True)

st.markdown("""
<div style="background:linear-gradient(120deg,#D5EBFC,#F0F8FF);
padding:28px;border-radius:22px;margin-bottom:25px;">
<div style="color:#6097C2;font-weight:bold;">SENIOR DIGITAL EXPERIENCE</div>
<div style="font-size:38px;font-weight:800;color:#294766;">🩵 쉬운 키오스크</div>
<div style="font-size:19px;color:#55738E;">천천히 눌러보세요. 누구나 쉽게 배울 수 있습니다.</div>
</div>
""",unsafe_allow_html=True)

pages = ["home","menu","option","cart","payment","done"]
labels = ["매장 선택","메뉴 선택","옵션 선택","장바구니","결제","완료"]
idx = pages.index(st.session_state.page)
st.markdown("　 →　".join(
    f"<span style='color:{'#348BC8' if i<=idx else '#AABAC9'};font-weight:bold'>{v}</span>"
    for i,v in enumerate(labels)
),unsafe_allow_html=True)
st.divider()

if st.session_state.page == "home":
    st.title("어떤 매장을 체험해 볼까요?")
    st.write("원하는 매장을 선택해 주세요.")
    cols = st.columns(3)
    for i,(store,data) in enumerate(stores.items()):
        with cols[i]:
            with st.container(border=True):
                st.markdown(f"<div style='text-align:center;padding:20px;font-size:27px;font-weight:bold;color:#315A7D'>{store}<br><br>{data['name']}</div>",unsafe_allow_html=True)
                if st.button("체험 시작하기",key=f"store{i}"):
                    st.session_state.store=store
                    st.session_state.cart=[]
                    move("menu")

elif st.session_state.page == "menu":
    st.title(f"🍽️ {stores[st.session_state.store]['name']}")
    st.subheader("원하는 메뉴를 선택해 주세요.")
    menus = stores[st.session_state.store]["menus"]
    cols = st.columns(3)
    emojis = ["🍔","🍟","🥤","🍗","🍰","🍜"]
    for i,(name,price) in enumerate(menus.items()):
        with cols[i%3]:
            with st.container(border=True):
                st.markdown(f"""
                <div style="text-align:center;padding:15px;">
                <div style="font-size:45px">{emojis[i%6]}</div>
                <div style="font-size:23px;font-weight:bold;color:#315A7D">{name}</div>
                <div style="font-size:21px;color:#559BD1">{price:,}원</div>
                </div>""",unsafe_allow_html=True)
                if st.button("선택하기",key=f"menu{i}"):
                    st.session_state.selected=name
                    st.session_state.price=price
                    st.session_state.qty=1
                    move("option")
    if st.button("🛒 장바구니 확인"):
        move("cart")

elif st.session_state.page == "option":
    st.title("🥤 옵션 선택")
    st.header(st.session_state.selected)
    st.write(f"가격: {st.session_state.price:,}원")
    st.session_state.qty=st.number_input("주문 수량",1,10,1)
    option=""
    if st.session_state.store=="☕ 카페":
        option=st.radio("음료 온도",["따뜻하게","차갑게"],horizontal=True)
    st.metric("예상 금액",f"{st.session_state.price*st.session_state.qty:,}원")
    c1,c2=st.columns(2)
    with c1:
        if st.button("🛒 장바구니에 담기"):
            st.session_state.cart.append({
                "name":st.session_state.selected,
                "price":st.session_state.price,
                "qty":st.session_state.qty,
                "option":option
            })
            move("cart")
    with c2:
        if st.button("← 메뉴로 돌아가기"):
            move("menu")

elif st.session_state.page == "cart":
    st.title("🛒 장바구니")
    if not st.session_state.cart:
        st.info("선택한 메뉴가 없습니다.")
        if st.button("메뉴 선택하기"):
            move("menu")
    else:
        for i,item in enumerate(st.session_state.cart):
            with st.container(border=True):
                c1,c2=st.columns([4,1])
                c1.subheader(item["name"])
                c1.write(f"{item['qty']}개 · {item['price']*item['qty']:,}원")
                if item["option"]:
                    c1.caption(item["option"])
                if c2.button("삭제",key=f"del{i}"):
                    st.session_state.cart.pop(i)
                    st.rerun()
        st.metric("총 결제 금액",f"{total():,}원")
        a,b=st.columns(2)
        with a:
            if st.button("➕ 메뉴 더 고르기"):
                move("menu")
        with b:
            if st.button("결제하기 →"):
                move("payment")

elif st.session_state.page == "payment":
    st.title("💳 결제 방법 선택")
    st.info("교육용 가상 결제입니다. 실제 결제는 발생하지 않습니다.")
    st.session_state.payment=st.radio(
        "결제 방법",["💳 신용카드","💵 현금","📱 간편결제"]
    )
    st.metric("결제 예정 금액",f"{total():,}원")
    a,b=st.columns(2)
    with a:
        if st.button("← 돌아가기"):
            move("cart")
    with b:
        if st.button("결제 연습하기",type="primary"):
            move("done")

elif st.session_state.page == "done":
    st.markdown("""
    <div style="background:#DDEEFF;padding:40px;border-radius:22px;text-align:center;">
    <div style="font-size:70px;">🎉</div>
    <h1>주문 체험 완료!</h1>
    <p style="font-size:22px;">정말 잘하셨습니다!</p>
    </div>
    """,unsafe_allow_html=True)
    st.subheader("주문 내역")
    for item in st.session_state.cart:
        st.write(f"• {item['name']} {item['qty']}개 — {item['price']*item['qty']:,}원")
    st.metric("총 주문 금액",f"{total():,}원")
    st.success(f"결제 방법: {st.session_state.payment}")
    st.info("실제 결제는 이루어지지 않았습니다.")
    if st.button("🔄 처음부터 다시 체험하기",type="primary"):
        st.session_state.cart=[]
        st.session_state.payment=""
        move("home")

# 오른쪽 아래 설명 버튼 및 설명창
help_button()

# 처음으로 돌아가기
if st.session_state.page != "home":
    st.divider()
    if st.button("🏠 처음 화면으로"):
        st.session_state.cart=[]
        move("home")
