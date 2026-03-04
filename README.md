# Captcha-Implementation

**Website Link - https://captcha-implementations.onrender.com/**
**I have Shifted the backend to a website to improve intuitivity and also make it simpler to execute; The latter would require a Python3 Virtual Environment with complex installations.**

**Disclaimer - Due to Free Services on Render, the Backend may sleep. Due to this it may take upto 1 minute to boot it back.**


A very simple CAPTCHA system built with **Flask (Python 3)** that combines:

- Traditional CAPTCHA challenges  
- Logic-based reasoning questions  
- Behavioral biometric analysis  
- Confidence scoring(basic reflex type)  

This project explores how multiple human-detection signals can be combined to build a smarter anti-bot verification system.

--------------------------------------------------------------------------------------------------------------------------------------------

# Test Parameters

- **Normal CAPTCHA** – Enter text as shown  
- **Reverse CAPTCHA** – Enter the code backwards  
- **Odd Character CAPTCHA** – Enter characters at odd indices  
- **Math Challenge** – Solve arithmetic problems  
- **Logic Challenge** – Context-based reasoning question  

## Example logic trap:

  > “You want to wash your car and the car wash is 50 meters away.  
  > Should you walk or drive the car there?”

Correct answer: **DRIVE**

---

The CAPTCHA does not rely only on correct answers.

It also analyzes human interaction patterns:

- Checkbox reaction timing
- Mouse movement distance & trajectory
- Keystroke variance
- Typing delay before first key press

--------------------------------------------------------------------------------------------------------------------------------------------

# Tech Stack

1. Python3
2. Gunicorn (For Render Backend)
3. Flask - Python Library (For Web Applications)
4. captcha - Python Library (To generate Captchas)
5. Python3 Virtual Environment (To run Flask and captcha)

--------------------------------------------------------------------------------------------------------------------------------------------

# Why Captcha over Turing Test?

Turing Test requires a Large Language Model to effectively test if a Judge is able to tell the difference if or not it is an AI.
>LLM libraries can be imported into Python (They require you to have a paid account)
>Machines can be used to locally run some LLMS like Ollama and Quen and also Deepseek's R1 but they require heafty Hardware with 32+ GB of Ram.

