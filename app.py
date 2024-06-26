from blog import create_app

app = create_app()
print("Static folder path:", app.static_folder)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001,debug=True)
