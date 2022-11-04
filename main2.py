import cv2
import pandas as pd
import argparse
import math

# Tạo đối số phân tích cú pháp để lấy hình ảnh đường dẫn từ dòng lệnh
ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', default='phongcanh.jpg', help="Image Path")
args = vars(ap.parse_args())
img_path = args['image']

# Đọc hình ảnh bằng opencv
img = cv2.imread(img_path)

# khai báo các biến toàn cục (được sử dụng sau này)
clicked = False
r = g = b = xpos = ypos = 0

# Đọc tệp csv với pandas và đặt tên cho từng cột
index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv('colors.csv', names=index, header=None)


# chức năng tính toán khoảng cách tối thiểu từ tất cả các màu và lấy màu phù hợp nhất
def getColorName(R, G, B):
    minimum = 10000
    for i in range(len(csv)):
        d = math.sqrt(R - int(csv.loc[i, "R"])) + math.sqrt(G - int(csv.loc[i, "G"])) + math.sqrt(
            B - int(csv.loc[i, "B"]))  # loc: nhan các hàng hoặc cột với cụ thể nhãn từ chỉ mục
        if (d <= minimum):
            minimum = d
            cname = csv.loc[i, "color_name"]
    return cname


# chức năng lấy tọa độ x, y khi nhấp đúp chuột
def draw_function(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b, g, r, xpos, ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b, g, r = img[y, x]
        b = int(b)
        g = int(g)
        r = int(r)


cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_function)

while (1):

    cv2.imshow("image", img)
    if (clicked):

        # cv2.rectangle (hình ảnh, điểm đầu, điểm cuối, màu sắc, độ dày) -1 lấp đầy toàn bộ hình chữ nhật
        cv2.rectangle(img, (20, 20), (750, 60), (b, g, r), -1)

        # Tạo chuỗi văn bản để hiển thị (Tên màu và các giá trị RGB)
        text = getColorName(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)

        # cv2.putText (img, văn bản, bắt đầu, phông chữ (0-7), fontScale, màu, độ dày, lineType)
        cv2.putText(img, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

        # Đối với các màu rất nhạt, hệ thống sẽ hiển thị văn bản bằng màu đen
        if (r + g + b >= 600):
            cv2.putText(img, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

        clicked = False

    # Ngắt vòng lặp khi người dùng nhấn phím 'esc'
    if cv2.waitKey(20) & 0xFF == 27:
        break

cv2.destroyAllWindows()
