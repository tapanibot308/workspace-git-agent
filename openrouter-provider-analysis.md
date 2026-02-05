# OpenRouter Provider-analyysi
**Päivämäärä:** 2026-02-05

## Käytössä olevat mallit - Provider-tiedot

### google/gemini-2.5-flash
- **Nimi:** Google: Gemini 2.5 Flash
- **Alkuperä:** USA (Google)
- **Provider:** Native Google AI API ✅
- **Context:** 1,048,576 tokensia
- **Hinta:** $0.0000003 / $0.0000025 (prompt/completion)
- **Luotettavuus:** ⭐⭐⭐⭐⭐ Länsimainen, suora Google API

### deepseek/deepseek-chat (DeepSeek V3)
- **Nimi:** DeepSeek: DeepSeek V3
- **Alkuperä:** Kiina (DeepSeek AI)
- **Provider:** Native DeepSeek API ⚠️
- **Context:** 163,840 tokensia
- **Hinta:** $0.0000003 / $0.0000012
- **Luotettavuus:** ⭐⭐⭐ Suora API Kiinaan, ei länsimaisia väliprovidereita

### deepseek/deepseek-r1
- **Nimi:** DeepSeek: R1 (Reasoning)
- **Alkuperä:** Kiina (DeepSeek AI)
- **Provider:** Native DeepSeek API ⚠️
- **Context:** 64,000 tokensia
- **Hinta:** $0.0000007 / $0.0000025
- **Luotettavuus:** ⭐⭐⭐ Suora API Kiinaan, ei länsimaisia väliprovidereita

### x-ai/grok-4.1-fast
- **Nimi:** xAI: Grok 4.1 Fast
- **Alkuperä:** USA (xAI / Elon Musk)
- **Provider:** Native xAI API ✅
- **Context:** 2,000,000 tokensia
- **Hinta:** $0.0000002 / $0.0000005
- **Luotettavuus:** ⭐⭐⭐⭐⭐ Länsimainen, suora xAI API

### moonshotai/kimi-k2.5
- **Nimi:** MoonshotAI: Kimi K2.5
- **Alkuperä:** Kiina (MoonshotAI)
- **Provider:** Native MoonshotAI API ⚠️
- **Context:** 262,144 tokensia
- **Hinta:** $0.00000045 / $0.0000025
- **Luotettavuus:** ⭐⭐⭐ Suora API Kiinaan, ei länsimaisia väliprovidereita

---

## KRIITTISET HAVAINNOT

### 1. Ei väliprovidereita
OpenRouter käyttää **natiiveja API-yhteyksiä** kaikille näille malleille:
- Ei `providers`-kenttää JSON-vastauksessa
- Jokainen malli yhdistyy suoraan omaan API-endpointiinsa
- **Ei löytynyt yhtään kiinalaista mallia länsimaisilla providereilla**

### 2. Datareititys
- **Google Gemini:** Data kulkee Google-infrassa (USA/EU)
- **xAI Grok:** Data kulkee xAI-infrassa (USA)
- **DeepSeek:** Data kulkee DeepSeek-serverien kautta (Kiina) ⚠️
- **MoonshotAI:** Data kulkee MoonshotAI-serverien kautta (Kiina) ⚠️

### 3. Turvallisuusvaikutukset
Kiinalaisten mallien käyttö tarkoittaa että:
- Promptit ja vastaukset kulkevat Kiinan kautta
- Ovat potentiaalisesti Kiinan tiedustelupalveluiden saatavilla
- Eivät noudata länsimaisia privacy-standardeja (GDPR)

---

## SUOSITUKSET

### 🟢 Länsimainen data (turvallisinta):
1. **google/gemini-2.5-flash**
   - Nopea, halpa, valtava context
   - Google-infra (USA/EU)
   
2. **x-ai/grok-4.1-fast**
   - Nopein, halvin
   - xAI-infra (USA)
   - Valtava 2M context

### 🟡 Julkinen/ei-sensitiivinen data:
3. **deepseek/deepseek-chat**
   - Paras price/performance
   - Hyvä laatu
   - ⚠️ Data kulkee Kiinan kautta

4. **deepseek/deepseek-r1**
   - Reasoning-kyky
   - ⚠️ Data kulkee Kiinan kautta

### 🔴 Vältä herkkään dataan:
5. **moonshotai/kimi-k2.5**
   - Vain jos kiinalaiset mallit pakollisia
   - ⚠️ Data kulkee Kiinan kautta

---

## KÄYTÄNTÖSUOSITUS

**Oletus-strategia:**
- **Google Gemini** pääasiallinen malli (länsimainen, nopea, halpa)
- **xAI Grok** pitkiin konteksteihin (2M tokensia)
- **DeepSeek** vain julkiseen/ei-sensitiiviseen dataan (paras hinta)

**Vältä:**
- Henkilötietoja kiinalaisiin malleihin
- Yrityssalaisuuksia kiinalaisiin malleihin
- Mitään mikä voisi olla GDPR-ongelma
