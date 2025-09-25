from flask import Flask, jsonify, request
import datetime
import os

app = Flask(__name__)

# Simple in-memory counter (resets on restart)
request_counter = 0

# Global CSS for consistent styling
GLOBAL_CSS = """
    body { 
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
        margin: 0; 
        padding: 20px; 
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
        min-height: 100vh; 
        color: #2c3e50;
    }
    .container { 
        max-width: 900px; 
        margin: 0 auto; 
        background: white; 
        border-radius: 15px; 
        padding: 40px; 
        box-shadow: 0 10px 30px rgba(0,0,0,0.2); 
        position: relative;
    }
    h1 { 
        color: #2c3e50; 
        text-align: center; 
        margin-bottom: 30px; 
        font-size: 2.5em;
    }
    .page-title {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 15px;
        margin-bottom: 40px;
    }
    .nav-bar {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 15px 30px;
        border-radius: 10px;
        margin-bottom: 30px;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    .nav-links {
        display: flex;
        justify-content: center;
        gap: 20px;
        flex-wrap: wrap;
    }
    .endpoint { 
        display: inline-block; 
        padding: 12px 24px; 
        background: #007bff; 
        color: white; 
        text-decoration: none; 
        border-radius: 25px; 
        margin: 5px; 
        transition: all 0.3s ease; 
        font-weight: 500;
        border: none;
        cursor: pointer;
    }
    .endpoint:hover { 
        background: #0056b3; 
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 123, 255, 0.3);
    }
    .endpoint.active {
        background: #28a745;
        box-shadow: 0 4px 12px rgba(40, 167, 69, 0.3);
    }
    .endpoint.active:hover {
        background: #218838;
    }
    .back-btn {
        position: absolute;
        top: 20px;
        left: 20px;
        background: #6c757d;
        color: white;
        padding: 10px 20px;
        border-radius: 20px;
        text-decoration: none;
        font-size: 0.9em;
        transition: all 0.3s ease;
    }
    .back-btn:hover {
        background: #5a6268;
        transform: translateY(-1px);
    }
    .status { 
        font-size: 1.3em; 
        padding: 15px; 
        border-radius: 10px; 
        margin: 20px 0; 
        text-align: center; 
        font-weight: 600;
    }
    .live { 
        background: #d4edda; 
        color: #155724; 
        border: 2px solid #c3e6cb; 
    }
    .healthy { 
        background: #d4edda; 
        color: #155724; 
        border: 2px solid #c3e6cb; 
        font-size: 1.4em;
    }
    .metric { 
        display: flex; 
        justify-content: space-between; 
        margin: 15px 0; 
        padding: 20px; 
        background: #f8f9fa; 
        border-radius: 10px; 
        border-left: 4px solid #007bff; 
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .metric-card {
        background: #f8f9fa; 
        padding: 25px; 
        border-radius: 10px; 
        margin: 20px 0; 
        border-left: 4px solid #17a2b8; 
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .metric-value { 
        font-size: 1.8em; 
        font-weight: bold; 
        color: #17a2b8; 
    }
    .env-badge { 
        display: inline-block; 
        padding: 10px 20px; 
        border-radius: 25px; 
        color: white; 
        font-weight: bold; 
        font-size: 0.9em;
    }
    .info-grid, .stats-grid { 
        display: grid; 
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); 
        gap: 20px; 
        margin: 30px 0; 
    }
    .info-card, .stat-card { 
        background: #f8f9fa; 
        padding: 25px; 
        border-radius: 10px; 
        text-align: center; 
        border: 1px solid #dee2e6; 
        transition: transform 0.2s ease;
    }
    .info-card:hover, .stat-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .info-card h3, .stat-card h3 { 
        margin-top: 0; 
        color: #007bff; 
        font-size: 1.1em;
    }
    .stat-value { 
        font-size: 2em; 
        font-weight: bold; 
        color: #495057; 
        margin: 10px 0; 
    }
    .json-link { 
        text-align: center; 
        margin: 40px 0; 
        padding: 20px;
        background: #f8f9fa;
        border-radius: 10px;
    }
    pre { 
        background: #f8f9fa; 
        padding: 20px; 
        border-radius: 8px; 
        overflow-x: auto; 
        font-size: 0.9em; 
        border-left: 4px solid #007bff; 
        white-space: pre-wrap;
        line-height: 1.5;
    }
    .json-highlight {
        color: #d63384;
        font-weight: bold;
    }
    hr { 
        border: none; 
        height: 2px; 
        background: linear-gradient(to right, transparent, #007bff, transparent); 
        margin: 40px 0; 
    }
    .footer {
        text-align: center;
        margin-top: 40px;
        padding-top: 20px;
        border-top: 1px solid #eee;
        color: #6c757d;
        font-size: 0.9em;
    }
    @media (max-width: 768px) {
        .container { padding: 20px; }
        .nav-links { flex-direction: column; align-items: center; }
        .info-grid, .stats-grid { grid-template-columns: 1fr; }
        h1 { font-size: 2em; }
    }
"""

