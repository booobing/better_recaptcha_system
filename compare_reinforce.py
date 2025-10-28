import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def find_and_mark_differences(image1_path, image2_path, output_path, threshold=30):
    """
    두 이미지의 차이를 찾아서 표시합니다.
    
    Parameters:
    - image1_path: 첫 번째 이미지 경로
    - image2_path: 두 번째 이미지 경로
    - output_path: 결과 이미지 저장 경로
    - threshold: 차이 감지 임계값 (0-255)
    """
    
    # 이미지 로드
    img1 = cv2.imread(image1_path)
    img2 = cv2.imread(image2_path)
    
    # 이미지 크기가 다르면 조정
    if img1.shape != img2.shape:
        img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
    
    # 그레이스케일로 변환
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    
    # 차이 계산
    diff = cv2.absdiff(gray1, gray2)
    
    # 임계값 적용
    _, thresh = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)
    
    # 노이즈 제거를 위한 모폴로지 연산
    kernel = np.ones((5, 5), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    
    # 컨투어 찾기
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # 결과 이미지 생성 (첫 번째 이미지 복사)
    result = img1.copy()
    
    # 차이가 있는 부분에 빨간색 사각형 그리기
    diff_count = 0
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 100:  # 너무 작은 차이는 무시
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(result, (x, y), (x + w, y + h), (0, 0, 255), 3)
            diff_count += 1
    
    # 결과 저장
    cv2.imwrite(output_path, result)
    
    # 시각화
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    # 원본 이미지들
    axes[0, 0].imshow(cv2.cvtColor(img1, cv2.COLOR_BGR2RGB))
    axes[0, 0].set_title('Image 1 (1번.png)')
    axes[0, 0].axis('off')
    
    axes[0, 1].imshow(cv2.cvtColor(img2, cv2.COLOR_BGR2RGB))
    axes[0, 1].set_title('Image 2 (2번.png)')
    axes[0, 1].axis('off')
    
    # 차이 이미지
    axes[0, 2].imshow(diff, cmap='gray')
    axes[0, 2].set_title('Difference Map')
    axes[0, 2].axis('off')
    
    # 임계값 적용된 이미지
    axes[1, 0].imshow(thresh, cmap='gray')
    axes[1, 0].set_title('Thresholded Difference')
    axes[1, 0].axis('off')
    
    # 결과 이미지
    axes[1, 1].imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
    axes[1, 1].set_title(f'Result ({diff_count} differences found)')
    axes[1, 1].axis('off')
    
    # 빈 공간
    axes[1, 2].axis('off')
    
    plt.rcParams['font.family'] = 'NanumGothic' # Or another Korean font you have installed
    plt.rcParams['axes.unicode_minus'] = False # This line is often included to properly display minus signs   
    plt.tight_layout()
    plt.savefig(output_path.replace('.png', '_analysis.png'), dpi=150, bbox_inches='tight')
    plt.show()
    
    print(f"차이점 {diff_count}개를 발견했습니다.")
    print(f"결과 이미지가 {output_path}에 저장되었습니다.")
    print(f"분석 이미지가 {output_path.replace('.png', '_analysis.png')}에 저장되었습니다.")
    
    return diff_count


if __name__ == "__main__":
    # 이미지 경로 설정
    image1_path = 'before.png'
    image2_path = 'after.png'
    output_path = 'differences_marked.png'
    
    # 차이점 찾기 및 표시
    find_and_mark_differences(image1_path, image2_path, output_path, threshold=30)