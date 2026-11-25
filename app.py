import io
import re
import uuid
import requests
import qrcode
import streamlit as st

st.set_page_config(page_title='학교 방문자 사전 등록', page_icon='🏫')
st.title('🏫 학교 방문자 사전 등록')
st.write('방문 정보를 입력하고 QR코드를 발급받으세요.')
if 'request_id' not in st.session_state:
    st.session_state.request_id = uuid.uuid4().hex
if 'receipt' not in st.session_state:
    st.session_state.receipt = None

if st.session_state.receipt is None:
    with st.form('visitor'):
        school = st.text_input('학교명 *', max_chars=100)
        student = st.text_input('학번 *', max_chars=30)
        name = st.text_input('이름 *', max_chars=50)
        phone = st.text_input('연락처 *', placeholder='010-1234-5678', max_chars=20)
        purpose = st.text_area('방문 목적 *', max_chars=500)
        st.caption('수집 목적: 방문자 확인 및 출입 관리. 수집 항목: 학교, 학번, 이름, 연락처, 방문 목적. 보유기간 및 문의처는 학교의 개인정보 처리 안내를 확인하세요.')
        consent = st.checkbox('개인정보 수집 및 이용 안내를 확인하고 동의합니다.')
        submit = st.form_submit_button('방문자 사전 등록하기', use_container_width=True)
    if submit:
        fields = dict(school=school.strip(), student=student.strip(), name=name.strip(), phone=phone.strip(), purpose=purpose.strip())
        if not all(fields.values()) or not consent:
            st.error('모든 항목을 입력하고 개인정보 수집에 동의해 주세요.')
        elif not re.fullmatch(r'01[016789]-?\d{3,4}-?\d{4}', fields['phone']):
            st.error('휴대전화 번호를 확인해 주세요.')
        else:
            try:
                payload = dict(**fields, token=st.secrets['API_TOKEN'], request_id=st.session_state.request_id, consent=True)
                with st.spinner('등록 중입니다...'):
                    response = requests.post(st.secrets['APPS_SCRIPT_URL'], json=payload, timeout=40)
                    response.raise_for_status()
                    result = response.json()
                if result.get('ok') is True and result.get('registration_id') == 'VIS-' + st.session_state.request_id:
                    st.session_state.receipt = result
                    st.rerun()
                else:
                    st.error('등록을 확인하지 못했습니다. 설정을 확인하거나 다시 시도해 주세요.')
            except Exception:
                st.error('서버 응답을 확인하지 못했습니다. 같은 정보로 다시 시도하면 중복 등록을 방지할 수 있습니다.')
else:
    receipt = st.session_state.receipt
    st.success('방문자 사전 등록이 완료되었습니다.')
    rid = receipt['registration_id']
    st.write('등록번호:', rid)
    st.write('등록일시:', receipt.get('registered_at', ''))
    buf = io.BytesIO()
    qrcode.make(rid).save(buf, format='PNG')
    png = buf.getvalue()
    st.image(png, width=260, caption='방문 시 QR코드를 제시하세요.')
    st.download_button('QR코드 다운로드', png, file_name=f'{rid}.png', mime='image/png')
    if st.button('새 방문자 등록'):
        st.session_state.receipt = None
        st.session_state.request_id = uuid.uuid4().hex
        st.rerun()
