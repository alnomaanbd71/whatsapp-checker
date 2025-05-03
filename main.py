# main.py

import os
from flask import Flask, request, render_template_string, jsonify, current_app
from whatsapp_checker import check_numbers

app = Flask(__name__)

# Simple HTML template with purple gradient & animated button
INDEX_HTML = 
!doctype html
html
head
  titleWhatsApp Checkertitle
  style
    body { margin0; font-familysans-serif;
      background linear-gradient(135deg, #7f00ff, #e100ff);
      height100vh; displayflex; align-itemscenter; justify-contentcenter;
    }
    .card {
      backgroundwhite; padding2rem; border-radius1rem;
      box-shadow0 10px 30px rgba(0,0,0,0.1); width90%; max-width400px;
    }
    textarea { width100%; height100px; margin-bottom1rem; padding0.5rem; }
    button {
      width100%; padding0.75rem; font-size1rem; bordernone; colorwhite;
      background linear-gradient(90deg, #9c27b0, #e040fb);
      border-radius0.5rem; cursorpointer; transitiontransform .2s;
    }
    buttonhover { transformscale(1.03); }
    pre { background#f4f4f4; padding1rem; border-radius0.5rem; overflowauto; }
  style
head
body
  div class=card
    h2WhatsApp Number Checkerh2
    form method=post action=check
      textarea name=numbers placeholder=e.g. 93777670441,93771228985,…textarea
      button type=submitCheck Numbersbutton
    form
    {% if result %}
      h3Resulth3
      preRegisteredn{{ result.registeredjoin('n') }}
Not Registeredn{{ result.not_registeredjoin('n') }}pre
    {% endif %}
  div
body
html


@app.route(, methods=[GET])
def home()
    return render_template_string(INDEX_HTML)

@app.route(check, methods=[POST])
def check()
    data = request.form.get(numbers, )
    nums = [n.strip() for n in data.split(,) if n.strip()]
    chrome_bin = os.getenv(CHROME_BIN)  # from Dockerfile env
    registered, not_registered = check_numbers(nums, chrome_bin=chrome_bin)
    # If AJAXJSON desired
    if request.headers.get(Accept,).startswith(applicationjson)
        return jsonify({
            registered registered,
            not_registered not_registered
        })
    # else re-render UI with result
    return render_template_string(
        INDEX_HTML,
        result={registered registered, not_registered not_registered}
    )

if __name__ == __main__
    port = int(os.environ.get(PORT, 5000))
    # listen on all interfaces
    app.run(host=0.0.0.0, port=port)
