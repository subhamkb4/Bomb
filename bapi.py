from flask import Flask, jsonify, request
import requests
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def make_bomb_call(encrypted_phone):
    """
    Make the API call to the bomb service with the provided encrypted phone number
    """
    cookies = {
        '_ga': 'GA1.1.1130754107.1762117369',
        '__gads': 'ID=6a5ecfe87f6201bc:T=1762117370:RT=1762117370:S=ALNI_Mb18lJ-8BI3lXwtrmU9_BCARjrHqw',
        '__gpi': 'UID=0000130104e735d2:T=1762117370:RT=1762117370:S=ALNI_Ma6qEW5CgFwvlLHMi2oJgk1QIjB9A',
        '__eoi': 'ID=e7b65938a9bf1cc7:T=1762117370:RT=1762117370:S=AA-Afja6V9zlnO7y19SGX5eY8cly',
        '_ga_GGDECM4YSH': 'GS2.1.s1762117368$o1$g1$t1762117436$j60$l0$h0',
        'cf_clearance': 'zBhnPFoYTxvp8NLWSL.wtaAygCAz0V0hTTZLLZBNL.g-1762117449-1.2.1.1-Y9iKXbBC4yDwm0_6EPjRqL_k_j_X6dDNpjrnj3nh3Eslged6M_k3_hgMdqNuXweO6HMIws1EkTBLcaVjKxOt6G_.ih.0TgTkbbolZ0.X1SrnG7m1JkzMJOts5VwqiErI7_N89muDRChrJgaE9uwrjpR9kNlGEAWnBov4uIh0G_Na3h8iOBa_NObwwZGq0Eg9gvQ9RYcegAVl.4LD3asa86Uca3eWKjI9.4s2dZSEKItiQr5HsN382jgTKgduPHrE',
        'FCCDCF': '%5Bnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2C%5B%5B32%2C%22%5B%5C%22c1fe3282-a983-44d2-881c-cf56b8e2e269%5C%22%2C%5B1762117371%2C270000000%5D%5D%22%5D%5D%5D',
        'FCNEC': '%5B%5B%22AKsRol_ilRWkLsQJS5qd-s4HLOuHQD9JhGM2yWyb453QnIfRCwzLbFtDJq5Oa1A7-qvp9XCc4JfwMMmKEIB1rL8rfptx4addl2d0ekfabPj7gNe9ZHy3nldgv51Tb4x89nNGiQCWKmS0IK6j49j9E4GaCZeiF8ONOQ%3D%3D%22%5D%5D',
    }

    headers = {
        'authority': 'b.callbomberz.in',
        'accept': '*/*',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'content-type': 'application/json',
        'origin': 'https://b.callbomberz.in',
        'referer': 'https://b.callbomberz.in/?phn=w2DoIRw%2FTepKI79kIAoDicqiaW%2FR2GgJVPnNdOulJYU%3D',
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

    json_data = {
        'action': 'sendtest',
        'phone': encrypted_phone,
    }

    try:
        response = requests.post(
            'https://b.callbomberz.in/controller', 
            cookies=cookies, 
            headers=headers, 
            json=json_data,
            timeout=30
        )
        
        logger.info(f"API Response Status: {response.status_code}")
        return {
            'success': True,
            'status_code': response.status_code,
            'response_text': response.text,
            'encrypted_phone': encrypted_phone
        }
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {str(e)}")
        return {
            'success': False,
            'error': str(e),
            'encrypted_phone': encrypted_phone
        }

@app.route('/')
def home():
    """Home endpoint with usage instructions"""
    return jsonify({
        'message': 'Bomb API Server is running',
        'usage': 'Use /num=<encrypted_phone_number> to make a call',
        'example': '/num=w2DoIRw/TepKI79kIAoDicqiaW/R2GgJVPnNdOulJYU='
    })

@app.route('/num=<path:target_number>')
def bomb_number(target_number):
    """
    Endpoint to trigger bomb call for the specified encrypted phone number
    """
    logger.info(f"Received request for encrypted number: {target_number}")
    
    # Validate that target_number is provided
    if not target_number or target_number.strip() == "":
        return jsonify({
            'success': False,
            'error': 'Encrypted phone number is required'
        }), 400
    
    # Make the API call
    result = make_bomb_call(target_number)
    
    return jsonify(result)

@app.route('/health')
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({'status': 'healthy', 'service': 'bombapi'})

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)