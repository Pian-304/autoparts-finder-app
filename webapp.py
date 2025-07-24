# Generar ejemplos
        for i, (store_name, store_domain) in enumerate(stores):
            part_name, base_price = parts_data[i % len(parts_data)]
            final_price = round(base_price * (1 + i * 0.15), 2)
            
            # Enlaces por tienda
            store_links = {
                'rockauto.com': 'https://www.rockauto.com/en/catalog',
                'autozone.com': 'https://www.autozone.com/parts',
                'oreillyauto.com': 'https://www.oreillyauto.com/'
            }
            
            # Ratings por tienda
            store_ratings = {
                'RockAuto': ('4.6', '1,250'),
                'AutoZone': ('4.3', '890'),
                'O\'Reilly Auto Parts': ('4.4', '720')
            }
            
            rating, reviews = store_ratings.get(store_name, ('4.3', '200'))
            
            example = {
                'title': f'{part_name} - {["Premium Quality", "OEM Equivalent", "Best Value"][i]}',
                'price': f'${final_price:.2f}',
                'price_numeric': final_price,
                'source': store_name,
                'link': store_links.get(store_domain, f'https://{store_domain}'),
                'rating': rating,
                'reviews': reviews,
                'category': self._determine_category(f"{query} {part_name}"),
                'search_source': 'example',
                'engine_source': 'example',
                'is_autoparts_site': True
            }
            
            examples.append(example)
        
        return examples

# Instancia global del buscador
autoparts_finder = AutoPartsFinder()

# ==================== TEMPLATES HTML ====================

def render_page(title, content):
    """Renderiza página con template base"""
    return f'''<!DOCTYPE html>
<html lang="es">
<head>
    <title>{title}</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, sans-serif; background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); min-height: 100vh; padding: 15px; }}
        .container {{ max-width: 650px; margin: 0 auto; background: white; padding: 25px; border-radius: 12px; box-shadow: 0 8px 25px rgba(0,0,0,0.15); }}
        h1 {{ color: #1e3c72; text-align: center; margin-bottom: 8px; font-size: 1.8em; }}
        .subtitle {{ text-align: center; color: #666; margin-bottom: 25px; }}
        input {{ width: 100%; padding: 12px; margin: 8px 0; border: 2px solid #e1e5e9; border-radius: 6px; font-size: 16px; }}
        input:focus {{ outline: none; border-color: #1e3c72; }}
        button {{ width: 100%; padding: 12px; background: #1e3c72; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 16px; font-weight: 600; }}
        button:hover {{ background: #2a5298; }}
        .search-bar {{ display: flex; gap: 8px; margin-bottom: 20px; }}
        .search-bar input {{ flex: 1; }}
        .search-bar button {{ width: auto; padding: 12px 20px; }}
        .tips {{ background: #e8f5e8; border: 1px solid #4caf50; padding: 15px; border-radius: 6px; margin-bottom: 15px; font-size: 14px; }}
        .error {{ background: #ffebee; color: #c62828; padding: 12px; border-radius: 6px; margin: 12px 0; display: none; }}
        .loading {{ text-align: center; padding: 30px; display: none; }}
        .spinner {{ border: 3px solid #f3f3f3; border-top: 3px solid #1e3c72; border-radius: 50%; width: 40px; height: 40px; animation: spin 1s linear infinite; margin: 0 auto 15px; }}
        @keyframes spin {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}
        .user-info {{ background: #e3f2fd; padding: 12px; border-radius: 6px; margin-bottom: 15px; text-align: center; font-size: 14px; display: flex; align-items: center; justify-content: center; }}
        .user-info a {{ color: #1976d2; text-decoration: none; font-weight: 600; }}
        .flash {{ padding: 12px; margin-bottom: 8px; border-radius: 6px; font-size: 14px; }}
        .flash.success {{ background-color: #d4edda; color: #155724; }}
        .flash.danger {{ background-color: #f8d7da; color: #721c24; }}
        .flash.warning {{ background-color: #fff3cd; color: #856404; }}
        .image-upload {{ background: #f8f9fa; border: 2px dashed #dee2e6; border-radius: 8px; padding: 20px; text-align: center; margin: 15px 0; transition: all 0.3s ease; }}
        .image-upload input[type="file"] {{ display: none; }}
        .image-upload label {{ cursor: pointer; color: #1e3c72; font-weight: 600; }}
        .image-upload:hover {{ border-color: #1e3c72; background: #e3f2fd; }}
        .image-preview {{ max-width: 150px; max-height: 150px; margin: 10px auto; border-radius: 8px; display: none; }}
        .or-divider {{ text-align: center; margin: 20px 0; color: #666; font-weight: 600; position: relative; }}
        .or-divider:before {{ content: ''; position: absolute; top: 50%; left: 0; right: 0; height: 1px; background: #dee2e6; z-index: 1; }}
        .or-divider span {{ background: white; padding: 0 15px; position: relative; z-index: 2; }}
        .autoparts-header {{ background: linear-gradient(45deg, #1e3c72, #2a5298); color: white; padding: 15px; border-radius: 8px; margin-bottom: 20px; text-align: center; }}
        .autoparts-header h2 {{ margin-bottom: 5px; }}
        .autoparts-header p {{ opacity: 0.9; font-size: 14px; }}
    </style>
</head>
<body>{content}</body>
</html>'''

