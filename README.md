# Captcha-Implementation

A very simple CAPTCHA system built with **Flask (Python 3)** that combines:

- Traditional CAPTCHA challenges  
- Logic-based reasoning questions  
- Behavioral biometric analysis  
- Confidence scoring(basic reflex type)  

This project explores how multiple human-detection signals can be combined to build a smarter anti-bot verification system.

**Test Parameters**

- **Normal CAPTCHA** – Enter text as shown  
- **Reverse CAPTCHA** – Enter the code backwards  
- **Odd Character CAPTCHA** – Enter characters at odd indices  
- **Math Challenge** – Solve arithmetic problems  
- **Logic Challenge** – Context-based reasoning question  

Example logic trap:

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


