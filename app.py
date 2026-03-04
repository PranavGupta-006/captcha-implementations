import random
import string
import time
import base64
import json
import math
import statistics
import os

from flask import Flask, request, render_template_string, session, redirect
from captcha.image import ImageCaptcha


app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "super_secret_secure_key")


def generate_captcha_text(length=6):
    chars = string.ascii_uppercase + string.digits
    for ch in "0O1IL":
        chars = chars.replace(ch, "")
    return "".join(random.choices(chars, k=length))


def generate_math():
    a, b = random.randint(4, 15), random.randint(4, 15)
    return f"What is {a} + {b}?", str(a + b)


CHALLENGES = ["normal", "reverse", "odd", "math", "logic"]


HTML = """<!DOCTYPE html>
<html>
<head>
<title>CAPTCHA Implementation</title>
<script src="https://cdn.tailwindcss.com"></script>
<script>
let pageLoad=Date.now(),mouse=[],keys=[],first=null;

document.addEventListener("mousemove",e=>{
mouse.push([e.clientX,e.clientY,Date.now()]);
if(mouse.length>60)mouse.shift();
});

function markCheckbox(){
document.getElementById("checkbox_time").value=Date.now()-pageLoad;
}

function keyPressed(){
let t=Date.now();
keys.push(t);
if(!first){
first=t;
document.getElementById("key_delay").value=t-pageLoad;
}
document.getElementById("keystrokes").value=JSON.stringify(keys);
}

function beforeSubmit(){
document.getElementById("mouse_data").value=JSON.stringify(mouse);
}
</script>
</head>

<body class="min-h-screen flex items-center justify-center bg-slate-900 text-white px-4">

<div class="w-full max-w-md bg-slate-800/80 backdrop-blur border border-slate-700 rounded-3xl shadow-2xl overflow-hidden">

<div class="bg-gradient-to-r from-blue-600 to-indigo-600 px-6 py-5 text-center">
<h2 class="text-2xl font-bold">🤖 Human Verification</h2>
<p class="text-xs text-blue-100 mt-1 tracking-widest">Security Checkpoint</p>
</div>

<div class="p-8 text-center">

{% if phase == "checkbox" %}

<form method="POST">
<input type="hidden" name="checkbox_time" id="checkbox_time">

<div class="flex items-center justify-center gap-2">
<input type="checkbox" name="robot_check" onclick="markCheckbox()" class="h-4 w-4">
<label class="text-sm">I am not a robot</label>
</div>

<button class="w-full py-3 mt-4 bg-blue-600 rounded-xl font-bold">
Continue
</button>

</form>

{% endif %}



{% if phase == "challenge" %}

{% if image %}
<div class="flex justify-center mb-4">
<img src="data:image/png;base64,{{ image }}" class="bg-white px-3 py-2 rounded-xl border shadow">
</div>
{% endif %}

<form method="POST" onsubmit="beforeSubmit()">

<input type="hidden" name="mouse_data" id="mouse_data">
<input type="hidden" name="key_delay" id="key_delay">
<input type="hidden" name="keystrokes" id="keystrokes">

<label class="text-xs uppercase tracking-widest text-slate-400">
{{ instruction }}
</label>

<input
type="text"
name="user_input"
onkeydown="keyPressed()"
class="w-full mt-3 px-4 py-3 rounded-xl bg-slate-700 border uppercase text-center"
>

<button class="w-full py-3 mt-4 bg-blue-600 rounded-xl font-bold">
Verify
</button>

</form>

{% endif %}



{% if phase == "result" %}

<div class="mt-5 font-semibold {% if status=='success' %}text-green-400{% else %}text-red-400{% endif %}">
{{ message }}
</div>

<a href="/" class="inline-block mt-6 text-xs text-blue-400 hover:text-blue-300">
↻ Restart
</a>

{% endif %}

</div>
</div>
</body>
</html>
"""


def safe_int(value, default=0):
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


@app.route("/", methods=["GET", "POST"])
def verify():

    session.setdefault("phase", "checkbox")

    if request.method == "POST":

        if session["phase"] == "checkbox":

            if request.form.get("robot_check"):
                session["checkbox_delay"] = safe_int(request.form.get("checkbox_time"), 0)
                session["phase"] = "challenge"

            return redirect("/")


        if session["phase"] == "challenge":

            if not request.form.get("user_input"):

                session["result"] = (
                    "Test not completed. Please try again.",
                    "error"
                )

                session["phase"] = "result"
                return redirect("/")

            confidence = 0


            t = session.get("checkbox_delay", 0)

            if 800 <= t <= 5000:
                confidence += 10
            elif 0 < t < 300:
                confidence -= 10


            try:
                mouse = json.loads(request.form.get("mouse_data", "[]"))
            except:
                mouse = []

            dist = sum(
                math.hypot(
                    mouse[i][0]-mouse[i-1][0],
                    mouse[i][1]-mouse[i-1][1]
                )
                for i in range(1, len(mouse))
            )

            if dist > 200:
                confidence += 15


            try:
                keys = json.loads(request.form.get("keystrokes", "[]"))
            except:
                keys = []

            if len(keys) >= 4:

                v = statistics.variance(
                    [keys[i+1]-keys[i] for i in range(len(keys)-1)]
                )

                if v > 200:
                    confidence += 10


            d = safe_int(request.form.get("key_delay"), 0)

            if d > 600:
                confidence += 10


            user = request.form.get("user_input", "").strip().upper()

            c = session.get("challenge")


            if c == "math":

                if user == session.get("answer"):
                    confidence += 40


            elif c == "logic":

                if user in ["DRIVE", "DRIVING"]:
                    confidence += 40


            else:

                expected = session.get("code", "")

                if c == "reverse":
                    expected = expected[::-1]

                if c == "odd":
                    expected = expected[1::2]

                if user == expected:
                    confidence += 40


            session["result"] = (

                f"Verified as Human (Confidence: {confidence}%)"
                if confidence >= 70
                else f"Verification Failed (Confidence: {confidence}%)",

                "success" if confidence >= 70 else "error"

            )

            session["phase"] = "result"

            return redirect("/")



    if session["phase"] == "checkbox":
        return render_template_string(HTML, phase="checkbox")



    if session["phase"] == "challenge":

        if "challenge" not in session:
            c = random.choice(CHALLENGES)
            session["challenge"] = c
        else:
            c = session["challenge"]


        if c == "logic":

            question = (
                "You want to wash your car and the car wash is 50 meters away. "
                "Should you walk or drive the car there?"
            )

            return render_template_string(
                HTML,
                phase="challenge",
                image=None,
                instruction=question
            )


        if c == "math":

            if "answer" not in session:

                q, a = generate_math()

                session["answer"] = a
                session["instruction"] = q

            return render_template_string(
                HTML,
                phase="challenge",
                image=None,
                instruction=session["instruction"]
            )


        if "code" not in session:
            session["code"] = generate_captcha_text()

        code = session["code"]

        img = ImageCaptcha(width=280, height=90).generate(code)


        instruction = {
            "normal": "Enter the code exactly as shown",
            "reverse": "Enter the code in reverse order",
            "odd": "Enter characters at odd positions only (0-indexed)"
        }[c]


        return render_template_string(

            HTML,

            phase="challenge",

            image=base64.b64encode(img.getvalue()).decode(),

            instruction=instruction

        )


    result_data = session.get(
        "result",
        ("An unexpected error occurred.", "error")
    )

    msg, st = result_data

    session.clear()

    return render_template_string(
        HTML,
        phase="result",
        message=msg,
        status=st
    )


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )
