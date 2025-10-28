import cv2
import numpy as np
import matplotlib.pyplot as plt

def generate_test_images(width=600, height=200, text="PASSWORD"):
    """
    분석을 위한 'before'와 'after' 테스트 이미지를 생성합니다.
    'after' 이미지에는 미세한 노이즈 변화로 텍스트가 숨겨져 있습니다.
    """
    # 1. 완전한 랜덤 노이즈로 'before' 이미지 생성
    before_img = np.random.randint(0, 256, (height, width), dtype=np.uint8)
    
    # 2. 'before' 이미지를 복사하여 'after' 이미지의 기반으로 사용
    after_img = before_img.copy()

    # 3. 텍스트 마스크 생성
    # 검은 배경에 흰색으로 텍스트를 그려서 텍스트 영역을 정의합니다.
    text_mask = np.zeros((height, width), dtype=np.uint8)
    font = cv2.FONT_HERSHEY_SIMPLEX
    text_size, _ = cv2.getTextSize(text, font, 2, 3)
    text_x = (width - text_size[0]) // 2
    text_y = (height + text_size[1]) // 2
    cv2.putText(text_mask, text, (text_x, text_y), font, 2, (255), 3)

    # 4. 텍스트 영역에만 새로운 노이즈 생성
    # text_mask가 흰색(255)인 위치를 찾습니다.
    text_pixels = np.where(text_mask == 255)
    # 해당 위치에만 새로운 랜덤 노이즈 값을 삽입합니다.
    new_noise = np.random.randint(0, 256, len(text_pixels[0]), dtype=np.uint8)
    after_img[text_pixels] = new_noise

    # 5. 생성된 이미지 파일로 저장
    cv2.imwrite('before.png', before_img)
    cv2.imwrite('after.png', after_img)
    print("테스트용 이미지 'before.png'와 'after.png'가 생성되었습니다.")
    return 'before.png', 'after.png'


def analyze_and_display_differences(before_path, after_path):
    """
    두 이미지의 차이점을 분석하고, 모든 과정을 Matplotlib을 사용해 시각화합니다.
    """
    # 1. 이미지 로드 (회색조로)
    before = cv2.imread(before_path, cv2.IMREAD_GRAYSCALE)
    after = cv2.imread(after_path, cv2.IMREAD_GRAYSCALE)
    
    # '결과' 이미지는 컬러로 표시하기 위해 BGR로 다시 로드
    after_color = cv2.cvtColor(after, cv2.COLOR_GRAY2BGR)

    # 2. Difference Map 생성 (두 이미지의 절대적인 차이)
    diff = cv2.absdiff(before, after)

    # 3. Thresholded Difference 생성 (차이점을 흑백으로 명확히 분리)
    # 약간의 차이라도 있으면 흰색(255)으로 만듭니다.
    _, thresh = cv2.threshold(diff, 1, 255, cv2.THRESH_BINARY)

    # 4. 윤곽선(Contours) 찾기
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 5. 결과 이미지에 바운딩 박스(사각형) 그리기
    result_img = after_color.copy()
    found_differences = 0
    for contour in contours:
        # 너무 작은 노이즈는 무시
        if cv2.contourArea(contour) > 20:
            found_differences += 1
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(result_img, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # 6. Matplotlib을 사용하여 모든 결과 시각화
    # plt.style.use('dark_background') # 어두운 테마를 원할 경우 주석 해제
    
    fig = plt.figure(figsize=(12, 6))
    
    # 이미지 제목 딕셔너리
    titles = {
        'Image 1 (before.png)': before,
        'Image 2 (after.png)': after,
        'Difference Map': diff,
        'Thresholded Difference': thresh,
        f'Result ({found_differences} differences found)': result_img
    }
    
    # 각 이미지를 subplot에 표시
    for i, (title, img) in enumerate(titles.items()):
        ax = fig.add_subplot(2, 3, i + 1)
        # BGR 이미지는 RGB로 변환해야 Matplotlib에서 색이 제대로 나옵니다.
        if img.ndim == 3:
            plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        else:
            plt.imshow(img, cmap='gray')
            
        ax.set_title(title)
        ax.axis('off') # 축 정보 숨기기

    plt.tight_layout() # 이미지 간 간격 자동 조절
    plt.show()


# --- 메인 코드 실행 ---
if __name__ == "__main__":
    # 1. 분석에 사용할 테스트 이미지를 먼저 생성합니다.
    before_image_file, after_image_file = generate_test_images()
    
    # 2. 생성된 이미지를 가지고 분석 및 시각화를 수행합니다.
    analyze_and_display_differences(before_image_file, after_image_file)