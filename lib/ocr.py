import requests
from PIL import Image
import pytesseract  # pip install pillow pytesseract tesseract
from io import BytesIO
pytesseract.pytesseract.tesseract_cmd = r'D:\Program Files\Tesseract-OCR\tesseract.exe'  # Replace with your actual path


def ocr_qrcode(url):
    """
    从指定 URL 下载图片并进行 OCR 识别

    :param url: 图片的 URL
    :return: 识别结果
    """
    try:
        # 发送请求下载图片
        response = requests.get(url)
        response.raise_for_status()

        # 打开图片
        image = Image.open(BytesIO(response.content))
        download_path = "downloaded_image.jpg"
        image.save(download_path)
        print(f"图片已下载到 {download_path}")
        # 图片预处理（转为灰度图）
        image = image.convert('L')
        # 使用 pytesseract 进行 OCR 识别
        captcha_text = pytesseract.image_to_string(image)
        return captcha_text.strip()
    except requests.RequestException as e:
        print(f"下载图片时出错: {e}")
    except Exception as e:
        print(f"识别图片时出错: {e}")
    return None    


def main():
    # 替换为实际的图片 URL
    image_url = 'https://bt66.org/index.php?s=Vcode-Index'
    result = ocr_qrcode(image_url)
    if result:
        print(f"识别结果: {result}")
    else:
        print("识别失败，请检查图片 URL 或网络连接。")

if __name__ == "__main__":
    main()
