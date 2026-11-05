from flask import Flask, render_template_string
import os

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ur" dir="rtl">
<head><title>Test Mode</title></head>
<body style="background:#121212; color:white; text-align:center; padding-top:50px;">
    <h1>✅ سسٹم زندہ ہے! (Test Mode)</h1>
    <p>اگر یہ پیج نظر آ رہا ہے، تو اس کا مطلب ہے کہ سرور ٹھیک ہے اور مسئلہ کسی اور فائل میں ہے۔</p>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