@app.route("/")
def hello():
    global request_counter
    request_counter += 1
    
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return f"""
    <html>
        <head>
            <title>STAGING infra</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>{GLOBAL_CSS}</style>
        </head>
        <body>
            <div class="container">
                <div class="nav-bar">
                    <div class="nav-links">
                        <a href="/" class="endpoint active">🏠 Dashboard</a>
                        <a href="/health" class="endpoint">❤️ Health Check</a>
                        <a href="/stats" class="endpoint">📊 Statistics</a>
                    </div>
                </div>
                
                <div class="page-title">
                    <h1>🚀 STAGING DevOps Dashboard</h1>
                </div>
                
                <div class="status live">
                    <strong>Service Status:</strong> <span>🟢 LIVE</span>
                </div>
                
                <div class="metric">
                    <span><strong>Server Time:</strong></span>
                    <span>{current_time}</span>
                </div>
                
                <div class="metric">
                    <span><strong>Requests Served:</strong></span>
                    <span>{request_counter} 🚀</span>
                </div>
                
                <hr>
                
                <div style="text-align: center;">
                    <h3 style="color: #007bff; margin-bottom: 20px;">🌐 Quick Navigation</h3>
                    <div class="nav-links">
                        <a href="/health" class="endpoint">❤️ Health Check</a>
                        <a href="/stats" class="endpoint">📊 Statistics</a>
                    </div>
                </div>
                
                <div class="footer">
                    <p>🌟 Built for DevOps Engineers | Requests: {request_counter} | Server Time: {current_time}</p>
                </div>
            </div>
        </body>
    </html>
    """

@app.route("/health")
def health_check():
    """Health check endpoint with frontend and JSON support"""
    global request_counter
    request_counter += 1
    
    accept_header = request.headers.get('Accept', '')
    wants_json = 'application/json' in accept_header or request.path.endswith('.json')
    
    if wants_json:
        return jsonify({
            "status": "healthy",
            "timestamp": datetime.datetime.now().isoformat(),
            "uptime": "running",
            "requests_served": request_counter
        })
    
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    timestamp = datetime.datetime.now().isoformat()
    
    return f"""
    <html>
        <head>
            <title>Health Check - DevOps Dashboard</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>{GLOBAL_CSS}</style>
        </head>
        <body>
            <div class="container">
                <a href="/" class="back-btn">🏠 Back to Dashboard</a>
                
                <div class="nav-bar">
                    <div class="nav-links">
                        <a href="/" class="endpoint">🏠 Dashboard</a>
                        <a href="/health" class="endpoint active">❤️ Health Check</a>
                        <a href="/stats" class="endpoint">📊 Statistics</a>
                    </div>
                </div>
                
                <div class="page-title">
                    <h1>❤️ Health Check</h1>
                </div>
                
                <div class="status healthy">
                    <strong>Service is: 🟢 HEALTHY</strong>
                </div>
                
                <div class="info-grid">
                    <div class="info-card">
                        <h3>📅 Last Checked</h3>
                        <p><strong>{current_time}</strong></p>
                    </div>
                    <div class="info-card">
                        <h3>📊 Total Requests</h3>
                        <p><strong>{request_counter}</strong></p>
                    </div>
                    <div class="info-card">
                        <h3>⏱️ Uptime</h3>
                        <p><strong>Running</strong></p>
                    </div>
                    <div class="info-card">
                        <h3>🔄 Status</h3>
                        <p><strong>100% Available</strong></p>
                    </div>
                </div>
                
                <div class="json-link">
                    <h3 style="color: #007bff; margin-bottom: 20px;">📋 API Response</h3>
                    <a href="/health.json" class="endpoint">📄 Get JSON Response</a>
                    <pre>{{"status": "healthy",<br>&nbsp;&nbsp;"timestamp": "{timestamp}",<br>&nbsp;&nbsp;"uptime": "running",<br>&nbsp;&nbsp;"requests_served": {request_counter}}}</pre>
                </div>
                
                <div class="footer">
                    <p>❤️ Health Check | Last Updated: {current_time} | Total Requests: {request_counter}</p>
                </div>
            </div>
        </body>
    </html>
    """

