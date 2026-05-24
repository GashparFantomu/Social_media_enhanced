import google.generativeai as genai

# Pune cheia ta reala intre ghilimele:
genai.configure(api_key="API KEY") #ma bat ăștia la cap cu emailuri că cică e descoperit an plm.

print("Se interogheaza Google pentru modelele disponibile...\n")

try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"Model suportat: {m.name}")
    print("\n✅ Test complet.")
except Exception as e:
    print(f"❌ Eroare la interogare: {e}")