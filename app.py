from flask import Flask,request,send_from_directory,jsonify
import werkzeug
from PIL import Image
from fpdf import FPDF
import os

app=Flask(__name__)
BG = Image.open("myfont/bg.png")
sizeOfSheet = BG.width
gap, _ = 0, 0
allowedChars = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM,.-?!() 1234567890'
path = 'E:/Text_to_Handwritten Python App/Python File/static'

def writee(char):
    global gap, _
    if char == '\n':
        pass
    else:
        char.lower()
        cases = Image.open("myfont/%s.png" % char)
        BG.paste(cases, (gap, _))
        size = cases.width
        gap += size
        del cases


def letterwrite(word):
    global gap, _
    if gap > sizeOfSheet - 95 * (len(word)):
        gap = 0
        _ += 200
    for letter in word:
        if letter in allowedChars:
            if letter.islower():
                pass
            elif letter.isupper():
                letter = letter.lower()
                letter += 'upper'
            elif letter == '.':
                letter = "fullstop"
            elif letter == '!':
                letter = 'exclamation'
            elif letter == '?':
                letter = 'question'
            elif letter == ',':
                letter = 'comma'
            elif letter == '(':
                letter = 'braketop'
            elif letter == ')':
                letter = 'braketcl'
            elif letter == '-':
                letter = 'hiphen'
            writee(letter)


def worddd(Input):
    wordlist = Input.split(' ')
    for i in wordlist:
        letterwrite(i)
        writee('space')

def pdf_creation(PNG_FILE,filename, flag=False):
    rgba = Image.open(PNG_FILE)
    rgb = Image.new('RGB', rgba.size, (255, 255, 255))  # white background
    rgb.paste(rgba, mask=rgba.split()[3])  # paste using alpha channel as mask
    rgb.save(f'E:/Text_to_Handwritten Python App/Python File/static/{filename}.pdf',
             append=flag)  #Now save multiple images in same pdf file

@app.route('/')
def home():
    return "Hello!"

@app.route('/download')
def getPDF():
    filename = 'final_output.pdf'
    return send_from_directory(directory=path, filename=filename, as_attachment=True)


@app.route('/upload', methods=['POST'])
def process_request():
    global gap, _,BG
    text_file=request.files['file']
    filename = werkzeug.utils.secure_filename(text_file.filename)
    text_file.save(filename)
    try:
        with open(filename, 'r') as file:
            data = file.read().replace('\n', '')

        with open('final_output.pdf', 'w') as file:
            pass        
        
        l = len(data)
        nn = len(data) // 600
        chunks, chunk_size = len(data), len(data) // (nn + 1)
        p = [data[i:i + chunk_size] for i in range(0, chunks, chunk_size)]
        print(len(p))
        for i in range(0, len(p)):
            worddd(p[i])
            writee('\n')
            BG.save('%doutt.png' % i)
            BG1 = Image.open("myfont/bg.png")
            BG = BG1
            gap = 0
            _ = 0
    except ValueError as E:
        print("{}\nTry again".format(E))
    
    imagelist = []
    
    for i in range(0, len(p)):
        imagelist.append('%doutt.png' % i)
    
    pdf_creation(imagelist.pop(0),filename)
    
    for PNG_FILE in imagelist:
        pdf_creation(PNG_FILE,filename,flag=True)
    
    return "processing done"

if(__name__=="__main__"):
    app.run(host='IP',port=5000,debug=True)