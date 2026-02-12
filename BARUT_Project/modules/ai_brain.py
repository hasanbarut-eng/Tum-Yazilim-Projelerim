# -*- coding: utf-8 -*-
# modules/ai_brain.py
import google.generativeai as genai
import os

class AIBrain:
    def __init__(self):
        # .env dosyasındaki anahtarı çekiyoruz
        api_key = os.getenv("VISION_API_KEY")
        genai.configure(api_key=api_key)
        
        # Kararlı ve hızlı model isimlendirmesi
        self.model = genai.GenerativeModel('gemini-1.5-flash') 
        
        self.system_instruction = (
            "Sen BARUT'sun. 56 yaşında tecrübeli bir matematik öğretmeni ve "
            "Kıdemli Yazılım Geliştirici (Senior Developer) asistanısın. "
            "Cevapların kısa, öz ve kesin çözüm odaklı olmalı. Excel, VBA, "
            "Python ve Borsa (ESEN) senin ana uzmanlık alanındır."
        )

    def ask(self, user_input, context=""):
        try:
            # Model çağırma protokolünü en kararlı yapıya çektik
            response = self.model.generate_content(
                f"{self.system_instruction}\n\nBağlam: {context}\nKullanıcı: {user_input}"
            )
            return response.text
        except Exception as e:
            # Hataları gizlemek yerine çözüm sunan mesaj
            return f"BARUT şu an yanıt veremiyor (Teknik Hata): {str(e)}"