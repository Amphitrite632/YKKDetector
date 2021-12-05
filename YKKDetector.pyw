import cv2 as cv, PySimpleGUI as sg , sys , datetime

height = 720
loadablefiletype = [("PNG画像", "*.png"), ("JPEG画像", "*.jpg")]
imgname = "./resource/waiting.png"
console_text = "画像を選択してください"
detectiontext = "YKK-San"
Model = "./resource/ModelP.xml"

def YKKDetector():
    global imgname , Model
    img = cv.imread(imgname)
    detectiontext = "YKK-San"    
    grayimg = cv.cvtColor(img, cv.COLOR_BGR2GRAY)       
    custom_cascade = cv.CascadeClassifier(Model)       
    custom_rect = custom_cascade.detectMultiScale(grayimg, scaleFactor=1.01, minNeighbors=12, minSize=(64, 64))
    if len(custom_rect) > 0:
        for rect in custom_rect:
            cv.rectangle(img, tuple(rect[0:2]), tuple(rect[0:2]+rect[2:4]), (70, 75, 250), thickness=2)
            cv.putText(img, detectiontext, tuple(rect[0:2]), cv.FONT_HERSHEY_SIMPLEX, 1.5, (70, 75, 250), 2, cv.LINE_AA)
    dt_now = datetime.datetime.now()
    nowtime = dt_now.strftime('%Y-%m-%d_%H-%M-%S')
    cv.imwrite("./output/"+nowtime+".png", img)
    def resize(img,height):
        h, w = img.shape[:2]
        width = round(w * (height / h))
        preview = cv.resize(img, dsize=(width, height))
        return preview
    preview = resize(img, height)
    cv.imwrite("./resource/preview.png", preview)
    imgname = "./resource/preview.png"

def InfoGUI():
    layout = [
       [sg.Text("ファイル"), sg.InputText(console_text,key="-filename-"), sg.FileBrowse(button_text = "開く",file_types = loadablefiletype,key="-file-", target="-filename-")],
       [sg.Button(button_text = "実行", key="-run-")],
       [(sg.Radio("ModelS",group_id="Model",key="-ModelS-",default = True)),(sg.Radio("ModelP",group_id="Model",key="-ModelP-"))],
       [sg.Image(filename=imgname,size=(1280,720),key="-Image-")]
    ]
    window = sg.Window("YKKDetector Ver0.9.1", layout)
    def InfoGUIUpdate():
        global console_text, imgname, Model
        while True:
            event, values = window.read(timeout=16,timeout_key="-timeout-")
            if event == None:
                sys.exit(0)
            elif event in "-timeout-":
                window["-Image-"].update(imgname)
            if event == "-run-":
                if values["-filename-"] != console_text:
                    imgname = values["-filename-"]
                    if values["-ModelS-"]:
                        print("ModelS Selected")
                        Model = "./resource/ModelS.xml"
                    elif values["-ModelP-"]:
                        print("ModelP Selected")
                        Model = "./resource/ModelP.xml"
                    YKKDetector()
    InfoGUIUpdate()

InfoGUI()