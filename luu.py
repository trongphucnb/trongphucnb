from flask import Flask, request, jsonify
app = Flask(__name__)

file_path = '/sdt.txt'
sms_path = '/sms.txt'

@app.route('/post/<phone>', methods=['POST'])
def save_phone(phone):
    # Kiểm tra tính hợp lệ của số điện thoại
    if not phone.isdigit() or not (10 <= len(phone) <= 11):
        return "Invalid phone number", 400
    
    # Kiểm tra xem số điện thoại đã tồn tại trong file chưa
    with open(file_path, 'r') as f:
        existing_numbers = f.readlines()
        if phone + '\n' in existing_numbers:
            return "Phone number already exists", 400

    # Lưu số điện thoại vào file
    with open(file_path, 'a') as f:
        f.write(phone + '\n')
    
    return "Phone number saved successfully", 200

@app.route('/get_phone', methods=['GET'])
def get_phone():
    with open(file_path, 'r') as f:
        numbers = f.readlines()

    # Nếu không có số điện thoại trong file
    if not numbers:
        return jsonify({"error": "No phone numbers available"}), 404

    # Lấy số đầu tiên và chuyển nó sang sms.txt
    phone = numbers[0].strip()
    with open(sms_path, 'a') as sms_file:
        sms_file.write(phone + '\n')

    # Xóa số điện thoại đã lấy khỏi sdt.txt
    with open(file_path, 'w') as f:
        f.writelines(numbers[1:])

    return jsonify({"phone": phone}), 200
@app.route('/post_code', methods=['POST'])
def save_code():
    content = request.data.decode('utf-8')
    
    if '|' in content:
        phone, code = content.split('|', 1)

        # Kiểm tra xem sdt đã tồn tại trong sms.txt chưa
        with open(sms_path, 'r') as sms_file:
            if any(line.startswith(phone) for line in sms_file):
                return "Phone number already exists in sms.txt", 400

        # Thêm sdt|code vào sms.txt
        with open(sms_path, 'a') as sms_file:
            sms_file.write(f"{phone}|{code}\n")

        return "Code saved successfully", 200

    return "Invalid content format. Expected format: sdt|code", 400
@app.route('/sec/<phone>', methods=['GET'])
def retrieve_code(phone):
    with open(sms_path, 'r') as sms_file:
        for line in sms_file:
            if line.startswith(phone):
                phone_in_file, code = line.strip().split('|')
                return jsonify({'phone': phone_in_file, 'code': code}), 200

    return jsonify({'error': f"No entry found for phone number: {phone}"}), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5009)
