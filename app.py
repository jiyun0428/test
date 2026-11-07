
import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="천천히 눌러봐요",
    page_icon="🩵",
    layout="wide"
)

# =========================
# 1. 기본 디자인
# =========================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700;800&display=swap');

* {font-family:'Noto Sans KR',sans-serif;}

.stApp {background:#F1F5F9;}
.block-container {max-width:1250px;padding-top:25px;}

h1,h2,h3 {color:#263B53;}

div.stButton > button {
    width:100%;
    min-height:65px;
    border-radius:12px;
    font-size:19px;
    font-weight:700;
    border:2px solid #D7E4EF;
    background:white;
    color:#263B53;
}

div.stButton > button:hover {
    background:#DCEEFF;
    border-color:#6AADE0;
}

div.stButton > button[kind="primary"] {
    background:#368BCB;
    color:white;
    border:0;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    background:white;
    border-radius:15px;
    border-color:#DFE8F0;
}

.guide {
    background:#E2F1FF;
    border:2px solid #8ABDE5;
    padding:25px;
    border-radius:18px;
    line-height:2;
    font-size:19px;
    color:#263B53;
}

.brand-title {
    font-size:32px;
    font-weight:800;
    margin-bottom:10px;
}

.product {
    text-align:center;
    padding:15px;
    background:white;
    border:1px solid #E4EAF0;
    border-radius:15px;
    min-height:130px;
}

.product-name {
    font-size:21px;
    font-weight:800;
    color:#263B53;
}

.product-price {
    font-size:18px;
    color:#478CC1;
    margin-top:8px;
}

div[data-testid="stMetric"] {
    background:white;
    padding:15px;
    border-radius:14px;
    border:1px solid #E0EAF3;
}
</style>
""", unsafe_allow_html=True)


# =========================
# 2. 브랜드별 메뉴 데이터
# =========================

BRANDS = {
    "맥도날드": {
        "emoji": "🍔",
        "color": "#DA291C",
        "background": "#FFF1E8",
        "categories": {
            "추천 메뉴": {
                "빅맥": 5900,
                "맥스파이시 상하이버거": 5800,
                "1955 버거": 6500,
                "불고기 버거": 3500
            },
            "세트 메뉴": {
                "빅맥 세트": 7900,
                "상하이 세트": 7800,
                "1955 세트": 8500
            },
            "사이드": {
                "후렌치 후라이": 2200,
                "맥너겟 6조각": 3500,
                "치즈스틱": 2500
            },
            "음료": {
                "콜라": 2000,
                "제로콜라": 2000,
                "아메리카노": 2500
            }
        }
    },

    "메가커피": {
        "emoji": "☕",
        "color": "#F5C400",
        "background": "#FFFBE7",
        "categories": {
            "커피": {
                "아메리카노": 2000,
                "카페라떼": 2900,
                "바닐라라떼": 3700,
                "카페모카": 3900
            },
            "논커피": {
                "초코라떼": 3500,
                "녹차라떼": 3500,
                "딸기라떼": 3900
            },
            "에이드": {
                "레몬에이드": 3500,
                "자몽에이드": 3500,
                "청포도에이드": 3500
            },
            "디저트": {
                "허니브레드": 5500,
                "치즈케이크": 4500,
                "쿠키": 2000
            }
        }
    },

    "롯데리아": {
        "emoji": "🍟",
        "color": "#E52B2B",
        "background": "#FFF0F0",
        "categories": {
            "버거": {
                "불고기버거": 4800,
                "새우버거": 4700,
                "한우불고기버거": 8500
            },
            "세트": {
                "불고기버거 세트": 6900,
                "새우버거 세트": 6800,
                "치킨버거 세트": 6500
            },
            "사이드": {
                "양념감자": 2500,
                "치즈스틱": 2500,
                "치킨너겟": 3000
            },
            "음료": {
                "콜라": 2000,
                "사이다": 2000
            }
        }
    }
}


# =========================
# 3. 화면별 쉬운 설명
# =========================

GUIDES = {
    "brand": (
        "매장 선택",
        "반갑습니다! 지금부터 키오스크 사용법을 연습해 보겠습니다.",
        [
            "화면에 보이는 매장 중 원하는 곳을 선택해 주세요.",
            "맥도날드는 햄버거와 감자튀김을 주문하는 곳입니다.",
            "메가커피는 커피와 다양한 음료를 주문하는 곳입니다.",
            "롯데리아는 햄버거와 세트 메뉴를 주문하는 곳입니다.",
            "실제 결제는 이루어지지 않으니 편하게 연습하세요."
        ]
    ),
    "category": (
        "메뉴 종류 선택",
        "이 화면은 먹고 싶은 음식의 종류를 고르는 화면입니다.",
        [
            "위쪽 또는 왼쪽에 있는 메뉴 이름을 살펴보세요.",
            "버거, 커피, 사이드처럼 종류별로 나누어져 있습니다.",
            "원하는 종류를 누르면 해당 메뉴들이 나타납니다.",
            "다른 종류를 눌러도 괜찮습니다. 언제든 다시 선택할 수 있습니다."
        ]
    ),
    "menu": (
        "음식 선택",
        "이 화면에서는 실제로 주문할 음식이나 음료를 고릅니다.",
        [
            "사진이나 메뉴 이름을 보고 먹고 싶은 것을 찾으세요.",
            "메뉴 아래에 표시된 숫자는 가격입니다.",
            "원하는 메뉴를 누르면 상세 선택 화면으로 이동합니다.",
            "잘못 눌러도 괜찮습니다. 장바구니에서 삭제할 수 있습니다."
        ]
    ),
    "option": (
        "상세 옵션 선택",
        "선택한 메뉴의 수량과 추가 옵션을 정하는 단계입니다.",
        [
            "수량은 주문할 음식의 개수입니다.",
            "커피는 따뜻한 음료(HOT)와 차가운 음료(ICE)를 선택할 수 있습니다.",
            "세트 메뉴는 사이드나 음료를 선택할 수 있습니다.",
            "선택이 끝나면 장바구니 담기를 눌러주세요."
        ]
    ),
    "cart": (
        "장바구니 확인",
        "장바구니는 내가 고른 음식들을 모아놓은 곳입니다.",
        [
            "내가 고른 음식이 맞는지 확인하세요.",
            "수량과 가격을 살펴보세요.",
            "잘못 고른 음식은 삭제 버튼으로 지울 수 있습니다.",
            "더 주문하고 싶다면 메뉴 추가를 누르세요.",
            "주문이 모두 끝났다면 결제하기를 눌러주세요."
        ]
    ),
    "payment": (
        "결제 방법 선택",
        "주문한 음식의 값을 어떤 방법으로 낼지 선택하는 화면입니다.",
        [
            "카드 결제는 신용카드나 체크카드를 사용하는 방법입니다.",
            "현금 결제는 지폐나 동전으로 결제하는 방법입니다.",
            "간편결제는 휴대전화 등을 이용하는 방법입니다.",
            "이 앱에서는 실제 돈이 빠져나가지 않습니다.",
            "원하는 결제 방법을 누르고 결제 연습을 진행하세요."
        ]
    ),
    "done": (
        "주문 완료",
        "축하합니다! 키오스크 주문 연습을 성공적으로 마쳤습니다.",
        [
            "주문한 음식과 금액을 확인해 보세요.",
            "실제 매장에서는 주문 번호나 영수증을 확인할 수 있습니다.",
            "처음 화면으로 돌아가 다른 브랜드도 연습해 보세요."
        ]
    )
}


# =========================
# 4. 세션 상태
# =========================

defaults = {
    "page": "brand",
    "brand": "맥도날드",
    "category": "추천 메뉴",
    "cart": [],
    "selected": None,
    "guide_open": False,
    "order_type": "매장에서 먹기",
    "temperature": "ICE",
    "size": "기본",
    "payment": "카드",
    "step": 0
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================
# 5. 공통 함수
# =========================

def go(page):
    st.session_state.page = page
    st.session_state.guide_open = False
    st.rerun()


def total_price():
    return sum(
        item["price"] * item["quantity"]
        for item in st.session_state.cart
    )


def header():
    st.markdown("""
    <div style="background:linear-gradient(120deg,#D8ECFC,#EFF7FF);
    padding:25px;border-radius:20px;margin-bottom:20px;">
    <div style="font-size:15px;color:#5592BF;font-weight:700;">
    SENIOR DIGITAL KIOSK CLASS
    </div>
    <div style="font-size:34px;font-weight:800;color:#294766;">
    🩵 천천히 눌러봐요
    </div>
    <div style="font-size:18px;color:#55738E;">
    실제 매장처럼 연습하는 키오스크 체험 교실
    </div>
    </div>
    """, unsafe_allow_html=True)


def progress():
    labels = [
        ("brand", "매장"),
        ("category", "종류"),
        ("menu", "메뉴"),
        ("option", "옵션"),
        ("cart", "장바구니"),
        ("payment", "결제"),
        ("done", "완료")
    ]

    current = [x[0] for x in labels].index(st.session_state.page)

    cols = st.columns(len(labels))

    for i, (key, label) in enumerate(labels):
        with cols[i]:
            color = "#368BCB" if i <= current else "#B9C5D0"
            st.markdown(
                f"<div style='text-align:center;color:{color};"
                f"font-size:16px;font-weight:800'>{i+1}. {label}</div>",
                unsafe_allow_html=True
            )

    st.divider()


def guide_button():
    st.divider()

    _, right = st.columns([5, 2])

    with right:
        if not st.session_state.guide_open:
            if st.button("💡 설명 보기", type="primary"):
                st.session_state.guide_open = True
                st.rerun()
        else:
            if st.button("✖ 설명 닫기"):
                st.session_state.guide_open = False
                st.rerun()

    if st.session_state.guide_open:
        title, intro, details = GUIDES[st.session_state.page]

        st.markdown(
            f"""
            <div class="guide">
            <h2>💡 {title}</h2>
            <div style="font-size:21px;font-weight:700;">
            {intro}
            </div>
            <hr>
            """,
            unsafe_allow_html=True
        )

        for i, detail in enumerate(details, 1):
            st.markdown(
                f"<div style='font-size:19px;margin:12px 0;'>"
                f"<b>{i}.</b> {detail}</div>",
                unsafe_allow_html=True
            )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )



def brand_top():
    brand = BRANDS[st.session_state.brand]

    st.markdown(
        f"""
        <div style="
            background:{brand['background']};
            padding:20px;
            border-radius:15px;
            border-bottom:5px solid {brand['color']};
        ">
            <div style="
                font-size:30px;
                font-weight:800;
                color:{brand['color']};
            ">
                {brand['emoji']} {st.session_state.brand}
            </div>
            <div style="font-size:17px;color:#555;">
                주문하실 메뉴를 선택해 주세요.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def add_to_cart(name, price, quantity, option=""):
    st.session_state.cart.append({
        "name": name,
        "price": price,
        "quantity": quantity,
        "option": option
    })


def back_button(target):
    if st.button("← 이전 화면으로"):
        go(target)


# =========================
# 6. 맥도날드 주문 방식
# =========================

def mcdonalds_order():

    brand_top()

    if st.session_state.page == "category":

        st.title("무엇을 주문하시겠어요?")

        categories = list(
            BRANDS["맥도날드"]["categories"].keys()
        )

        cols = st.columns(4)

        for i, category in enumerate(categories):
            with cols[i]:
                if st.button(
                    category,
                    key=f"mcd_cat_{i}",
                    type="primary" if st.session_state.category == category else "secondary"
                ):
                    st.session_state.category = category
                    go("menu")

        st.write("")
        if st.button("전체 메뉴 보기"):
            st.session_state.category = "추천 메뉴"
            go("menu")

    elif st.session_state.page == "menu":

        st.title("메뉴를 선택해 주세요.")

        categories = list(
            BRANDS["맥도날드"]["categories"].keys()
        )

        cols = st.columns(len(categories))

        for i, cat in enumerate(categories):
            with cols[i]:
                if st.button(cat, key=f"mcd_tab_{i}"):
                    st.session_state.category = cat
                    st.rerun()

        st.divider()

        menus = BRANDS["맥도날드"]["categories"][
            st.session_state.category
        ]

        cols = st.columns(3)

        for i, (name, price) in enumerate(menus.items()):
            with cols[i % 3]:
                with st.container(border=True):
                    st.markdown(
                        f"""
                        <div class="product">
                        <div style="font-size:40px">🍔</div>
                        <div class="product-name">{name}</div>
                        <div class="product-price">{price:,}원</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    if st.button("선택하기", key=f"mcd_menu_{name}"):
                        st.session_state.selected = {
                            "name": name,
                            "price": price
                        }
                        go("option")

    elif st.session_state.page == "option":

        item = st.session_state.selected

        if item is None:
            go("menu")

        st.title(item["name"])
        st.subheader(f"{item['price']:,}원")

        st.write("주문 수량을 선택하세요.")

        quantity = st.number_input(
            "수량",
            min_value=1,
            max_value=10,
            value=1
        )

        st.write("매장 식사 또는 포장을 선택하세요.")

        order_type = st.radio(
            "이용 방법",
            ["매장에서 먹기", "포장하기"],
            horizontal=True
        )

        st.session_state.order_type = order_type

        st.markdown(
            f"### 총 금액: {item['price']*quantity:,}원"
        )

        if st.button("장바구니에 담기", type="primary"):
            add_to_cart(
                item["name"],
                item["price"],
                quantity,
                order_type
            )
            go("cart")

# =========================
# 7. 메가커피 / 롯데리아 주문
# =========================

def other_brand_order():

    brand_top()

    if st.session_state.page == "category":

        st.title("어떤 메뉴를 주문하시겠어요?")

        categories = list(
            BRANDS[st.session_state.brand]["categories"].keys()
        )

        cols = st.columns(len(categories))

        for i, category in enumerate(categories):
            with cols[i]:
                if st.button(category, key=f"other_cat_{i}"):
                    st.session_state.category = category
                    go("menu")

    elif st.session_state.page == "menu":

        st.title("원하는 메뉴를 선택하세요.")

        categories = list(
            BRANDS[st.session_state.brand]["categories"].keys()
        )

        cols = st.columns(len(categories))

        for i, category in enumerate(categories):
            with cols[i]:
                if st.button(category, key=f"other_tab_{i}"):
                    st.session_state.category = category
                    st.rerun()

        st.divider()

        menus = BRANDS[st.session_state.brand]["categories"][
            st.session_state.category
        ]

        cols = st.columns(3)

        for i, (name, price) in enumerate(menus.items()):
            with cols[i % 3]:
                with st.container(border=True):

                    emoji = "☕" if st.session_state.brand == "메가커피" else "🍔"

                    st.markdown(
                        f"""
                        <div class="product">
                        <div style="font-size:42px">{emoji}</div>
                        <div class="product-name">{name}</div>
                        <div class="product-price">{price:,}원</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    if st.button("이 메뉴 선택", key=f"other_menu_{name}"):
                        st.session_state.selected = {
                            "name": name,
                            "price": price
                        }
                        go("option")

    elif st.session_state.page == "option":

        item = st.session_state.selected

        if item is None:
            go("menu")

        st.title("메뉴 상세 선택")
        st.header(item["name"])
        st.subheader(f"{item['price']:,}원")

        quantity = st.number_input(
            "주문 수량",
            min_value=1,
            max_value=10,
            value=1
        )

        option = ""

        if st.session_state.brand == "메가커피":

            st.markdown("### 음료 온도 선택")

            temperature = st.radio(
                "음료 온도",
                ["HOT 따뜻하게", "ICE 차갑게"],
                horizontal=True
            )

            option = temperature

            st.markdown("### 사이즈 선택")

            size = st.radio(
                "사이즈",
                ["기본", "큰 사이즈"],
                horizontal=True
            )

            if size == "큰 사이즈":
                option += " / 큰 사이즈"

        else:

            st.markdown("### 이용 방법 선택")

            order_type = st.radio(
                "매장 이용",
                ["매장에서 먹기", "포장하기"],
                horizontal=True
            )

            option = order_type

        st.write("")
        st.markdown(
            f"### 총 금액: {item['price']*quantity:,}원"
        )

        if st.button("🛒 장바구니에 담기", type="primary"):
            add_to_cart(
                item["name"],
                item["price"],
                quantity,
                option
            )
            go("cart")


# =========================
# 8. 장바구니
# =========================

def cart_page():

    brand_top()

    st.title("🛒 주문 내역 확인")

    if not st.session_state.cart:

        st.info("아직 선택한 메뉴가 없습니다.")

        if st.button("메뉴 선택하러 가기"):
            go("category")

        return

    for i, item in enumerate(st.session_state.cart):

        with st.container(border=True):

            col1, col2 = st.columns([4, 1])

            with col1:

                st.markdown(f"### {item['name']}")

                st.write(f"수량: {item['quantity']}개")

                if item["option"]:
                    st.caption(f"선택 옵션: {item['option']}")

                st.markdown(
                    f"**{item['price']*item['quantity']:,}원**"
                )

            with col2:

                if st.button("삭제", key=f"delete_{i}"):

                    st.session_state.cart.pop(i)
                    st.rerun()

    st.divider()

    st.markdown(
        f"""
        <div style="background:#E5F2FF;padding:25px;
        border-radius:18px;text-align:center;">
        <div style="font-size:20px;color:#526E86;">
        총 주문 금액
        </div>
        <div style="font-size:36px;font-weight:800;color:#267FC0;">
        {total_price():,}원
        </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("➕ 메뉴 더 담기"):
            go("category")

    with col2:
        if st.button("결제하기 →", type="primary"):
            go("payment")


# =========================
# 9. 결제 화면
# =========================

def payment_page():

    brand_top()

    st.title("💳 결제 방법을 선택해 주세요.")

    st.info(
        "교육용 체험 화면입니다. 실제 카드 정보 입력이나 "
        "실제 결제는 이루어지지 않습니다."
    )

    st.markdown("### 결제 방법")

    payment = st.radio(
        "원하는 결제 수단을 선택하세요.",
        ["💳 신용카드 / 체크카드", "💵 현금", "📱 간편결제"],
        horizontal=False
    )

    st.divider()

    st.metric(
        "결제할 금액",
        f"{total_price():,}원"
    )

    st.write("")

    col1, col2 = st.columns(2)

    with col1:

        if st.button("← 주문 내역으로"):
            go("cart")

    with col2:

        if st.button("결제 진행하기", type="primary"):

            st.session_state.payment = payment
            go("done")


# =========================
# 10. 주문 완료
# =========================

def done_page():

    brand_top()

    st.markdown(
        """
        <div style="
        background:#E4F3FF;
        padding:40px 20px;
        border-radius:22px;
        text-align:center;
        ">
        <div style="font-size:75px;">🎉</div>
        <div style="font-size:34px;font-weight:800;color:#267FC0;">
        주문이 완료되었습니다!
        </div>
        <div style="font-size:20px;color:#526E86;margin-top:15px;">
        정말 잘하셨습니다. 키오스크 주문에 성공하셨어요.
        </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")
    st.subheader("주문 내역")

    for item in st.session_state.cart:

        st.write(
            f"🍽️ {item['name']} "
            f"{item['quantity']}개 "
            f"· {item['price']*item['quantity']:,}원"
        )

    st.divider()

    st.metric(
        "총 주문 금액",
        f"{total_price():,}원"
    )

    st.write(f"결제 방법: {st.session_state.payment}")

    st.success(
        "가상 주문 체험이 성공적으로 끝났습니다. "
        "실제 결제는 발생하지 않았습니다."
    )

    st.write("")

    if st.button("🔄 다른 매장 체험하기", type="primary"):

        st.session_state.cart = []
        st.session_state.selected = None
        st.session_state.payment = ""
        go("brand")


# =========================
# 11. 앱 메인 화면
# =========================

header()

progress()

# 매장 선택 화면
if st.session_state.page == "brand":

    st.title("어떤 매장을 체험해 볼까요?")
    st.write("원하는 브랜드를 선택해 주세요.")

    cols = st.columns(3)

    for i, (brand, data) in enumerate(BRANDS.items()):

        with cols[i]:

            with st.container(border=True):

                st.markdown(
                    f"""
                    <div style="
                    background:{data['background']};
                    padding:30px 10px;
                    border-radius:15px;
                    text-align:center;
                    ">
                    <div style="font-size:65px;">
                    {data['emoji']}
                    </div>
                    <div style="
                    font-size:27px;
                    font-weight:800;
                    color:{data['color']};
                    ">
                    {brand}
                    </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.write("")

                if brand == "맥도날드":
                    st.write("햄버거, 세트, 사이드 주문 체험")
                elif brand == "메가커피":
                    st.write("커피, 음료, HOT / ICE 주문 체험")
                else:
                    st.write("버거, 세트, 사이드 주문 체험")

                if st.button(
                    "이 매장 체험하기",
                    key=f"brand_{i}",
                    type="primary"
                ):

                    st.session_state.brand = brand
                    st.session_state.cart = []
                    st.session_state.selected = None
                    st.session_state.category = list(
                        data["categories"].keys()
                    )[0]

                    go("category")


# 브랜드별 주문 화면
elif st.session_state.page in ["category", "menu", "option"]:

    if st.session_state.brand == "맥도날드":
        mcdonalds_order()
    else:
        other_brand_order()


# 장바구니
elif st.session_state.page == "cart":
    cart_page()


# 결제
elif st.session_state.page == "payment":
    payment_page()


# 주문 완료
elif st.session_state.page == "done":
    done_page()


# =========================
# 12. 설명 보기 버튼
# =========================

guide_button()


# =========================
# 13. 하단 이동 버튼
# =========================

if st.session_state.page not in ["brand", "done"]:

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        if st.button("🏠 처음 화면으로"):

            st.session_state.cart = []
            st.session_state.selected = None
            go("brand")

    with col2:

        if st.button("🛒 장바구니 바로가기"):

            go("cart")
