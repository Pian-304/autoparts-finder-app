# webapp.py - AutoParts Finder USA
import os
import re
import html
import time
import io
import logging
from datetime import datetime
from urllib.parse import urlparse, quote_plus
from functools import wraps

from flask import Flask, request, jsonify, session, redirect, url_for, render_template_string, flash
import requests

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    genai = None
    GEMINI_AVAILABLE = False

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear app Flask
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'autoparts-secret-key-2025')
app.config['PERMANENT_SESSION_LIFETIME'] = 1800
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = bool(os.environ.get('RENDER'))
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Configurar Gemini
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
GEMINI_READY = False

if GEMINI_AVAILABLE and GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        GEMINI_READY = True
        logger.info("Gemini configurado")
    except Exception as e:
        logger.error(f"Error Gemini: {e}")

# Base de datos de sitios
AUTOPARTS_SITES = [
    'rockauto.com', 'carparts.com', 'partsgeek.com', '1aauto.com', 'carid.com',
    'autozone.com', 'oreillyauto.com', 'advanceautoparts.com', 'napaonline.com',
    'pepboys.com', 'amazon.com', 'ebay.com', 'parts.honda.com', 'parts.toyota.com',
    'mopar.com', 'jegs.com', 'summitracing.com', 'ecstuning.com', 'fcpeuro.com'
]

logger.info(f"Sitios de autopartes cargados: {len(AUTOPARTS_SITES)}")

class FirebaseAuth:
    def __init__(self):
        self.api_key = os.environ.get("FIREBASE_WEB_API_KEY")
        self.configured = bool(self.api_key)
        logger.info(f"Firebase: {'OK' if self.configured else 'NO'}")
    
    def login_user(self, email, password):
        if not self.configured:
            return {'success': False, 'message': 'Servicio no configurado', 'user_data': None}
        
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={self.api_key}"
        payload = {'email': email, 'password': password, 'returnSecureToken': True}
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            user_data = response.json()
            
            return {
                'success': True,
                'message': 'Bienvenido!',
                'user_data': {
                    'user_id': user_data['localId'],
                    'email': user_data['email'],
                    'display_name': user_data.get('displayName', email.split('@')[0]),
                    'id_token': user_data['idToken']
                }
            }
        except Exception as e:
            logger.error(f"Login error: {e}")
            return {'success': False, 'message': 'Error de login', 'user_data': None}
    
    def set_user_session(self, user_data):
        session.update({
            'user_id': user_data['user_id'],
            'user_name': user_data['display_name'],
            'user_email': user_data['email'],
            'login_time': datetime.now().isoformat()
        })
        session.permanent = True
    
    def clear_user_session(self):
        session.clear()
    
    def is_user_logged_in(self):
        return 'user_id' in session
    
    def get_current_user(self):
        if not self.is_user_logged_in():
            return None
        return {
            'user_id': session.get('user_id'),
            'user_name': session.get('user_name'),
            'user_email': session.get('user_email')
        }

firebase_auth = FirebaseAuth()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not firebase_auth.is_user_logged_in():
            flash('Sesión expirada', 'warning')
            return redirect(url_for('auth_login_page'))
        return f(*args, **kwargs)
    return decorated_function

def analyze_image_with_gemini(image_content):
    if not GEMINI_READY or not PIL_AVAILABLE or not image_content:
        return None
    
    try:
        image = Image.open(io.BytesIO(image_content))
        if image.size[0] > 1024 or image.size[1] > 1024:
            image.thumbnail((1024, 1024), Image.Resampling.LANCZOS)
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        prompt = """Analiza esta imagen de autoparte y genera una consulta de búsqueda en inglés.
        Identifica el tipo de pieza, marca si es visible, y características.
        Responde solo con la consulta optimizada.
        Ejemplo: brake pads ceramic Honda Civic"""
        
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        response = model.generate_content([prompt, image])
        
        if response.text:
            return response.text.strip()
        return None
    except Exception as e:
        logger.error(f"Error imagen: {e}")
        return None

def validate_image(image_content):
    if not PIL_AVAILABLE or not image_content:
        return False
    try:
        image = Image.open(io.BytesIO(image_content))
        return image.size[0] >= 10 and image.size[1] >= 10 and image.format in ['JPEG', 'PNG', 'WEBP']
    except:
        return False

