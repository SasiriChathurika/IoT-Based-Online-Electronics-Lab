from flask import Flask, render_template, request, jsonify, send_from_directory
import subprocess
import time  # Import the time module

app = Flask(__name__)

# --- Configuration ---
# Adjust these paths to match your actual script locations
ADS_SCRIPT = "only_ADS_kalman_wth_sliders.py"
SWITCHING_SCRIPT = "only_switching.py"
MCP_SCRIPT = "only_MCP.py"

# --- Helper Functions ---


def run_script(script_path, args=[]):
    """
    Runs a Python script in a separate process.
    """
    try:
        process = subprocess.Popen(
            ["python", script_path] + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return process
    except FileNotFoundError:
        print(f"Error: Script not found at {script_path}")
        return None
    except Exception as e:
        print(f"Error running script {script_path}: {e}")
        return None


def stop_script(process):
    """
    Stops a running script process.
    """
    if process:
        process.terminate()
        try:
            # Wait for the process to terminate (with a timeout)
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            print("Warning: Script did not terminate gracefully.")


# --- Global Variables ---
ads_process = None
switching_process = None
mcp_process = None

# --- Routes ---


@app.route("/")
def index():
    """
    Renders the main page with the input form.
    """
    return render_template("index.html")


@app.route("/run_experiment", methods=["POST"])
def run_experiment():
    """
    Handles the experiment execution request.
    """
    global ads_process, switching_process, mcp_process

    # Get form data
    l_value = request.form.get("l_value")
    c_value = request.form.get("c_value")
    r_value = request.form.get("r_value")
    frequency = request.form.get("frequency")

    # Validate form data
    if not all([l_value, c_value, r_value, frequency]):
        return jsonify({"error": "Missing input parameters."}), 400

    # Stop existing processes
    stop_script(ads_process)
    stop_script(switching_process)
    stop_script(mcp_process)

    # Construct switching configuration
    switch_config = (l_value, c_value, r_value)

    # Run scripts
    try:
        switching_process = run_script(SWITCHING_SCRIPT, list(switch_config))
        mcp_process = run_script(MCP_SCRIPT)
        ads_process = run_script(ADS_SCRIPT)

        # Allow processes to start
        time.sleep(2)

        return jsonify({"status": "Experiment started."})

    except Exception as e:
        print(f"Error starting experiment: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/get_plot", methods=["GET"])
def get_plot():
    """
    Serves the plot image.  Assumes the plotting script saves the image to 'static/plot.png'.
    """
    return send_from_directory("static", "plot.png")  # requires "import send_from_directory"


@app.route("/stop_experiment", methods=["POST"])
def stop_experiment():
    """
    Stops the running experiment.
    """
    global ads_process, switching_process, mcp_process

    stop_script(ads_process)
    stop_script(switching_process)
    stop_script(mcp_process)

    return jsonify({"status": "Experiment stopped."})


if __name__ == "__main__":
    app.run(debug=True)
