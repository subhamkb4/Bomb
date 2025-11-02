from flask import Flask, request, jsonify
import requests
import base64
import json
from urllib.parse import quote

app = Flask(__name__)

class CallBomberAPI:
    def __init__(self):
        self.base_url = "https://b.callbomberz.in"
        self.cookies = {
            '_ga': 'GA1.1.1130754107.1762117369',
            '__gads': 'ID=6a5ecfe87f6201bc:T=1762117370:RT=1762117370:S=ALNI_Mb18lJ-8BI3lXwtrmU9_BCARjrHqw',
            '__gpi': 'UID=0000130104e735d2:T=1762117370:RT=1762117370:S=ALNI_Ma6qEW5CgFwvlLHMi2oJgk1QIjB9A',
            '__eoi': 'ID=e7b65938a9bf1cc7:T=1762117370:RT=1762117370:S=AA-Afja6V9zlnO7y19SGX5eY8cly',
            '_ga_GGDECM4YSH': 'GS2.1.s1762117368$o1$g1$t1762117436$j60$l0$h0',
            'cf_clearance': 'zBhnPFoYTxvp8NLWSL.wtaAygCAz0V0hTTZLLZBNL.g-1762117449-1.2.1.1-Y9iKXbBC4yDwm0_6EPjRqL_k_j_X6dDNpjrnj3nh3Eslged6M_k3_hgMdqNuXweO6HMIws1EkTBLcaVjKxOt6G_.ih.0TgTkbbolZ0.X1SrnG7m1JkzMJOts5VwqiErI7_N89muDRChrJgaE9uwrjpR9kNlGEAWnBov4uIh0G_Na3h8iOBa_NObwwZGq0Eg9gvQ9RYcegAVl.4LD3asa86Uca3eWKjI9.4s2dZSEKItiQr5HsN382jgTKgduPHrE',
            'FCCDCF': '%5Bnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2C%5B%5B32%2C%22%5B%5C%22c1fe3282-a983-44d2-881c-cf56b8e2e269%5C%22%2C%5B1762117371%2C270000000%5D%5D%22%5D%5D%5D',
            'FCNEC': '%5B%5B%22AKsRol_ilRWkLsQJS5qd-s4HLOuHQD9JhGM2yWyb453QnIfRCwzLbFtDJq5Oa1A7-qvp9XCc4JfwMMmKEIB1rL8rfptx4addl2d0ekfabPj7gNe9ZHy3nldgv51Tb4x89nNGiQCWKmS0IK6j49j9E4GaCZeiF8ONOQ%3D%3D%22%5D%5D',
        }
        self.headers = {
            'authority': 'b.callbomberz.in',
            'accept': '*/*',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'content-type': 'application/json',
            'origin': 'https://b.callbomberz.in',
            'referer': 'https://b.callbomberz.in/',
            'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
            'sec-ch-ua-arch': '""',
            'sec-ch-ua-bitness': '""',
            'sec-ch-ua-full-version': '"139.0.7339.0"',
            'sec-ch-ua-full-version-list': '"Chromium";v="139.0.7339.0", "Not;A=Brand";v="99.0.0.0"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-model': '"CPH2607"',
            'sec-ch-ua-platform': '"Android"',
            'sec-ch-ua-platform-version': '"15.0.0"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }
    
    def encode_phone(self, phone_number):
        """Encode phone number to base64 for the API"""
        encoded = base64.b64encode(phone_number.encode()).decode()
        return encoded
    
    def send_bomb(self, phone_number):
        """Send bomb request to the target number"""
        try:
            # Encode the phone number
            encoded_phone = self.encode_phone(phone_number)
            
            # Update referer with encoded phone
            self.headers['referer'] = f'https://b.callbomberz.in/?phn={quote(encoded_phone)}'
            
            # Prepare JSON data
            json_data = {
                'action': 'sendtest',
                'phone': encoded_phone,
            }
            
            # Send the request
            response = requests.post(
                f'{self.base_url}/controller',
                cookies=self.cookies,
                headers=self.headers,
                json=json_data,
                timeout=30
            )
            
            return {
                'status': 'success',
                'target_number': phone_number,
                'response_status': response.status_code,
                'response_text': response.text,
                'encoded_phone': encoded_phone
            }
            
        except requests.exceptions.RequestException as e:
            return {
                'status': 'error',
                'target_number': phone_number,
                'error': str(e)
            }
        except Exception as e:
            return {
                'status': 'error',
                'target_number': phone_number,
                'error': f'Unexpected error: {str(e)}'
            }

# Initialize the bomber API
bomber_api = CallBomberAPI()

@app.route('/')
def home():
    """Home endpoint with API information"""
    return jsonify({
        'message': 'Call Bomber API',
        'version': '1.0',
        'endpoints': {
            'bomb_number': 'GET /num=<phone_number>',
            'health': 'GET /health'
        },
        'usage': 'Send GET request to /num=YOUR_TARGET_NUMBER'
    })

@app.route('/num=<path:target_number>')
def bomb_number(target_number):
    """
    Bomb a target phone number
    Example: /num=+1234567890 or /num=1234567890
    """
    # Validate phone number (basic validation)
    if not target_number or len(target_number) < 10:
        return jsonify({
            'status': 'error',
            'message': 'Invalid phone number format'
        }), 400
    
    # Send bomb request
    result = bomber_api.send_bomb(target_number)
    
    return jsonify(result)

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Call Bomber API'
    })

@app.route('/encode/<phone_number>')
def encode_number(phone_number):
    """Encode a phone number to see the format used by the API"""
    encoded = bomber_api.encode_phone(phone_number)
    return jsonify({
        'original': phone_number,
        'encoded': encoded,
        'url_encoded': quote(encoded)
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'status': 'error',
        'message': 'Endpoint not found. Use /num=<phone_number>'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'status': 'error',
        'message': 'Internal server error'
    }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)