@app.route("/stats")
def get_stats():
    """Statistics endpoint with frontend and JSON support"""
    global request_counter
    request_counter += 1
    
    accept_header = request.headers.get('Accept', '')
    wants_json = 'application/json' in accept_header or request.path.endswith('.json')
    
    if wants_json:
        stats = {
            "total_requests": request_counter,
            "current_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "hostname": os.getenv("HOSTNAME", "unknown"),
            "environment": os.getenv("FLASK_ENV", "development"),
            "message": "DevOps monitoring ready! 📊"
        }
        return jsonify(stats)
    
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    hostname = os.getenv("HOSTNAME", "unknown")
    environment = os.getenv("FLASK_ENV", "development")
    
    env_color = "#28a745" if environment == "production" else "#ffc107"
    
    return f"""
    <html>
        <head>
            <title>Statistics - DevOps Dashboard</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>{GLOBAL_CSS}</style>
        </head>
        <body>
            <div class="container">
                <a href="/" class="back-btn">🏠 Back to Dashboard</a>
                
                <div class="nav-bar">
                    <div class="nav-links">
                        <a href="/" class="endpoint">🏠 Dashboard</a>
                        <a href="/health" class="endpoint">❤️ Health Check</a>
                        <a href="/stats" class="endpoint active">📊 Statistics</a>
                    </div>
                </div>
                
                <div class="page-title">
                    <h1>📊 Statistics</h1>
                </div>
                
                <div class="metric-card">
                    <div>
                        <h3>Total Requests Served</h3>
                        <div class="metric-value">{request_counter} 🚀</div>
                    </div>
                    <div class="env-badge" style="background: {env_color}">{environment.upper()}</div>
                </div>
                
                <div class="stats-grid">
                    <div class="stat-card">
                        <h3>⏰ Current Time</h3>
                        <div class="stat-value">{current_time}</div>
                    </div>
                    <div class="stat-card">
                        <h3>🖥️ Hostname</h3>
                        <div class="stat-value">{hostname}</div>
                    </div>
                    <div class="stat-card">
                        <h3>🌍 Environment</h3>
                        <div class="stat-value" style="color: {env_color}">{environment}</div>
                    </div>
                    <div class="stat-card">
                        <h3>📈 Request Rate</h3>
                        <div class="stat-value">{request_counter} req</div>
                    </div>
                </div>
                
                <div class="json-link">
                    <h3 style="color: #007bff; margin-bottom: 20px;">📋 API Response</h3>
                    <a href="/stats.json" class="endpoint">📄 Get JSON Response</a>
                    <pre>{{"total_requests": {request_counter},<br>&nbsp;&nbsp;"current_time": "{current_time}",<br>&nbsp;&nbsp;"hostname": "{hostname}",<br>&nbsp;&nbsp;"environment": "{environment}",<br>&nbsp;&nbsp;"message": "DevOps monitoring ready! 📊"<br>}}</pre>
                </div>
                
                <div class="footer">
                    <p>📊 Statistics | Updated: {current_time} | Environment: {environment}</p>
                </div>
            </div>
        </body>
    </html>
    """

@app.route("/health.json")
@app.route("/stats.json")
def json_endpoints():
    """Redirect JSON requests to appropriate handlers"""
    if request.path == "/health.json":
        return health_check()
    elif request.path == "/stats.json":
        return get_stats()
    return jsonify({"error": "Not Found"}), 404

@app.errorhandler(404)
def not_found(error):
    """Custom 404 handler"""
    return f"""
    <html>
        <head>
            <title>404 - Page Not Found</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>{GLOBAL_CSS}</style>
            <style>
                body {{ background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%); }}
                .container {{ text-align: center; max-width: 600px; }}
                h1 {{ color: #e74c3c; margin-bottom: 20px; font-size: 3em; }}
                .error-status {{ font-size: 1.5em; color: #e74c3c; margin: 20px 0; }}
                .nav-bar {{ background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%); }}
                .endpoint {{ background: #e74c3c; }}
                .endpoint:hover {{ background: #c0392b; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="nav-bar">
                    <div class="nav-links">
                        <a href="/" class="endpoint">🏠 Dashboard</a>
                        <a href="/health" class="endpoint">❤️ Health Check</a>
                        <a href="/stats" class="endpoint">📊 Statistics</a>
                    </div>
                </div>
                
                <div class="page-title">
                    <h1>❌ 404</h1>
                </div>
                
                <div class="error-status">
                    <strong>Page Not Found</strong>
                </div>
                
                <p style="font-size: 1.2em; margin: 30px 0;">This endpoint doesn't exist. Try one of these:</p>
                
                <div style="margin: 40px 0;">
                    <a href="/" class="endpoint" style="font-size: 1.1em; padding: 15px 30px;">🏠 Go to Dashboard</a>
                </div>
                
                <div class="footer">
                    <p>❌ Error 404 | Let's get you back on track!</p>
                </div>
            </div>
        </body>
    </html>
    """, 404

if __name__ == "__main__":
    debug = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    print(f"🚀 Starting DevOps Dashboard...")
    print(f"🌐 Available at: http://0.0.0.0:5000")
    print(f"🔧 Debug mode: {debug}")
    app.run(host="0.0.0.0", port=5000, debug=debug)
