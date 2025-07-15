from app import create_app

app = create_app()

# ✅ This part must be outside if __name__ == '__main__' so Vercel sees `app`
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050)
