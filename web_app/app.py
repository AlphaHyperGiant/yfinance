from flask import Flask, render_template, request, jsonify
import sys
import io
import contextlib
import random

app = Flask(__name__)

# State
instances = {
    "v1": "print('Hello World from v1')",
}
current_version = "v1"
next_version = None
phase_shift = 0.0 # 0.0 to 1.0 (0% to 100% traffic to next_version)

@app.route('/')
def index():
    return render_template('index.html', 
                           instances=instances, 
                           current_version=current_version, 
                           next_version=next_version,
                           phase_shift=phase_shift)

@app.route('/deploy', methods=['POST'])
def deploy():
    global next_version, instances
    code = request.json.get('code')
    version_name = f"v{len(instances) + 1}"
    instances[version_name] = code
    next_version = version_name
    return jsonify({"status": "success", "version": version_name})

@app.route('/rollback', methods=['POST'])
def rollback():
    global current_version, next_version, phase_shift
    target_version = request.json.get('version')
    if target_version in instances:
        current_version = target_version
        next_version = None
        phase_shift = 0.0
        return jsonify({"status": "success"})
    return jsonify({"status": "error", "message": "Version not found"}), 404

@app.route('/phase', methods=['POST'])
def set_phase():
    global phase_shift
    shift = float(request.json.get('shift', 0))
    if 0 <= shift <= 100:
        phase_shift = shift / 100.0
        return jsonify({"status": "success", "phase": phase_shift})
    return jsonify({"status": "error"}), 400

@app.route('/execute', methods=['POST'])
def execute():
    # Simulate traffic shifting
    version_to_run = current_version
    if next_version and random.random() < phase_shift:
        version_to_run = next_version
    
    code = instances.get(version_to_run, "")
    
    # Capture stdout
    f = io.StringIO()
    try:
        with contextlib.redirect_stdout(f):
            exec(code)
        result = f.getvalue()
    except Exception as e:
        result = str(e)
        
    return jsonify({
        "result": result, 
        "version_executed": version_to_run
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