class AutoPartsFinder:
    def __init__(self):
        self.api_key = os.environ.get('SERPAPI_KEY') or os.environ.get('SERPAPI_API_KEY')
        self.base_url = "https://serpapi.com/search"
        self.cache = {}
        self.cache_ttl = 300
        logger.info(f"SerpAPI: {'OK' if self.api_key else 'NO'}")
    
    def is_configured(self):
        return bool(self.api_key)
    
    def is_autoparts_site(self, url_or_domain):
        if not url_or_domain:
            return False
        try:
            if url_or_domain.startswith('http'):
                domain = urlparse(url_or_domain).netloc.lower()
            else:
                domain = url_or_domain.lower()
            
            domain = domain.replace('www.', '').replace('shop.', '').replace('parts.', '')
            
            for site in AUTOPARTS_SITES:
                if site in domain or domain in site:
                    return True
            return False
        except:
            return False
    
    def extract_price(self, price_str):
        if not price_str:
            return 0.0
        try:
            clean_price = str(price_str).replace(',', '').replace('$', '').replace('USD', '').strip()
            match = re.search(r'(\d{1,5}(?:\.\d{2})?)', clean_price)
            if match:
                price = float(match.group(1))
                if 0.50 <= price <= 15000:
                    return price
        except:
            pass
        return 0.0
    
    def generate_realistic_price(self, query, index=0):
        query_lower = query.lower()
        if any(word in query_lower for word in ['engine', 'motor']):
            base_price = 800
        elif any(word in query_lower for word in ['brake', 'freno']):
            base_price = 85
        elif any(word in query_lower for word in ['headlight', 'light']):
            base_price = 120
        elif any(word in query_lower for word in ['filter', 'filtro']):
            base_price = 25
        else:
            base_price = 60
        return round(base_price * (1 + index * 0.18), 2)
    
    def get_product_link(self, item):
        if not item:
            return "#"
        
        for key in ['product_link', 'link']:
            link = item.get(key, '')
            if link and self.is_autoparts_site(link):
                return link
        
        title = item.get('title', '')
        source = item.get('source', '').lower()
        
        if title:
            search_query = quote_plus(title[:60])
            if 'amazon' in source:
                return f"https://www.amazon.com/s?k={search_query}+automotive"
            elif 'autozone' in source:
                return f"https://www.autozone.com/parts?searchText={search_query}"
            elif 'oreilly' in source:
                return f"https://www.oreillyauto.com/search?q={search_query}"
            else:
                return f"https://www.google.com/search?tbm=shop&q={search_query}+auto+parts"
        return "#"
    
    def make_request(self, engine, query):
        if not self.api_key:
            return None
        
        optimized_query = f"{query} automotive parts replacement"
        
        params = {
            'engine': engine,
            'q': optimized_query,
            'api_key': self.api_key,
            'num': 10,
            'location': 'United States',
            'gl': 'us'
        }
        
        if engine == 'google_shopping':
            params['tbm'] = 'shop'
        
        try:
            time.sleep(0.5)
            response = requests.get(self.base_url, params=params, timeout=10)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            logger.error(f"API error: {e}")
        return None
    
    def process_results(self, data, engine):
        if not data:
            return []
        
        results_key = 'shopping_results' if engine == 'google_shopping' else 'organic_results'
        results = data.get(results_key, [])
        
        products = []
        autopart_keywords = ['part', 'filter', 'brake', 'engine', 'automotive', 'car', 'auto', 'oem', 'aftermarket']
        
        for item in results:
            if len(products) >= 6:
                break
            
            title = item.get('title', '')
            if len(title) < 5:
                continue
            
            if not any(keyword in title.lower() for keyword in autopart_keywords):
                continue
            
            source = item.get('source', '')
            if not self.is_autoparts_site(source):
                continue
            
            price_str = item.get('price', '')
            price_num = self.extract_price(price_str)
            if price_num == 0:
                price_num = self.generate_realistic_price(title, len(products))
            
            product = {
                'title': html.escape(title[:120]),
                'price': f"${price_num:.2f}",
                'price_numeric': float(price_num),
                'source': html.escape(source[:50]),
                'link': self.get_product_link(item),
                'rating': str(item.get('rating', '')),
                'reviews': str(item.get('reviews', '')),
                'is_autoparts_site': True,
                'engine_source': engine
            }
            products.append(product)
        
        return products
    
    def search_autoparts(self, query=None, image_content=None):
        final_query = query or "auto parts"
        search_source = "text"
        
        if image_content and GEMINI_READY and validate_image(image_content):
            image_query = analyze_image_with_gemini(image_content)
            if image_query:
                if query:
                    final_query = f"{query} {image_query}"
                    search_source = "combined"
                else:
                    final_query = image_query
                    search_source = "image"
        
        logger.info(f"Búsqueda: '{final_query}' ({search_source})")
        
        cache_key = f"autoparts_{hash(final_query.lower())}"
        if cache_key in self.cache:
            cache_data, timestamp = self.cache[cache_key]
            if (time.time() - timestamp) < self.cache_ttl:
                return cache_data
        
        if not self.api_key:
            return self.get_examples(final_query)
        
        all_products = []
        
        # Google Shopping
        shopping_data = self.make_request('google_shopping', final_query)
        if shopping_data:
            products = self.process_results(shopping_data, 'google_shopping')
            all_products.extend(products)
        
        # Google orgánico si necesitamos más
        if len(all_products) < 4:
            organic_data = self.make_request('google', final_query)
            if organic_data:
                products = self.process_results(organic_data, 'google')
                all_products.extend(products)
        
        # Ejemplos si muy pocos resultados
        if len(all_products) < 3:
            examples = self.get_examples(final_query)
            all_products.extend(examples[:3])
        
        # Remover duplicados
        seen_titles = set()
        unique_products = []
        for product in all_products:
            title_key = product['title'].lower()[:50]
            if title_key not in seen_titles:
                seen_titles.add(title_key)
                unique_products.append(product)
                product['search_source'] = search_source
        
        # Ordenar por precio
        unique_products.sort(key=lambda x: x['price_numeric'])
        final_products = unique_products[:6]
        
        # Cache
        self.cache[cache_key] = (final_products, time.time())
        if len(self.cache) > 20:
            oldest_key = min(self.cache.keys(), key=lambda k: self.cache[k][1])
            del self.cache[oldest_key]
        
        return final_products
    
    def get_examples(self, query):
        stores = [
            ('RockAuto', 'rockauto.com'),
            ('AutoZone', 'autozone.com'),
            ('O\'Reilly Auto', 'oreillyauto.com')
        ]
        
        examples = []
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['brake', 'freno']):
            parts_data = [('Ceramic Brake Pads Set', 75), ('Brake Rotor Pair', 120), ('Brake Caliper', 95)]
        elif any(word in query_lower for word in ['filter', 'filtro']):
            parts_data = [('OEM Air Filter', 18), ('Premium Oil Filter', 12), ('Cabin Air Filter', 22)]
        else:
            base_name = query.title() if len(query) < 30 else query[:30].title()
            parts_data = [(f'{base_name} OEM', 60), (f'{base_name} Aftermarket', 45), (f'{base_name} Premium', 85)]
        
        for i, (store_name, store_domain) in enumerate(stores):
            part_name, base_price = parts_data[i % len(parts_data)]
            final_price = round(base_price * (1 + i * 0.15), 2)
            
            store_links = {
                'rockauto.com': 'https://www.rockauto.com/en/catalog',
                'autozone.com': 'https://www.autozone.com/parts',
                'oreillyauto.com': 'https://www.oreillyauto.com/'
            }
            
            examples.append({
                'title': f'{part_name} - {["Premium", "OEM", "Value"][i]}',
                'price': f'${final_price:.2f}',
                'price_numeric': final_price,
                'source': store_name,
                'link': store_links.get(store_domain, f'https://{store_domain}'),
                'rating': ['4.6', '4.3', '4.4'][i],
                'reviews': ['1250', '890', '720'][i],
                'search_source': 'example',
                'engine_source': 'example',
                'is_autoparts_site': True
            })
        
        return examples

autoparts_finder = AutoPartsFinder()

def render_page(title, content):
    return f'''<!DOCTYPE html>
<html lang="es">
<head>
    <title>{title}</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, sans-serif; background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); min-height: 100vh; padding: 15px; }}
        .container {{ max-width: 650px; margin: 0 auto; background: white; padding: 25px; border-radius: 12px; box-shadow: 0 8px 25px rgba(0,0,0,0.15); }}
        h1 {{ color: #1e3c72; text-align: center; margin-bottom: 8px; font-size: 1.8em; }}
        .subtitle {{ text-align: center; color: #666; margin-bottom: 25px; }}
        input {{ width: 100%; padding: 12px; margin: 8px 0; border: 2px solid #e1e5e9; border-radius: 6px; font-size: 16px; }}
        input:focus {{ outline: none; border-color: #1e3c72; }}
        button {{ width: 100%; padding: 12px; background: #1e3c72; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 16px; font-weight: 600; }}
        .search-bar {{ display: flex; gap: 8px; margin-bottom: 20px; }}
        .search-bar input {{ flex: 1; }}
        .search-bar button {{ width: auto; padding: 12px 20px; }}
        .tips {{ background: #e8f5e8; border: 1px solid #4caf50; padding: 15px; border-radius: 6px; margin-bottom: 15px; font-size: 14px; }}
        .error {{ background: #ffebee; color: #c62828; padding: 12px; border-radius: 6px; margin: 12px 0; display: none; }}
        .loading {{ text-align: center; padding: 30px; display: none; }}
        .spinner {{ border: 3px solid #f3f3f3; border-top: 3px solid #1e3c72; border-radius: 50%; width: 40px; height: 40px; animation: spin 1s linear infinite; margin: 0 auto 15px; }}
        @keyframes spin {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}
        .user-info {{ background: #e3f2fd; padding: 12px; border-radius: 6px; margin-bottom: 15px; text-align: center; font-size: 14px; }}
        .user-info a {{ color: #1976d2; text-decoration: none; font-weight: 600; }}
        .flash {{ padding: 12px; margin-bottom: 8px; border-radius: 6px; font-size: 14px; }}
        .flash.success {{ background-color: #d4edda; color: #155724; }}
        .flash.danger {{ background-color: #f8d7da; color: #721c24; }}
        .flash.warning {{ background-color: #fff3cd; color: #856404; }}
        .image-upload {{ background: #f8f9fa; border: 2px dashed #dee2e6; border-radius: 8px; padding: 20px; text-align: center; margin: 15px 0; }}
        .image-upload input[type="file"] {{ display: none; }}
        .image-upload label {{ cursor: pointer; color: #1e3c72; font-weight: 600; }}
        .image-preview {{ max-width: 150px; max-height: 150px; margin: 10px auto; border-radius: 8px; display: none; }}
    </style>
</head>
<body>{content}</body>
</html>'''

