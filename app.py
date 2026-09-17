from flask import Flask, request, render_template_string, redirect, url_for

app = Flask(__name__)

# Base de datos temporal en memoria
usuarios_db = {}
publicaciones = [] # Posts del muro estilo Instagram
mensajes_grupo = [] # Mensajes del chat estilo WhatsApp

HTML_APP = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BroNet - Bro Developer Zone</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        body { background-color: #0f1419; color: #e7e9ea; display: flex; justify-content: center; }
        .app-container { width: 100%; max-width: 480px; background: #161e27; min-height: 100vh; border-left: 1px solid #2f3336; border-right: 1px solid #2f3336; display: flex; flex-direction: column; }
        header { background: #1d2733; padding: 15px; text-align: center; font-size: 22px; font-weight: bold; color: #0088cc; border-bottom: 1px solid #2f3336; }
        .brand-sub { font-size: 11px; font-weight: normal; color: #8899a6; margin-top: 3px; letter-spacing: 0.5px; }
        .content { padding: 15px; flex: 1; overflow-y: auto; }
        .card { background: #222e3a; padding: 20px; border-radius: 12px; margin-bottom: 15px; border: 1px solid #2f3336; text-align: center; }
        input, textarea, button { width: 100%; padding: 12px; margin-top: 10px; border-radius: 8px; border: none; font-size: 14px; }
        input, textarea { background: #161e27; color: #fff; border: 1px solid #3d4a58; }
        button { background: #0088cc; color: white; font-weight: bold; cursor: pointer; transition: 0.2s; }
        button:hover { background: #0077b5; }
        .post { background: #1d2733; padding: 12px; border-radius: 10px; margin-bottom: 10px; border-left: 4px solid #0088cc; }
        .post-author { font-weight: bold; color: #58b9ff; font-size: 13px; }
        .post-text { margin-top: 5px; font-size: 15px; }
        .chat-box { background: #111721; height: 260px; overflow-y: auto; padding: 10px; border-radius: 8px; margin-bottom: 10px; display: flex; flex-direction: column; gap: 8px; text-align: left; }
        .msg { background: #2b394a; padding: 8px 12px; border-radius: 8px; max-width: 85%; width: fit-content; }
        .msg-author { font-size: 11px; color: #0088cc; font-weight: bold; }
        .nav-tabs { display: flex; background: #1d2733; border-top: 1px solid #2f3336; }
        .tab { flex: 1; text-align: center; padding: 12px; color: #8899a6; text-decoration: none; font-weight: bold; }
        .tab.active { color: #0088cc; border-bottom: 2px solid #0088cc; }
    </style>
</head>
<body>
    <div class="app-container">
        <header>
            BroNet 🚀
            <div class="brand-sub">Created by Bdz | Bro Developer Zone</div>
        </header>
        
        <div class="content">
            {% if not usuario_actual %}
            <!-- ACCESO Y FIRMA BDZ -->
            <div class="card">
                <h2>Bienvenido a BroNet</h2>
                <p style="font-size: 13px; color: #0088cc; font-weight: bold; margin-top: 5px;">Created by Bdz</p>
                <p style="font-size: 11px; color: #8899a6; margin-top: 4px;">Coding the future, building the brotherhood.</p>
                <p style="font-size: 12px; color: #e7e9ea; margin-top: 12px;">Acceso con Alias o Gmail (Sin verificación telefónica)</p>
                
                <form action="/login" method="POST">
                    <input type="text" name="username" placeholder="Usuario, Alias o Gmail" required>
                    <input type="password" name="password" placeholder="Contraseña" required>
                    <button type="submit">Iniciar Sesión / Registrarse</button>
                </form>
            </div>
            {% else %}
            
            <p style="margin-bottom: 12px; font-size: 14px;">Conectado como: <strong style="color:#0088cc;">@{{ usuario_actual }}</strong> | <a href="/logout" style="color: #e0245e; font-size: 12px;">Cerrar sesión</a></p>

            <!-- SECCIÓN 1: MURO (ESTILO INSTAGRAM) -->
            {% if seccion == 'muro' %}
            <div class="card" style="text-align: left;">
                <h3 style="text-align: center;">Crear Publicación</h3>
                <form action="/publicar" method="POST">
                    <textarea name="texto" rows="3" placeholder="¿Qué está pasando, bro?" required></textarea>
                    <button type="submit">Publicar en el Muro</button>
                </form>
            </div>
            
            <h3 style="margin-bottom: 10px;">Muro de la Comunidad</h3>
            {% for post in publicaciones %}
            <div class="post">
                <div class="post-author">@{{ post.autor }}</div>
                <div class="post-text">{{ post.texto }}</div>
            </div>
            {% else %}
            <p style="color: #8899a6; font-size: 13px;">No hay publicaciones aún. ¡Sé el primero en escribir algo!</p>
            {% endfor %}

            <!-- SECCIÓN 2: CHAT GRUPAL (ESTILO WHATSAPP) -->
            {% elif seccion == 'chat' %}
            <div class="card" style="text-align: left;">
                <h3 style="text-align: center; margin-bottom: 10px;">Grupo General (Wi-Fi Chat)</h3>
                <div class="chat-box">
                    {% for msg in mensajes %}
                    <div class="msg">
                        <div class="msg-author">@{{ msg.autor }}</div>
                        <div>{{ msg.texto }}</div>
                    </div>
                    {% else %}
                    <p style="color: #8899a6; font-size: 12px;">Chat vacío. Escribe un mensaje para empezar...</p>
                    {% endfor %}
                </div>
                <form action="/enviar_chat" method="POST">
                    <input type="text" name="mensaje" placeholder="Escribe un mensaje al grupo..." required>
                    <button type="submit">Enviar Mensaje</button>
                </form>
            </div>
            {% endif %}

            {% endif %}
        </div>

        {% if usuario_actual %}
        <!-- NAVEGACIÓN INFERIOR -->
        <div class="nav-tabs">
            <a href="/?sec=muro" class="tab {% if seccion == 'muro' %}active{% endif %}">📷 Muro</a>
            <a href="/?sec=chat" class="tab {% if seccion == 'chat' %}active{% endif %}">💬 Grupos</a>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

# Rutas del Servidor
usuario_sesion = None

@app.route('/')
def home():
    sec = request.args.get('sec', 'muro')
    return render_template_string(HTML_APP, usuario_actual=usuario_sesion, publicaciones=publicaciones, mensajes=mensajes_grupo, seccion=sec)

@app.route('/login', methods=['POST'])
def login():
    global usuario_sesion
    user = request.form.get('username')
    pwd = request.form.get('password')
    
    if user not in usuarios_db:
        usuarios_db[user] = pwd
    elif usuarios_db[user] != pwd:
        return "<h3>Contraseña incorrecta. <a href='/'>Volver</a></h3>", 401
    
    usuario_sesion = user
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    global usuario_sesion
    usuario_sesion = None
    return redirect(url_for('home'))

@app.route('/publicar', methods=['POST'])
def publicar():
    if usuario_sesion:
        texto = request.form.get('texto')
        publicaciones.insert(0, {'autor': usuario_sesion, 'texto': texto})
    return redirect(url_for('home', sec='muro'))

@app.route('/enviar_chat', methods=['POST'])
def enviar_chat():
    if usuario_sesion:
        msg = request.form.get('mensaje')
        mensajes_grupo.append({'autor': usuario_sesion, 'texto': msg})
    return redirect(url_for('home', sec='chat'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
