from app import app

if __name__ == "__main__":
    # Bind to 0.0.0.0 for container use; port can be controlled externally
    app.run(host="0.0.0.0", port=5000)
