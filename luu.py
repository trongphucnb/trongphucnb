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

@app.route('/getphone', methods=['GET'])
def get_phone():
    with open(file_path, 'r') as f:
        numbers = f.readlines()

    # Nếu không có số điện thoại trong file
    if not numbers:
        return jsonify({"error": "No phone numbers available"}), 404
        
    # Xóa số điện thoại đã lấy khỏi sdt.txt
    with open(file_path, 'w') as f:
        f.writelines(numbers[1:])
 
    return jsonify({"phone": phone}), 200
@app.route('/postcode/<code>', methods=['POST'])
def save_code(code):
    # Đọc tất cả các mã từ file
    with open(sms_path, 'r') as sms_file:
        existing_codes = [line.strip() for line in sms_file.readlines()]

    # Kiểm tra nếu mã đã tồn tại
    if code in existing_codes:
        return "Code already exists", 400

    # Lưu mã vào file
    with open(sms_path, 'a') as sms_file:
        sms_file.write(code + '\n')
        
    return "Code saved successfully", 200

@app.route('/getcode', methods=['GET'])
def retrieve_codes():
    with open(sms_path, 'r') as sms_file:
        codes = [line.strip() for line in sms_file.readlines()]
    
    # Xóa dữ liệu sau khi truy xuất
    with open(sms_path, 'w') as sms_file:
        sms_file.write("")

    return jsonify({'codes': codes}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5009)
