import os
from flask import Flask, request, jsonify
import speech_recognition as sr

app = Flask(__name__)

def recognize_speech(file_path):
    recognizer = sr.Recognizer()

    with sr.AudioFile(file_path) as source:
        audio_data = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio_data, language="vi-VN")
        return text
    except sr.UnknownValueError:
        return "Không thể nhận dạng giọng nói"
    except sr.RequestError as e:
        return f"Có lỗi trong quá trình gửi yêu cầu đến Google: {e}"

@app.route('/api/translate', methods=['POST'])
def translate_wav():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)
        result = recognize_speech(file_path)
        os.remove(file_path)
        return jsonify({'result': result[:6]}), 200

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)
