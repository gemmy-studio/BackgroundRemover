import streamlit as st
from rembg import remove
from PIL import Image
from io import BytesIO
from streamlit.components.v1 import html

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB


def convert_image(img):
    buf = BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    buf.close()
    return byte_im


def fix_image(upload):
    col1, col2 = st.columns(2)

    image = Image.open(upload)
    col1.write("업로드 이미지")
    col1.image(image)

    try:
        fixed = remove(image)
    except Exception as e:
        st.error(f"배경 제거 중 오류 발생: {e}")
        return
    fixed = remove(image)
    col2.write("변경된 이미지")
    col2.image(fixed)
    st.sidebar.markdown("\n")
    st.sidebar.download_button(
        "이미지 다운로드", convert_image(fixed), "fixed.png", "image/png")


def main():
    st.set_page_config(page_title="이미지 배경 제거 도구", page_icon="favicon.ico",
                       layout="wide", initial_sidebar_state="auto", menu_items=None)

    button = """
    <script type="text/javascript" src="https://cdnjs.buymeacoffee.com/1.0.0/button.prod.min.js" data-name="bmc-button" data-slug="woojae" data-color="#FFDD00" data-emoji="☕"  data-font="Cookie" data-text="Buy me a coffee" data-outline-color="#000000" data-font-color="#000000" data-coffee-color="#ffffff" ></script>
    """

    st.title('이미지 배경 제거 도구')
    st.write('### 이미지에서 불필요한 배경을 제거하세요!')
    st.write(
        "이미지를 업로드 하시고 배경을 제거해보세요. 왼쪽의 사이드바를 사용하여 이미지를 업로드하고 배경이 제거된 이미지를 PNG 파일로 다운로드 할 수 있습니다."
    )
    st.sidebar.write("## 이미지를 업로드 하세요.")

    my_upload = st.sidebar.file_uploader(
        "이미지 크기는 5MB 이하이어야 합니다.", type=["png", "jpg", "jpeg"])

    if my_upload is not None:
        if my_upload.size > MAX_FILE_SIZE:
            st.error(
                "업로드한 이미지의 크기가 너무 급티나. 5MB보다 작은 크기의 이미지를 업로드 해주세요.")
        else:
            with st.spinner('배경 제거하는 중'):
                fix_image(upload=my_upload)

    html(button, height=70, width=240)

    st.markdown(
        """
        <style>
            iframe[width="240"] {
                position: fixed;
                bottom: 30px;
                right: 10px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


if __name__ == '__main__':
    main()