LOGIN_TEMPLATE = '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login | AutoParts Finder USA</title>
    <style>
        body { font-family: -apple-system, sans-serif; background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); min-height: 100vh; display: flex; justify-content: center; align-items: center; padding: 20px; }
        .auth-container { max-width: 420px; width: 100%; background: white; border-radius: 15px; box-shadow: 0 20px 40px rgba(0,0,0,0.1); overflow: hidden; }
        .form-header { text-align: center; padding: 30px 25px 15px; background: linear-gradient(45deg, #1e3c72, #2a5298); color: white; }
        .form-header h1 { font-size: 1.8em; margin-bottom: 8px; }
        .form-body { padding: 25px; }
        form { display: flex; flex-direction: column; gap: 18px; }
        .input-group { display: flex; flex-direction: column; gap: 6px; }
        .input-group label { font-weight: 600; color: #1e3c72; font-size: 14px; }
        .input-group input { padding: 14px 16px; border: 2px solid #e0e0e0; border-radius: 8px; font-size: 16px; }
        .input-group input:focus { outline: 0; border-color: #1e3c72; }
        .submit-btn { background: linear-gradient(45deg, #1e3c72, #2a5298); color: white; border: none; padding: 14px 25px; font-size: 16px; font-weight: 600; border-radius: 8px; cursor: pointer; }
        .flash { padding: 12px; margin-bottom: 10px; border-radius: 6px; text-align: center; font-size: 14px; }
        .flash.success { background-color: #d4edda; color: #155724; }
        .flash.danger { background-color: #f8d7da; color: #721c24; }
        .flash.warning { background-color: #fff3cd; color: #856404; }
    </style>
</head>
<body>
    <div class="auth-container">
        <div class="form-header">
            <div style="font-size: 2em; margin-bottom: 10px;">🔧</div>
            <h1>AutoParts Finder USA</h1>
            <p>Repuestos Automotrices</p>
        </div>
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="flash {{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        <div class="form-body">
            <form action="{{ url_for('auth_login') }}" method="post">
                <div class="input-group">
                    <label for="email">Email</label>
                    <input type="email" name="email" id="email" required>
                </div>
                <div class="input-group">
                    <label for="password">Password</label>
                    <input type="password" name="password" id="password" required>
                </div>
                <button type="submit" class="submit-btn">Entrar</button>
            </form>
        </div>
    </div>
</body>
</html>'''

@app.route('/auth/login-page')
def auth_login_page():
    return render_template_string(LOGIN_TEMPLATE)

@app.route('/auth/login', methods=['POST'])
def auth_login():
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '').strip()
    
    if not email or not password:
        flash('Completa todos los campos', 'danger')
        return redirect(url_for('auth_login_page'))
    
    result = firebase_auth.login_user(email, password)
    
    if result['success']:
        firebase_auth.set_user_session(result['user_data'])
        flash(result['message'], 'success')
        return redirect(url_for('index'))
    else:
        flash(result['message'], 'danger')
        return redirect(url_for('auth_login_page'))

@app.route('/auth/logout')
def auth_logout():
    firebase_auth.clear_user_session()
    flash('Sesión cerrada', 'success')
    return redirect(url_for('auth_login_page'))

@app.route('/')
def index():
    if not firebase_auth.is_user_logged_in():
        return redirect(url_for('auth_login_page'))
    return redirect(url_for('search_page'))

@app.route('/search')
@login_required
def search_page():
    current_user = firebase_auth.get_current_user()
    user_name = html.escape(current_user['user_name'] if current_user else 'Usuario')
    
    image_available = GEMINI_READY and PIL_AVAILABLE
    
    content = f'''
    <div class="container">
        <div style="background: linear-gradient(45deg, #1e3c72, #2a5298); color: white; padding: 15px; border-radius: 8px; margin-bottom: 20px; text-align: center;">
            <h2>🔧 AutoParts Finder USA</h2>
            <p>Especializado en Repuestos Automotrices - {len(AUTOPARTS_SITES)} Sitios Verificados</p>
        </div>
        
        <div class="user-info">
            <span><strong>{user_name}</strong></span>
            <a href="{url_for('auth_logout')}" style="margin-left: 15px; background: #dc3545; color: white; padding: 6px 12px; border-radius: 4px; text-decoration: none;">Salir</a>
        </div>
        
        <h1>Buscar Autopartes</h1>
        <p class="subtitle">{'Búsqueda por texto o imagen' if image_available else 'Búsqueda por texto'} - Solo sitios autorizados</p>
        
        <form id="searchForm" enctype="multipart/form-data">
            <div class="search-bar">
                <input type="text" id="searchQuery" name="query" placeholder="Ej: brake pads Honda Civic, air filter Toyota...">
                <button type="submit">🔍 Buscar</button>
            </div>
            
            {'<div style="text-align: center; margin: 20px 0; color: #666;">O sube una imagen del repuesto</div>' if image_available else ''}
            
            {'<div class="image-upload"><input type="file" id="imageFile" name="image_file" accept="image/*"><label for="imageFile">📷 Identificar repuesto por imagen<br><small>JPG/PNG, máx 10MB</small></label><img id="imagePreview" class="image-preview"></div>' if image_available else ''}
        </form>
        
        <div class="tips">
            <h4>🔧 Sistema Especializado{'+ IA Visual:' if image_available else ':'}</h4>
            <ul style="margin: 8px 0 0 15px; font-size: 13px;">
                <li><strong>✅ Solo sitios autorizados:</strong> {len(AUTOPARTS_SITES)} tiendas verificadas</li>
                <li><strong>🏪 Incluye:</strong> RockAuto, AutoZone, O'Reilly, NAPA, CarParts.com</li>
                <li><strong>🚫 Excluye:</strong> Vendedores no autorizados</li>
                {'<li><strong>🤖 IA Visual:</strong> Identifica repuestos automáticamente</li>' if image_available else '<li><strong>⚠️ IA Visual:</strong> Configura GEMINI_API_KEY para activar</li>'}
            </ul>
        </div>
        
        <div id="loading" class="loading">
            <div class="spinner"></div>
            <h3>Buscando autopartes...</h3>
            <p id="loadingText">Filtrando sitios autorizados</p>
        </div>
        <div id="error" class="error"></div>
    </div>
    
    <script>
        let searching = false;
        const imageAvailable = {str(image_available).lower()};
        
        if (imageAvailable) {{
            document.getElementById('imageFile').addEventListener('change', function(e) {{
                const file = e.target.files[0];
                const preview = document.getElementById('imagePreview');
                
                if (file) {{
                    if (file.size > 10 * 1024 * 1024) {{
                        alert('