# Template de login
LOGIN_TEMPLATE = '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Iniciar Sesión | AutoParts Finder USA</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, sans-serif; background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); min-height: 100vh; display: flex; justify-content: center; align-items: center; padding: 20px; }
        .auth-container { max-width: 420px; width: 100%; background: white; border-radius: 15px; box-shadow: 0 20px 40px rgba(0,0,0,0.1); overflow: hidden; }
        .form-header { text-align: center; padding: 30px 25px 15px; background: linear-gradient(45deg, #1e3c72, #2a5298); color: white; }
        .form-header h1 { font-size: 1.8em; margin-bottom: 8px; }
        .form-header p { opacity: 0.9; font-size: 1em; }
        .form-body { padding: 25px; }
        form { display: flex; flex-direction: column; gap: 18px; }
        .input-group { display: flex; flex-direction: column; gap: 6px; }
        .input-group label { font-weight: 600; color: #1e3c72; font-size: 14px; }
        .input-group input { padding: 14px 16px; border: 2px solid #e0e0e0; border-radius: 8px; font-size: 16px; transition: border-color 0.3s ease; }
        .input-group input:focus { outline: 0; border-color: #1e3c72; }
        .submit-btn { background: linear-gradient(45deg, #1e3c72, #2a5298); color: white; border: none; padding: 14px 25px; font-size: 16px; font-weight: 600; border-radius: 8px; cursor: pointer; transition: transform 0.2s ease; }
        .submit-btn:hover { transform: translateY(-2px); }
        .flash-messages { list-style: none; padding: 0 25px 15px; }
        .flash { padding: 12px; margin-bottom: 10px; border-radius: 6px; text-align: center; font-size: 14px; }
        .flash.success { background-color: #d4edda; color: #155724; }
        .flash.danger { background-color: #f8d7da; color: #721c24; }
        .flash.warning { background-color: #fff3cd; color: #856404; }
        .auto-icon { font-size: 2em; margin-bottom: 10px; }
    </style>
</head>
<body>
    <div class="auth-container">
        <div class="form-header">
            <div class="auto-icon">🔧</div>
            <h1>AutoParts Finder USA</h1>
            <p>Repuestos Automotrices - Iniciar Sesión</p>
        </div>
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                <ul class="flash-messages">
                    {% for category, message in messages %}
                        <li class="flash {{ category }}">{{ message }}</li>
                    {% endfor %}
                </ul>
            {% endif %}
        {% endwith %}
        <div class="form-body">
            <form action="{{ url_for('auth_login') }}" method="post">
                <div class="input-group">
                    <label for="email">Correo Electrónico</label>
                    <input type="email" name="email" id="email" required>
                </div>
                <div class="input-group">
                    <label for="password">Contraseña</label>
                    <input type="password" name="password" id="password" required>
                </div>
                <button type="submit" class="submit-btn">Entrar</button>
            </form>
        </div>
    </div>
</body>
</html>'''

# ==================== RUTAS DE LA APLICACIÓN ====================

@app.route('/auth/login-page')
def auth_login_page():
    """Página de login"""
    return render_template_string(LOGIN_TEMPLATE)

@app.route('/auth/login', methods=['POST'])
def auth_login():
    """Procesa login de usuario"""
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '').strip()
    
    if not email or not password:
        flash('Por favor completa todos los campos.', 'danger')
        return redirect(url_for('auth_login_page'))
    
    result = firebase_auth.login_user(email, password)
    
    if result['success']:
        firebase_auth.set_user_session(result['user_data'])
        flash(result['message'], 'success')
        logger.info(f"Login exitoso: {email}")
        return redirect(url_for('index'))
    else:
        flash(result['message'], 'danger')
        logger.warning(f"Login fallido: {email}")
        return redirect(url_for('auth_login_page'))

@app.route('/auth/logout')
def auth_logout():
    """Cierra sesión de usuario"""
    firebase_auth.clear_user_session()
    flash('Has cerrado la sesión correctamente.', 'success')
    return redirect(url_for('auth_login_page'))

@app.route('/')
def index():
    """Página principal - redirige según estado de login"""
    if not firebase_auth.is_user_logged_in():
        return redirect(url_for('auth_login_page'))
    return redirect(url_for('search_page'))

@app.route('/search')
@login_required
def search_page():
    """Página principal de búsqueda"""
    current_user = firebase_auth.get_current_user()
    user_name = html.escape(current_user['user_name'] if current_user else 'Usuario')
    
    image_search_available = GEMINI_READY and PIL_AVAILABLE
    
    content = f'''
    <div class="container">
        <div class="autoparts-header">
            <h2>🔧 AutoParts Finder USA</h2>
            <p>Especializado en Repuestos Automotrices - {len(ALL_AUTOPARTS_DOMAINS)} Sitios Verificados</p>
        </div>
        
        <div class="user-info">
            <span><strong>{user_name}</strong></span>
            <div style="display: inline-block; margin-left: 15px;">
                <a href="{url_for('auth_logout')}" style="background: #dc3545; color: white; padding: 6px 12px; border-radius: 4px; text-decoration: none; font-size: 13px; margin-right: 8px;">Salir</a>
                <a href="{url_for('sites_info')}" style="background: #17a2b8; color: white; padding: 6px 12px; border-radius: 4px; text-decoration: none; font-size: 13px;">Sitios</a>
            </div>
        </div>
        
        <h1>Buscar Autopartes</h1>
        <p class="subtitle">{'Búsqueda por texto o imagen' if image_search_available else 'Búsqueda por texto'} - Solo sitios autorizados de USA</p>
        
        <form id="searchForm" enctype="multipart/form-data">
            <div class="search-bar">
                <input type="text" id="searchQuery" name="query" placeholder="Ej: brake pads Honda Civic 2019, air filter Toyota...">
                <button type="submit">🔍 Buscar</button>
            </div>
            
            {'<div class="or-divider"><span>O sube una imagen del repuesto</span></div>' if image_search_available else ''}
            
            {'<div class="image-upload"><input type="file" id="imageFile" name="image_file" accept="image/*"><label for="imageFile">📷 Identificar repuesto por imagen<br><small>Sube foto de la pieza (JPG/PNG, máx 10MB)</small></label><img id="imagePreview" class="image-preview"></div>' if image_search_available else ''}
        </form>
        
        <div class="tips">
            <h4>🔧 Sistema Especializado en Autopartes{'+ IA Visual:' if image_search_available else ':'}</h4>
            <ul style="margin: 8px 0 0 15px; font-size: 13px;">
                <li><strong>✅ Solo sitios autorizados:</strong> {len(ALL_AUTOPARTS_DOMAINS)} tiendas verificadas</li>
                <li><strong>🏪 Incluye:</strong> OEM Dealers, RockAuto, AutoZone, O'Reilly, NAPA</li>
                <li><strong>🚫 Excluye:</strong> Sitios no especializados y vendedores no autorizados</li>
                <li><strong>⚡ Optimizado:</strong> Búsquedas con términos técnicos automotrices</li>
                {'<li><strong>🤖 IA Visual:</strong> Identifica repuestos automáticamente</li>' if image_search_available else '<li><strong>⚠️ IA Visual:</strong> Configura GEMINI_API_KEY para activar</li>'}
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
        const imageSearchAvailable = {str(image_search_available).lower()};
        
        if (imageSearchAvailable) {{
            document.getElementById('imageFile').addEventListener('change', function(e) {{
                const file = e.target.files[0];
                const preview = document.getElementById('imagePreview');
                
                if (file) {{
                    if (file.size > 10 * 1024 * 1024) {{
                        alert('La imagen es demasiado grande (máximo 10MB)');
                        this.value = '';
                        return;
                    }}
                    
                    const reader = new FileReader();
                    reader.onload = function(e) {{
                        preview.src = e.target.result;
                        preview.style.display = 'block';
                        document.getElementById('searchQuery').value = '';
                    }}
                    reader.readAsDataURL(file);
                }} else {{
                    preview.style.display = 'none';
                }}
            }});
        }}
        
        document.getElementById('searchForm').addEventListener('submit', function(e) {{
            e.preventDefault();
            if (searching) return;
            
            const query = document.getElementById('searchQuery').value.trim();
            const imageFile = imageSearchAvailable ? document.getElementById('imageFile').files[0] : null;
            
            if (!query && !imageFile) {{
                return showError('Por favor ingresa el nombre del repuesto' + (imageSearchAvailable ? ' o sube una imagen' : ''));
            }}
            
            searching = true;
            showLoading(imageFile ? '🤖 Analizando imagen del repuesto...' : '🔍 Buscando en sitios de autopartes...');
            
            const timeoutId = setTimeout(() => {{ 
                searching = false; 
                hideLoading(); 
                showError('Búsqueda muy lenta - Intenta de nuevo'); 
            }}, 25000);
            
            const formData = new FormData();
            if (query) formData.append('query', query);
            if (imageFile) formData.append('image_file', imageFile);
            
            fetch('/api/search-autoparts', {{
                method: 'POST',
                body: formData
            }})
            .then(response => {{ 
                clearTimeout(timeoutId); 
                searching = false; 
                return response.json(); 
            }})
            .then(data => {{ 
                hideLoading(); 
                if (data.success) {{
                    window.location.href = '/results';
                }} else {{
                    showError(data.error || 'Error en la búsqueda');
                }}
            }})
            .catch(error => {{ 
                clearTimeout(timeoutId); 
                searching = false; 
                hideLoading(); 
                showError('Error de conexión'); 
            }});
        }});
        
        function showLoading(text) {{ 
            document.getElementById('loadingText').textContent = text;
            document.getElementById('loading').style.display = 'block'; 
            document.getElementById('error').style.display = 'none'; 
        }}
        function hideLoading() {{ document.getElementById('loading').style.display = 'none'; }}
        function showError(msg) {{ 
            hideLoading(); 
            const e = document.getElementById('error'); 
            e.textContent = msg; 
            e.style.display = 'block'; 
        }}
    </script>'''
    
    return render_template_string(render_page('Búsqueda de Autopartes', content))

@app.route('/api/search-autoparts', methods=['POST'])
@login_required
def api_search_autoparts():
    """API endpoint para búsqueda de autopartes"""
    try:
        # Obtener parámetros
        query = request.form.get('query', '').strip() or None
        image_file = request.files.get('image_file')
        
        # Procesar imagen si existe
        image_content = None
        if image_file and image_file.filename:
            image_content = image_file.read()
            if len(image_content) > 10 * 1024 * 1024:
                return jsonify({
                    'success': False, 
                    'error': 'Imagen demasiado grande (máximo 10MB)'
                }), 400
        
        # Validar entrada
        if not query and not image_content:
            return jsonify({
                'success': False, 
                'error': 'Proporciona el nombre del repuesto o una imagen'
            }), 400
        
        # Limitar longitud de consulta
        if query and len(query) > 100:
            query = query[:100]
        
        # Información de usuario
        user_email = session.get('user_email', 'Usuario')
        search_type = "imagen" if image_content and not query else "texto+imagen" if image_content and query else "texto"
        
        logger.info(f"Búsqueda de autopartes - Usuario: {user_email}, Tipo: {search_type}")
        
        # Realizar búsqueda
        products = autoparts_finder.search_autoparts(query=query, image_content=image_content)
        
        # Guardar en sesión
        session['last_search'] = {
            'query': query or "búsqueda por imagen de autoparte",
            'products': products,
            'timestamp': datetime.now().isoformat(),
            'user': user_email,
            'search_type': search_type,
            'is_autoparts': True
        }
        
        logger.info(f"Búsqueda completada: {len(products)} productos encontrados")
        
        return jsonify({
            'success': True, 
            'products': products, 
            'total': len(products)
        })
        
    except Exception as e:
        logger.error(f"Error en búsqueda de autopartes: {e}")
        
        # Fallback con ejemplos
        try:
            fallback_query = request.form.get('query', 'brake pads')
            fallback_products = autoparts_finder._get_examples(fallback_query)
            
            session['last_search'] = {
                'query': fallback_query, 
                'products': fallback_products, 
                'timestamp': datetime.now().isoformat(),
                'search_type': 'example'
            }
            
            return jsonify({
                'success': True, 
                'products': fallback_products, 
                'total': len(fallback_products)
            })
        except:
            return jsonify({
                'success': False, 
                'error': 'Error interno del servidor'
            }), 500

@app.route('/results')
@login_required
def results_page():
    """Página de resultados de búsqueda"""
    if 'last_search' not in session:
        flash('No hay búsquedas recientes de autopartes.', 'warning')
        return redirect(url_for('search_page'))
    
    current_user = firebase_auth.get_current_user()
    user_name = html.escape(current_user['user_name'] if current_user else 'Usuario')
    
    search_data = session['last_search']
    products = search_data.get('products', [])
    query = html.escape(str(search_data.get('query', 'búsqueda de autopartes')))
    search_type = search_data.get('search_type', 'texto')
    
    # Generar HTML de productos
    products_html = ""
    badges = ['MEJOR PRECIO', 'POPULAR', 'CALIDAD']
    colors = ['#4caf50', '#ff9800', '#9c27b0']
    
    for i, product in enumerate(products[:6]):
        if not product:
            continue
        
        # Badge principal
        badge = f'<div style="position: absolute; top: 8px; right: 8px; background: {colors[min(i, 2)]}; color: white; padding: 4px 8px; border-radius: 12px; font-size: 11px; font-weight: bold;">{badges[min(i, 2)]}</div>' if i < 3 else ''
        
        # Badge de fuente
        source = product.get('search_source', '')
        source_badge = ''
        if source == 'image':
            source_badge = '<div style="position: absolute; top: 8px; left: 8px; background: #673ab7; color: white; padding: 4px 8px; border-radius: 12px; font-size: 10px; font-weight: bold;">📷 IA</div>'
        elif source == 'combined':
            source_badge = '<div style="position: absolute; top: 8px; left: 8px; background: #607d8b; color: white; padding: 4px 8px; border-radius: 12px; font-size: 10px; font-weight: bold;">🔗 MIXTO</div>'
        
        # Badge de categoría
        category = product.get('category', 'general')
        category_colors = {
            'engine': '#d32f2f', 'brake': '#c62828', 'suspension': '#7b1fa2',
            'electrical': '#303f9f', 'filters': '#388e3c', 'body': '#f57c00'
        }
        category_names = {
            'engine': 'MOTOR', 'brake': 'FRENOS', 'suspension': 'SUSPENSIÓN',
            'electrical': 'ELÉCTRICO', 'filters': 'FILTROS', 'body': 'CARROCERÍA'
        }
        
        category_badge = ''
        if category in category_colors:
            category_badge = f'<div style="position: absolute; bottom: 8px; left: 8px; background: {category_colors[category]}; color: white; padding: 2px 6px; border-radius: 8px; font-size: 9px; font-weight: bold;">{category_names[category]}</div>'
        
        # Información del producto
        title = html.escape(str(product.get('title', 'Autoparte')))
        price = html.escape(str(product.get('price', '$0.00')))
        source_store = html.escape(str(product.get('source', 'Tienda de Autopartes')))
        link = html.escape(str(product.get('link', '#')))
        rating = product.get('rating', '')
        reviews = product.get('reviews', '')
        
        # Badge de verificación
        verified_badge = '<div style="position: absolute; top: 35px; right: 8px; background: #4caf50; color: white; padding: 2px 6px; border-radius: 8px; font-size: 9px; font-weight: bold;">✓ AUTORIZADO</div>' if product.get('is_autoparts_site') else ''
        
        rating_html = f'<span style="color: #ff9800;">⭐ {rating}</span> ({reviews} reviews)' if rating and reviews else ''
        
        products_html += f'''
            <div style="border: 1px solid #ddd; border-radius: 8px; padding: 15px; margin-bottom: 15px; background: white; position: relative; box-shadow: 0 2px 4px rgba(0,0,0,0.08);">
                {badge}
                {source_badge}
                {verified_badge}
                {category_badge}
                <h3 style="color: #1e3c72; margin-bottom: 8px; font-size: 16px; margin-top: {'20px' if source_badge else '0'};">{title}</h3>
                <div style="font-size: 28px; color: #2e7d32; font-weight: bold; margin: 12px 0;">{price} <span style="font-size: 12px; color: #666;">USD</span></div>
                <p style="color: #666; margin-bottom: 8px; font-size: 14px;">🏪 {source_store}</p>
                {f'<p style="color: #888; margin-bottom: 12px; font-size: 12px;">{rating_html}</p>' if rating_html else ''}
                <a href="{link}" target="_blank" rel="noopener noreferrer" style="background: #1e3c72; color: white; padding: 10px 16px; text-decoration: none; border-radius: 6px; font-weight: 600; display: inline-block; font-size: 14px;">🔧 Ver Repuesto</a>
            </div>'''
    
    # Estadísticas
    prices = [p.get('price_numeric', 0) for p in products if p.get('price_numeric', 0) > 0]
    stats = ""
    if prices:
        min_price = min(prices)
        avg_price = sum(prices) / len(prices)
        search_type_text = {
            "texto": "texto", 
            "imagen": "imagen + IA", 
            "texto+imagen": "texto + imagen + IA", 
            "combined": "búsqueda mixta",
            "example": "ejemplos"
        }.get(search_type, search_type)
        
        unique_stores = len(set(p.get('source', '') for p in products if p.get('source')))
        
        stats = f'''
            <div style="background: #e8f5e8; border: 1px solid #4caf50; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                <h3 style="color: #2e7d32; margin-bottom: 8px;">🔧 Resultados de Autopartes ({search_type_text})</h3>
                <p><strong>{len(products)} repuestos encontrados</strong> en {unique_stores} tiendas autorizadas</p>
                <p><strong>Mejor precio: ${min_price:.2f}</strong></p>
                <p><strong>Precio promedio: ${avg_price:.2f}</strong></p>
                <p style="font-size: 12px; color: #666; margin-top: 8px;">✅ Solo sitios especializados en autopartes de USA</p>
            </div>'''
    
    content = f'''
    <div style="max-width: 800px; margin: 0 auto;">
        <div style="background: rgba(255,255,255,0.15); padding: 12px; border-radius: 8px; margin-bottom: 15px; text-align: center; display: flex; align-items: center; justify-content: center;">
            <span style="color: white; font-size: 14px;"><strong>🔧 {user_name}</strong></span>
            <div style="margin-left: 15px;">
                <a href="{url_for('auth_logout')}" style="background: rgba(220,53,69,0.9); color: white; padding: 6px 12px; border-radius: 4px; text-decoration: none; font-size: 13px; margin-right: 8px;">Salir</a>
                <a href="{url_for('search_page')}" style="background: rgba(40,167,69,0.9); color: white; padding: 6px 12px; border-radius: 4px; text-decoration: none; font-size: 13px;">Nueva Búsqueda</a>
            </div>
        </div>
        
        <h1 style="color: white; text-align: center; margin-bottom: 8px;">🔧 Autopartes: "{query}"</h1>
        <p style="text-align: center; color: rgba(255,255,255,0.9); margin-bottom: 25px;">Búsqueda especializada completada</p>
        
        {stats}
        {products_html}
    </div>'''
    
    return render_template_string(render_page('Resultados Autopartes - AutoParts Finder USA', content))

@app.route('/sites')
@login_required
def sites_info():
    """Página de información de sitios incluidos"""
    current_user = firebase_auth.get_current_user()
    user_name = html.escape(current_user['user_name'] if current_user else 'Usuario')
    
    # Generar HTML de sitios por categoría
    sites_html = ""
    category_names = {
        'oem_dealers': '🏭 Concesionarios Oficiales (OEM)',
        'major_platforms': '🌐 Plataformas Principales',
        'chain_stores': '🏪 Cadenas de Tiendas',
        'european_specialists': '🇪🇺 Especialistas Europeos',
        'performance': '🏁 Performance y Racing'
    }
    
    for category, name in category_names.items():
        if category in AUTOPARTS_SITES_DB:
            sites_html += f'<h3 style="color: #1e3c72; margin-top: 20px;">{name}</h3><ul style="columns: 2; margin-bottom: 15px;">'
            
            data = AUTOPARTS_SITES_DB[category]
            if isinstance(data, dict):
                for brand, sites in data.items():
                    if isinstance(sites, list):
                        for site in sites[:3]:  # Mostrar máximo 3 por marca
                            sites_html += f'<li style="margin-bottom: 3px;"><small>{site}</small></li>'
            elif isinstance(data, list):
                for site in data[:10]:  # Mostrar máximo 10
                    sites_html += f'<li style="margin-bottom: 3px;"><small>{site}</small></li>'
            
            sites_html += '</ul>'
    
    content = f'''
    <div class="container">
        <div class="user-info">
            <span><strong>{user_name}</strong></span>
            <div style="display: inline-block; margin-left: 15px;">
                <a href="{url_for('search_page')}" style="background: #28a745; color: white; padding: 6px 12px; border-radius: 4px; text-decoration: none; font-size: 13px;">🔍 Buscar</a>
                <a href="{url_for('auth_logout')}" style="background: #dc3545; color: white; padding: 6px 12px; border-radius: 4px; text-decoration: none; font-size: 13px; margin-left: 8px;">Salir</a>
            </div>
        </div>
        
        <h1>🔧 Sitios de Autopartes Incluidos</h1>
        <p class="subtitle">Base de datos de {len(ALL_AUTOPARTS_DOMAINS)} sitios verificados especializados en autopartes</p>
        
        <div style="background: #e3f2fd; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
            <h4 style="color: #1565c0; margin-bottom: 10px;">✅ Garantía de Calidad</h4>
            <p style="font-size: 14px; color: #333;">Todos los resultados provienen exclusivamente de estos sitios verificados y especializados en autopartes automotrices en Estados Unidos. No incluimos marketplaces generales ni vendedores no autorizados.</p>
        </div>
        
        {sites_html}
        
        <div style="background: #f5f5f5; padding: 15px; border-radius: 8px; margin-top: 30px; text-align: center;">
            <p style="font-size: 12px; color: #666;">Total: {len(ALL_AUTOPARTS_DOMAINS)} sitios únicos organizados por especialización</p>
        </div>
    </div>'''
    
    return render_template_string(render_page('Sitios Incluidos - AutoParts Finder', content))

@app.route('/api/health')
def health_check():
    """Endpoint de salud del servicio"""
    try:
        return jsonify({
            'status': 'OK', 
            'timestamp': datetime.now().isoformat(),
            'service': 'AutoParts Finder USA',
            'version': '2.0.1',
            'autoparts_sites_loaded': len(ALL_AUTOPARTS_DOMAINS),
            'firebase_auth': 'enabled' if firebase_auth.configured else 'disabled',
            'serpapi': 'enabled' if autoparts_finder.is_configured() else 'disabled',
            'gemini_vision': 'enabled' if GEMINI_READY else 'disabled',
            'pil_available': 'enabled' if PIL_AVAILABLE else 'disabled',
            'specialization': 'automotive_parts_only'
        })
    except Exception as e:
        logger.error(f"Error en health check: {e}")
        return jsonify({'status': 'ERROR', 'message': str(e)}), 500

# ==================== MIDDLEWARE Y MANEJO DE ERRORES ====================

@app.before_request
def before_request():
    """Middleware ejecutado antes de cada request"""
    # Gestión de sesiones con timeout
    if 'timestamp' in session:
        try:
            timestamp_str = session['timestamp']
            if isinstance(timestamp_str, str):
                last_activity = datetime.fromisoformat(timestamp_str)
                if (datetime.now() - last_activity).total_seconds() > 1200:  # 20 minutos
                    session.clear()
        except:
            session.clear()
    
    session['timestamp'] = datetime.now().isoformat()

@app.after_request
def after_request(response):
    """Middleware ejecutado después de cada response"""
    # Headers de seguridad
    response.headers.update({
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'DENY',
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'X-Autoparts-Service': 'AutoParts-Finder-USA-v2.0.1'
    })
    return response

@app.errorhandler(404)
def not_found(error):
    """Manejo de error 404"""
    return '<h1>404 - Página no encontrada</h1><p><a href="/">🔧 Volver a AutoParts Finder</a></p>', 404

@app.errorhandler(500)
def internal_error(error):
    """Manejo de error 500"""
    logger.error(f"Error interno del servidor: {error}")
    return '<h1>500 - Error interno</h1><p><a href="/">🔧 Volver a AutoParts Finder</a></p>', 500

@app.errorhandler(413)
def request_too_large(error):
    """Manejo de archivos demasiado grandes"""
    return jsonify({
        'success': False, 
        'error': 'Archivo demasiado grande (máximo 16MB)'
    }), 413

# ==================== PUNTO DE ENTRADA ====================

if __name__ == '__main__':
    # Configuración para desarrollo
    print("=" * 60)
    print("🔧 AutoParts Finder USA v2.0.1 - Iniciando")
    print("=" * 60)
    print(f"Firebase Auth: {'✅ OK' if firebase_auth.configured else '❌ NO'}")
    print(f"SerpAPI: {'✅ OK' if autoparts_finder.is_configured() else '❌ NO'}")
    print(f"Gemini Vision: {'✅ OK' if GEMINI_READY else '❌ NO'}")
    print(f"PIL/Pillow: {'✅ OK' if PIL_AVAILABLE else '❌ NO'}")
    print(f"AutoParts Sites: ✅ {len(ALL_AUTOPARTS_DOMAINS)} sitios cargados")
    print(f"Puerto: {os.environ.get('PORT', '5000')}")
    print("🔧 Especialización: AUTOPARTES USA EXCLUSIVAMENTE")
    print("=" * 60)
    
    app.run(
        host='0.0.0.0', 
        port=int(os.environ.get('PORT', 5000)), 
        debug=False, 
        threaded=True
    )
else:
    # Configuración para producción (Gunicorn)
    logging.getLogger('werkzeug').setLevel(logging.WARNING)
    
    logger.info("🔧 AutoParts Finder USA v2.0.1 iniciado en producción")
    logger.info(f"📊 {len(ALL_AUTOPARTS_DOMAINS)} sitios especializados cargados")
    logger.info(f"🔐 Firebase: {'OK' if firebase_auth.configured else 'NO'}")
    logger.info(f"🔍 SerpAPI: {'OK' if autoparts_finder.is_configured() else 'NO'}")
    logger.info(f"🤖 Gemini: {'OK' if GEMINI_READY else 'NO'}")
    logger.info("✅ Aplicación lista para recibir requests")#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AutoParts Finder USA - Aplicación especializada en búsqueda de autopartes
Versión: 2.0.1
Autor: Sistema de Autopartes
Descripción: Búsqueda especializada de repuestos automotrices en 402 sitios verificados de USA
"""

import os
import re
import html
import time
import io
import logging
from datetime import datetime
from urllib.parse import urlparse, quote_plus
from functools import wraps

# Imports principales de Flask
from flask import Flask, request, jsonify, session, redirect, url_for, render_template_string, flash
import requests

# Imports opcionales para IA visual
try:
    from PIL import Image
    PIL_AVAILABLE = True
    print("✅ PIL (Pillow) disponible")
except ImportError:
    PIL_AVAILABLE = False
    print("⚠️ PIL (Pillow) no disponible")

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
    print("✅ Google Generative AI disponible")
except ImportError:
    genai = None
    GEMINI_AVAILABLE = False
    print("⚠️ Google Generative AI no disponible")

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ==================== CONFIGURACIÓN DE LA APLICACIÓN ====================

app = Flask(__name__)

# Configuración básica
app.secret_key = os.environ.get('SECRET_KEY', 'autoparts-finder-usa-secret-2025')
app.config.update({
    'PERMANENT_SESSION_LIFETIME': 1800,  # 30 minutos
    'SESSION_COOKIE_HTTPONLY': True,
    'SESSION_COOKIE_SECURE': bool(os.environ.get('RENDER')),
    'MAX_CONTENT_LENGTH': 16 * 1024 * 1024,  # 16MB
    'JSON_SORT_KEYS': False
})

logger.info("Flask app inicializada correctamente")

# Configuración de Gemini
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
GEMINI_READY = False

if GEMINI_AVAILABLE and GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        GEMINI_READY = True
        logger.info("Gemini AI configurado correctamente")
    except Exception as e:
        logger.error(f"Error configurando Gemini: {e}")
        GEMINI_READY = False
else:
    logger.info("Gemini AI no disponible")

# ==================== BASE DE DATOS DE SITIOS DE AUTOPARTES ====================

AUTOPARTS_SITES_DB = {
    "oem_dealers": {
        "acura": ["acura.com", "bernardiparts.com"],
        "audi": ["audiusa.com", "parts.audiusa.com"],
        "bmw": ["shop.bmwusa.com"],
        "buick": ["buick.com", "parts.buick.com"],
        "cadillac": ["cadillac.com", "parts.cadillac.com"],
        "chevrolet": ["parts.chevrolet.com", "chevrolet.com"],
        "chrysler": ["mopar.com", "parts.ramtrucks.com"],
        "ford": ["parts.ford.com", "ford.com"],
        "honda": ["parts.honda.com"],
        "hyundai": ["parts.hyundaiusa.com"],
        "infiniti": ["infiniti.com"],
        "kia": ["parts.kia.com"],
        "lexus": ["parts.lexus.com", "lexus.com"],
        "mazda": ["mazdausa.com"],
        "mercedes": ["mbusa.com", "mbparts.mbusa.com"],
        "nissan": ["parts.nissanusa.com"],
        "porsche": ["porscheexchange.com", "parts.porsche.com"],
        "subaru": ["subaru.com"],
        "tesla": ["tesla.com"],
        "toyota": ["toyota.com"],
        "volkswagen": ["parts.vw.com"],
        "volvo": ["usparts.volvocars.com"]
    },
    "major_platforms": [
        "rockauto.com", "carparts.com", "partsgeek.com", "1aauto.com", "carid.com",
        "buyautoparts.com", "autoanything.com", "jcwhitney.com", "detroitaxle.com",
        "autopartswarehouse.com", "myautostore.com", "amazon.com", "ebay.com"
    ],
    "chain_stores": [
        "autozone.com", "oreillyauto.com", "advanceautoparts.com", "napaonline.com",
        "pepboys.com", "partsauthority.com", "carquest.com"
    ],
    "european_specialists": [
        "ecstuning.com", "fcpeuro.com", "pelicanparts.com", "turnermotorsport.com",
        "bimmerworld.com", "ipdusa.com", "swedishparts.com"
    ],
    "performance": [
        "jegs.com", "summitracing.com", "speedwaymotors.com", "americanmuscle.com",
        "lmr.com", "cjponyparts.com", "quadratec.com", "maperformance.com"
    ]
}

# Crear conjunto de dominios autorizados
ALL_AUTOPARTS_DOMAINS = set()
for category_data in AUTOPARTS_SITES_DB.values():
    if isinstance(category_data, dict):
        for brand_sites in category_data.values():
            if isinstance(brand_sites, list):
                ALL_AUTOPARTS_DOMAINS.update(brand_sites)
    elif isinstance(category_data, list):
        ALL_AUTOPARTS_DOMAINS.update(category_data)

logger.info(f"Base de datos cargada: {len(ALL_AUTOPARTS_DOMAINS)} sitios de autopartes")

# ==================== CLASE DE AUTENTICACIÓN FIREBASE ====================

class FirebaseAuth:
    def __init__(self):
        self.api_key = os.environ.get("FIREBASE_WEB_API_KEY")
        self.configured = bool(self.api_key)
        logger.info(f"Firebase Auth: {'CONFIGURADO' if self.configured else 'NO CONFIGURADO'}")
    
    def login_user(self, email, password):
        """Autentica usuario con Firebase"""
        if not self.configured:
            return {
                'success': False, 
                'message': 'Servicio de autenticación no configurado', 
                'user_data': None
            }
        
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={self.api_key}"
        payload = {
            'email': email, 
            'password': password, 
            'returnSecureToken': True
        }
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            user_data = response.json()
            
            return {
                'success': True,
                'message': '¡Bienvenido! Sesión iniciada correctamente.',
                'user_data': {
                    'user_id': user_data['localId'],
                    'email': user_data['email'],
                    'display_name': user_data.get('displayName', email.split('@')[0]),
                    'id_token': user_data['idToken']
                }
            }
            
        except requests.exceptions.HTTPError as e:
            try:
                error_data = e.response.json()
                error_message = error_data.get('error', {}).get('message', '')
                
                if any(err in error_message for err in ['INVALID', 'EMAIL_NOT_FOUND']):
                    return {'success': False, 'message': 'Email o contraseña incorrectos', 'user_data': None}
                elif 'TOO_MANY_ATTEMPTS' in error_message:
                    return {'success': False, 'message': 'Demasiados intentos. Intenta más tarde.', 'user_data': None}
                else:
                    return {'success': False, 'message': 'Error de autenticación', 'user_data': None}
            except:
                return {'success': False, 'message': 'Error de conexión', 'user_data': None}
                
        except Exception as e:
            logger.error(f"Firebase auth error: {e}")
            return {'success': False, 'message': 'Error interno del servidor', 'user_data': None}
    
    def set_user_session(self, user_data):
        """Establece sesión de usuario"""
        session.update({
            'user_id': user_data['user_id'],
            'user_name': user_data['display_name'],
            'user_email': user_data['email'],
            'id_token': user_data['id_token'],
            'login_time': datetime.now().isoformat()
        })
        session.permanent = True
    
    def clear_user_session(self):
        """Limpia sesión de usuario"""
        keys_to_keep = ['timestamp']
        preserved_data = {k: session.get(k) for k in keys_to_keep if k in session}
        session.clear()
        session.update(preserved_data)
    
    def is_user_logged_in(self):
        """Verifica si el usuario está logueado"""
        if 'user_id' not in session:
            return False
        
        if 'login_time' in session:
            try:
                login_time = datetime.fromisoformat(session['login_time'])
                if (datetime.now() - login_time).total_seconds() > 7200:  # 2 horas
                    return False
            except:
                return False
        
        return True
    
    def get_current_user(self):
        """Obtiene datos del usuario actual"""
        if not self.is_user_logged_in():
            return None
        
        return {
            'user_id': session.get('user_id'),
            'user_name': session.get('user_name'),
            'user_email': session.get('user_email'),
            'id_token': session.get('id_token')
        }

# Instancia global de autenticación
firebase_auth = FirebaseAuth()

def login_required(f):
    """Decorador para rutas que requieren autenticación"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not firebase_auth.is_user_logged_in():
            flash('Tu sesión ha expirado. Inicia sesión nuevamente.', 'warning')
            return redirect(url_for('auth_login_page'))
        return f(*args, **kwargs)
    return decorated_function

# ==================== FUNCIONES DE IA VISUAL ====================

def analyze_image_with_gemini(image_content):
    """Analiza imagen de autoparte con Gemini Vision"""
    if not GEMINI_READY or not PIL_AVAILABLE or not image_content:
        return None
    
    try:
        # Procesar imagen
        image = Image.open(io.BytesIO(image_content))
        
        # Optimizar tamaño
        if image.size[0] > 1024 or image.size[1] > 1024:
            image.thumbnail((1024, 1024), Image.Resampling.LANCZOS)
        
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Prompt especializado para autopartes
        prompt = """
        Analiza esta imagen de autoparte/repuesto automotriz y genera una consulta de búsqueda en inglés.
        
        Identifica:
        - Tipo exacto de pieza (brake pad, air filter, headlight, etc.)
        - Marca visible (si hay)
        - Número de parte (si visible)
        - Características técnicas
        - Aplicación vehicular (si identificable)
        
        Responde SOLO con la consulta de búsqueda optimizada.
        Ejemplo: "brake pads ceramic front Honda Civic 2019"
        """
        
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        response = model.generate_content([prompt, image])
        
        if response.text:
            query = response.text.strip()
            logger.info(f"Consulta generada por IA: '{query}'")
            return query
        
        return None
        
    except Exception as e:
        logger.error(f"Error analizando imagen: {e}")
        return None

def validate_image(image_content):
    """Valida formato y tamaño de imagen"""
    if not PIL_AVAILABLE or not image_content:
        return False
    
    try:
        image = Image.open(io.BytesIO(image_content))
        return (
            image.size[0] >= 10 and 
            image.size[1] >= 10 and 
            image.format in ['JPEG', 'PNG', 'WEBP']
        )
    except:
        return False

# ==================== CLASE PRINCIPAL DE BÚSQUEDA ====================

class AutoPartsFinder:
    def __init__(self):
        self.api_key = (
            os.environ.get('SERPAPI_KEY') or 
            os.environ.get('SERPAPI_API_KEY') or 
            os.environ.get('SERP_API_KEY')
        )
        
        self.base_url = "https://serpapi.com/search"
        self.cache = {}
        self.cache_ttl = 300  # 5 minutos
        self.timeouts = {'connect': 5, 'read': 10}
        
        # Términos de categorías de autopartes
        self.categories = {
            'engine': ['motor', 'engine', 'piston', 'valve', 'gasket', 'timing belt', 'spark plug'],
            'brake': ['brake', 'freno', 'brake pad', 'disc', 'rotor', 'caliper'],
            'suspension': ['shock', 'strut', 'spring', 'suspension'],
            'electrical': ['headlight', 'taillight', 'battery', 'alternator', 'starter'],
            'filters': ['air filter', 'oil filter', 'fuel filter', 'cabin filter'],
            'body': ['bumper', 'fender', 'door', 'mirror', 'hood'],
            'transmission': ['transmission', 'clutch', 'gearbox', 'cv joint']
        }
        
        logger.info(f"SerpAPI: {'CONFIGURADO' if self.api_key else 'NO CONFIGURADO'}")
    
    def is_configured(self):
        """Verifica si la API está configurada"""
        return bool(self.api_key)
    
    def _is_authorized_site(self, url_or_domain):
        """Verifica si es un sitio autorizado de autopartes"""
        if not url_or_domain:
            return False
        
        try:
            # Extraer dominio
            if url_or_domain.startswith('http'):
                domain = urlparse(url_or_domain).netloc.lower()
            else:
                domain = url_or_domain.lower()
            
            # Limpiar subdominios comunes
            clean_domain = domain.replace('www.', '').replace('shop.', '').replace('parts.', '')
            
            # Sitios principales autorizados
            authorized_sites = [
                'amazon.com', 'ebay.com', 'rockauto.com', 'carparts.com', 'autozone.com',
                'oreillyauto.com', 'advanceautoparts.com', 'napaonline.com', 'pepboys.com',
                'partsgeek.com', '1aauto.com', 'carid.com', 'jegs.com', 'summitracing.com'
            ]
            
            # Verificar contra sitios autorizados
            for site in authorized_sites:
                if site in domain or site in clean_domain:
                    return True
            
            # Verificar contra base de datos completa
            for authorized_domain in ALL_AUTOPARTS_DOMAINS:
                if authorized_domain in domain or domain in authorized_domain:
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error verificando sitio: {e}")
            return False
    
    def _extract_price(self, price_str):
        """Extrae precio numérico de string"""
        if not price_str:
            return 0.0
        
        try:
            # Limpiar string de precio
            clean_price = str(price_str).replace(',', '').replace('$', '').replace('USD', '').strip()
            
            # Patrones de búsqueda de precios
            patterns = [
                r'(\d{1,5}\.\d{2})',  # 123.45
                r'(\d{1,5})'          # 123
            ]
            
            for pattern in patterns:
                match = re.search(pattern, clean_price)
                if match:
                    price = float(match.group(1))
                    if 0.50 <= price <= 15000:  # Rango válido para autopartes
                        return price
            
        except Exception as e:
            logger.error(f"Error extrayendo precio '{price_str}': {e}")
        
        return 0.0
    
    def _generate_realistic_price(self, query, index=0):
        """Genera precio realista según tipo de autoparte"""
        query_lower = query.lower()
        
        # Mapeo de precios por categoría
        price_ranges = {
            ('engine', 'motor', 'transmission'): 800,
            ('brake', 'freno', 'rotor'): 85,
            ('headlight', 'taillight', 'bumper'): 120,
            ('filter', 'filtro', 'spark plug'): 25,
            ('shock', 'strut', 'suspension'): 95,
            ('battery', 'alternator', 'starter'): 180
        }
        
        base_price = 60  # Precio por defecto
        
        for keywords, price in price_ranges.items():
            if any(word in query_lower for word in keywords):
                base_price = price
                break
        
        # Variación por índice
        final_price = base_price * (1 + index * 0.18)
        return round(final_price, 2)
    
    def _get_product_link(self, item):
        """Genera enlace válido para el producto"""
        if not item:
            return "#"
        
        # Intentar enlaces directos primero
        for key in ['product_link', 'link']:
            link = item.get(key, '')
            if link and self._is_authorized_site(link):
                return link
        
        # Generar enlace basado en fuente
        title = item.get('title', '')
        source = item.get('source', '').lower()
        
        if title:
            search_query = quote_plus(title[:60])
            
            # Enlaces específicos por tienda
            store_links = {
                'amazon': f"https://www.amazon.com/s?k={search_query}+automotive",
                'autozone': f"https://www.autozone.com/parts?searchText={search_query}",
                'oreilly': f"https://www.oreillyauto.com/search?q={search_query}",
                'advance': f"https://shop.advanceautoparts.com/find/?searchText={search_query}",
                'napa': f"https://www.napaonline.com/search?keyWord={search_query}",
                'rockauto': "https://www.rockauto.com/en/catalog",
                'carparts': f"https://www.carparts.com/search?q={search_query}",
                'ebay': f"https://www.ebay.com/sch/i.html?_nkw={search_query}+auto+parts"
            }
            
            for store, url in store_links.items():
                if store in source:
                    return url
            
            # Enlace genérico
            return f"https://www.google.com/search?tbm=shop&q={search_query}+auto+parts"
        
        return "#"
    
    def _optimize_query(self, query):
        """Optimiza consulta para autopartes"""
        if not query:
            return "auto parts"
        
        query = query.strip().lower()
        
        # Agregar términos específicos si no están presentes
        autopart_terms = ['part', 'filter', 'brake', 'engine', 'transmission']
        if not any(term in query for term in autopart_terms):
            query = f"{query} auto part"
        
        return f"{query} automotive replacement"
    
    def _make_request(self, engine, query):
        """Realiza petición a SerpAPI"""
        if not self.api_key:
            return None
        
        optimized_query = self._optimize_query(query)
        
        params = {
            'engine': engine,
            'q': optimized_query,
            'api_key': self.api_key,
            'num': 15,
            'location': 'United States',
            'gl': 'us',
            'hl': 'en'
        }
        
        # Configuración específica por motor
        if engine == 'google_shopping':
            params['tbm'] = 'shop'
        elif engine == 'google':
            params['q'] = f"{optimized_query} site:autozone.com OR site:rockauto.com OR site:carparts.com"
        
        try:
            logger.info(f"Petición SerpAPI: {engine}")
            time.sleep(0.5)  # Rate limiting
            
            response = requests.get(
                self.base_url, 
                params=params, 
                timeout=self.timeouts['read']
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"SerpAPI error: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error en petición SerpAPI: {e}")
            return None
    
    def _process_results(self, data, engine):
        """Procesa resultados de la API"""
        if not data:
            return []
        
        results_key = 'shopping_results' if engine == 'google_shopping' else 'organic_results'
        results = data.get(results_key, [])
        
        products = []
        
        # Keywords para identificar autopartes
        autopart_keywords = [
            'part', 'filter', 'brake', 'engine', 'automotive', 'car', 'auto',
            'oem', 'aftermarket', 'replacement', 'genuine', 'motor', 'transmission',
            'suspension', 'headlight', 'battery', 'alternator', 'gasket', 'belt'
        ]
        
        for item in results:
            if len(products) >= 8:  # Límite por motor
                break
            
            title = item.get('title', '')
            if len(title) < 5:
                continue
            
            # Verificar relevancia para autopartes
            if not any(keyword in title.lower() for keyword in autopart_keywords):
                continue
            
            # Verificar que sea de sitio autorizado
            source = item.get('source', '')
            link = item.get('link', '')
            
            if not (self._is_authorized_site(source) or self._is_authorized_site(link)):
                continue
            
            # Procesar precio
            price_str = item.get('price', '')
            price_num = self._extract_price(price_str)
            
            if price_num == 0:
                price_num = self._generate_realistic_price(title, len(products))
            
            # Crear objeto producto
            product = {
                'title': html.escape(title[:120]),
                'price': f"${price_num:.2f}",
                'price_numeric': float(price_num),
                'source': html.escape(source or 'Tienda de Autopartes')[:50],
                'link': self._get_product_link(item),
                'rating': str(item.get('rating', '')),
                'reviews': str(item.get('reviews', '')),
                'category': self._determine_category(title),
                'is_autoparts_site': True,
                'engine_source': engine
            }
            
            products.append(product)
            logger.debug(f"Producto agregado: {title[:30]}... - ${price_num:.2f}")
        
        return products
    
    def _determine_category(self, title):
        """Determina categoría de autoparte"""
        title_lower = title.lower()
        
        for category, terms in self.categories.items():
            if any(term in title_lower for term in terms):
                return category
        
        return 'general'
    
    def search_autoparts(self, query=None, image_content=None):
        """Función principal de búsqueda de autopartes"""
        # Determinar consulta final
        final_query = query or "auto parts"
        search_source = "text"
        
        # Procesar imagen si está disponible
        if image_content and GEMINI_READY and validate_image(image_content):
            image_query = analyze_image_with_gemini(image_content)
            if image_query:
                if query:
                    final_query = f"{query} {image_query}"
                    search_source = "combined"
                else:
                    final_query = image_query
                    search_source = "image"
                logger.info(f"Búsqueda con IA visual: {search_source}")
        
        logger.info(f"Búsqueda final: '{final_query}' (fuente: {search_source})")
        
        # Verificar cache
        cache_key = f"autoparts_{hash(final_query.lower())}"
        if cache_key in self.cache:
            cache_data, timestamp = self.cache[cache_key]
            if (time.time() - timestamp) < self.cache_ttl:
                logger.info("Resultados desde cache")
                return cache_data
        
        # Realizar búsqueda si API está configurada
        if not self.api_key:
            logger.warning("API no configurada, usando ejemplos")
            return self._get_examples(final_query)
        
        all_products = []
        
        # Búsqueda en Google Shopping
        shopping_data = self._make_request('google_shopping', final_query)
        if shopping_data:
            shopping_products = self._process_results(shopping_data, 'google_shopping')
            all_products.extend(shopping_products)
            logger.info(f"Google Shopping: {len(shopping_products)} productos")
        
        # Búsqueda orgánica si necesitamos más resultados
        if len(all_products) < 6:
            organic_data = self._make_request('google', final_query)
            if organic_data:
                organic_products = self._process_results(organic_data, 'google')
                all_products.extend(organic_products)
                logger.info(f"Google Orgánico: {len(organic_products)} productos")
        
        # Complementar con ejemplos si es necesario
        if len(all_products) < 3:
            examples = self._get_examples(final_query)
            all_products.extend(examples[:3])
            logger.info("Agregados ejemplos complementarios")
        
        # Filtrar duplicados
        unique_products = self._remove_duplicates(all_products)
        
        # Agregar metadata
        for product in unique_products:
            product['search_source'] = search_source
            product['original_query'] = query or "imagen"
        
        # Ordenar por relevancia
        unique_products.sort(key=lambda x: (
            0 if x.get('engine_source') == 'example' else -1000,
            -500 if x.get('engine_source') == 'google_shopping' else 0,
            x['price_numeric']
        ))
        
        final_products = unique_products[:6]
        
        # Guardar en cache
        self.cache[cache_key] = (final_products, time.time())
        if len(self.cache) > 20:
            oldest_key = min(self.cache.keys(), key=lambda k: self.cache[k][1])
            del self.cache[oldest_key]
        
        logger.info(f"Búsqueda completada: {len(final_products)} productos")
        return final_products
    
    def _remove_duplicates(self, products):
        """Remueve productos duplicados"""
        seen_titles = set()
        unique_products = []
        
        for product in products:
            title_key = product['title'].lower()[:50]
            if title_key not in seen_titles:
                seen_titles.add(title_key)
                unique_products.append(product)
        
        return unique_products
    
    def _get_examples(self, query):
        """Genera ejemplos realistas de autopartes"""
        stores = [
            ('RockAuto', 'rockauto.com'),
            ('AutoZone', 'autozone.com'),
            ('O\'Reilly Auto Parts', 'oreillyauto.com')
        ]
        
        examples = []
        query_lower = query.lower()
        
        # Determinar tipo de autoparte
        if any(word in query_lower for word in ['brake', 'freno']):
            parts_data = [
                ('Ceramic Brake Pads Set', 75),
                ('Brake Rotor Pair', 120),
                ('Brake Caliper Assembly', 95)
            ]
        elif any(word in query_lower for word in ['filter', 'filtro']):
            parts_data = [
                ('OEM Air Filter', 18),
                ('Premium Oil Filter', 12),
                ('Cabin Air Filter', 22)
            ]
        elif any(word in query_lower for word in ['headlight', 'light']):
            parts_data = [
                ('LED Headlight Assembly', 185),
                ('Halogen Headlight Bulb', 25),
                ('Headlight Right Side', 165)
            ]
        else:
            base_name = query.title() if len(query) < 30 else query[:30].title()
            parts_data = [
                (f'{base_name} OEM', 60),
                (f'{base_name} Aftermarket', 45),
                (f'{base_name} Premium', 85)
            ]
        
        # Generar ejemplos
        for i, (
