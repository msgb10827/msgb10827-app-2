import streamlit as st

# ==========================================
# 0단계: 기본 데이터 및 세션(Session) 상태 초기화
# ==========================================
product_list = ["키링", "스티커", "인형", "엽서"]
price_list = [3000, 2000, 5000, 1000]

# Streamlit은 화면이 새로고침될 때마다 변수가 초기화되므로,
# 유지되어야 할 데이터(장바구니, 현재 화면 단계)는 st.session_state에 저장합니다.
if 'cart_list' not in st.session_state:
    st.session_state.cart_list = []
if 'cart_price' not in st.session_state:
    st.session_state.cart_price = []
if 'phase' not in st.session_state:
    st.session_state.phase = 'shopping'  # 'shopping'(쇼핑 단계) 또는 'checkout'(결제 단계)

st.title("🛒 미니 쇼핑몰")

# ==========================================
# 1단계: 상품 주문 (장바구니 담기)
# ==========================================
if st.session_state.phase == 'shopping':
    st.header("1단계: 상품 주문")
    
    # 판매 상품 목록을 보기 좋게 표시
    st.write("### [현재 판매 상품]")
    cols = st.columns(len(product_list))
    for col, prod, price in zip(cols, product_list, price_list):
        col.metric(label=prod, value=f"{price}원")
    
    st.write("---")
    
    # input() 대신 스트림릿의 selectbox(드롭다운)를 사용하여 잘못된 입력을 원천 차단합니다.
    selected_product = st.selectbox("구매하실 상품을 선택해주세요:", product_list)
    
    if st.button("장바구니에 담기"):
        i = product_list.index(selected_product)
        st.session_state.cart_list.append(selected_product)
        st.session_state.cart_price.append(price_list[i])
        st.success(f"장바구니에 '{selected_product}'이(가) 담겼습니다. (+{price_list[i]}원)")
    
    # 현재 장바구니 현황 표시
    if st.session_state.cart_list:
        st.write(f"**현재 장바구니:** {st.session_state.cart_list}")
        st.write(f"**현재 총 금액:** {sum(st.session_state.cart_price)}원")
        
        # N을 입력하던 것 대신 '결제창으로 이동' 버튼 사용
        if st.button("결제창으로 이동하기"):
            st.session_state.phase = 'checkout'
            st.rerun()  # 화면을 즉시 새로고침하여 결제 화면으로 넘어갑니다.

# ==========================================
# 2단계: 결제 진행
# ==========================================
elif st.session_state.phase == 'checkout':
    st.header("2단계: 결제 진행")
    
    total_price = sum(st.session_state.cart_price)
    
    st.info(f"결제하실 총 금액은 **{total_price}원** 입니다.")
    
    # try-except로 문자열 입력을 막았던 원본 코드 대신,
    # 숫자만 입력받을 수 있는 number_input 위젯을 사용합니다.
    balance = st.number_input("현재 잔액을 입력해주세요 (숫자만):", min_value=0, step=1000)
    
    # 결제 버튼
    if st.button("결제하기"):
        if balance >= total_price:
            st.success("🎉 결제완료!")
            st.write(f"**구매하신 상품:** {', '.join(st.session_state.cart_list)}")
            st.write(f"**총 상품 가격:** {total_price}원")
            st.write(f"**남은 잔액:** {balance - total_price}원")
            st.balloons()  # 스트림릿에서 제공하는 축하 애니메이션
            
        else:
            st.error("잔액이 부족합니다.")
            # st.error를 띄우고 앱이 대기 상태가 되므로, 
            # 원본 코드의 "다시 결제창으로 돌아가기"가 자연스럽게 구현됩니다.
            
    st.write("---")
    # 쇼핑 단계로 다시 돌아갈 수 있는 기능 추가 (편의성)
    if st.button("장바구니로 돌아가기"):
        st.session_state.phase = 'shopping'
        st.rerun()