import streamlit as st
from PIL import Image
import numpy as np
import cv2


def pil2cv(image):
    new_image = np.array(image, dtype=np.uint8)
    if new_image.ndim == 2:  # モノクロ
        new_image = cv2.cvtColor(new_image, cv2.COLOR_GRAY2BGRA)
    elif new_image.shape[2] == 3:  # カラー
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGB2BGRA)
    elif new_image.shape[2] == 4:  # 透過
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGBA2BGRA)
    return new_image


def make_square(image):
    h, w = image.shape[:2]
    a = max(h, w)
    blank = np.full((a, a, 4), 0, dtype=np.uint8)
    blank[int(a / 2 - h / 2):int(a / 2 - h / 2) + h,
          int(a / 2 - w / 2):int(a / 2 - w / 2) + w] = image
    return blank


def main():
    st.markdown('# Notion Icon Maker')
    file = st.file_uploader('画像をアップロードしてください', type=['jpg', 'jpeg', 'png'])
    if file:
        st.markdown(f'{file.name} をアップロードしました')
        img = Image.open(file)
        st.image(img)

    if file is not None:
        cv_img = pil2cv(img)
        dst = make_square(cv_img)
        cv2.imwrite("dst.png", dst)
        st.download_button(
            'ダウンロード',
            open("dst.png", 'br'),
            file.name
        )


if __name__ == '__main__':
    main()

