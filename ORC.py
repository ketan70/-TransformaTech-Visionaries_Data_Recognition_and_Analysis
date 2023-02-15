import cv2
import pytesseract
from matplotlib import pyplot as plt
import os
import pandas as pd 
import numpy as np


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

img = cv2.imread("4.png")


gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (35, 45))

dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1)

contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                                cv2.CHAIN_APPROX_SIMPLE)



# Creating a copy of image
im2 = img.copy()


# for cnt in contours:
#     x, y, w, h = cv2.boundingRect(cnt)
#     rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 4)
#     print(x,y,w,h)
#     cropped = im2[y:y + h, x:x + w]

#     # gray2 = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
#     # ret2, thresh2 = cv2.threshold(gray2, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
#     # rect_kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
#     # dilation2 = cv2.dilate(thresh2, rect_kernel2, iterations = 1)
#     # contours2, hierarchy2 = cv2.findContours(dilation2, cv2.RETR_EXTERNAL,
#     #                                             cv2.CHAIN_APPROX_SIMPLE)
    


#     for cnt1 in contours2:
#         x, y, w, h = cv2.boundingRect(cnt1)
#         rect = cv2.rectangle(cropped, (x, y), (x + w, y + h), (255, 0, 0), 2)

df2 = pd.DataFrame(columns = ['id1','x', 'y','w','h'])
df = pd.DataFrame(columns = ['x', 'y','w','h'])
count1 = 1
count2 = 1
list_id1=[]
list_id2=[]

for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)
    list = [x,y,w,h]
    df.loc[len(df)]=list
    list_id1.append(count1)
    count1 =count1+1

df = df.sort_values(by=["y","x"],ascending=True)
df['id_1'] = list_id1


for i in df.index:

    x=df.x[i]
    y=df.y[i]
    w=df.w[i]
    h=df.h[i]
    id=df.id_1[i]

    

    gray2 = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)
    ret2, thresh2 = cv2.threshold(gray2, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    rect_kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 25))
    dilation2 = cv2.dilate(thresh1, rect_kernel2, iterations = 1)
    contours2, hierarchy2 = cv2.findContours(dilation2, cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)


    # A = x*y
    # B= (x+w)*y
    # C= (x+w)*(y+h)
    # D= (y+h)*x
    for cnt1 in contours2:
        x1, y1, w1, h1 = cv2.boundingRect(cnt1)
        
        # A1 = x1*y1
        # B1= (x1+w1)*y1
        # C1= (x1+w1)*(y1+h1)
        # D1= (y1+h1)*x1
        # print ("x:",x)
        # print ("x1:",x1)
        if x1 >=x and y1>=y and x1+w1<=x+w and y1+h1<=+y+h:
            list = [id,x1,y1,w1,h1]
            df2.loc[len(df2)]=list
            list_id2.append(count2)
            count2=count2+1
                    

df2 = df2.sort_values(by=["id1","y","x"],ascending=True)
df2['id2'] = list_id2


df3 = pd.DataFrame(columns = ['id1','id2','x', 'y','w','h'])

gray3 = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)
ret3, thresh3 = cv2.threshold(gray2, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
rect_kernel3 = cv2.getStructuringElement(cv2.MORPH_RECT, (10,3))
dilation3 = cv2.dilate(thresh3, rect_kernel3, iterations = 1)
contours3, hierarchy3 = cv2.findContours(dilation3, cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)

            
for i in df2.index:
    x1=df2.x[i]
    y1=df2.y[i]
    w1=df2.w[i]
    h1=df2.h[i]
    id1=df2.id1[i]
    id2=df2.id2[i]

    for cnt3 in contours3:
        x2, y2, w2, h2 = cv2.boundingRect(cnt3)
        
        # A1 = x1*y1
        # B1= (x1+w1)*y1
        # C1= (x1+w1)*(y1+h1)
        # D1= (y1+h1)*x1
        # print ("x:",x)
        # print ("x1:",x1)
        if x2 >=x1 and y2>=y1 and x2+w2<=x1+w1 and y2+h2<=+y1+h1:
            list = [id1,id2,x2,y2,w2,h2]
            df3.loc[len(df3)]=list

df3 = df3.sort_values(by=["id1","id2","y","x"],ascending=True)

# df3["y1"]=0
# for i in df3.index:
#     maxvalue =0
#     for k in df3.index:
#         y_1 = df3["y"][i]
#         y_2 = df3["y"][k]
#         if y_1==y_2 and maxvalue ==0:
#             maxvalue=y_2    
#         elif y_2 >(y_1 -10) and y_2< (y_1 +10):
#             maxvalue=y_2
#         else:
#             maxvalue=y_1
#     df3["y1"][i]=maxvalue
#     df3 = df3.sort_values(by=["id1","id2","y1","x"],ascending=True)
# list3_text = []
# for i in df3.index:
#     x=df3.x[i]
#     y=df3.y[i]
#     w=df3.w[i]
#     h=df3.h[i]
#     rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 4)
#     #cropped = im2[y:y + h, x:x + w]

#     # Apply OCR on the cropped image
#     #text = pytesseract.image_to_string(cropped)
#     #list3_text.append(text)

# #df3["Text"]=list3_text

print(df3)


for i in df3.index:
    x=df3.x[i]
    y=df3.y[i]
    w=df3.w[i]
    h=df3.h[i]
    print(y,x)
    rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 4)
    cropped = im2[y:y + h, x:x + w]

    # Apply OCR on the cropped image
    #text = pytesseract.image_to_string(cropped)
    #list3_text.append(text)
    
    rect= cv2.resize(rect, (780, 540))

    cv2.imshow("vido of how to worck reading",rect)
    cv2.waitKey(100)