import spacy
from spacy.pipeline import EntityRuler

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

# Example text containing mentions of companies and stocks
text = """
Kotak Mahindra Bank faced regulatory action from the RBI due to significant concerns arising from the bank's non-compliance with IT regulations. 
The bank was found to be deficient in its IT risk and information security governance for two consecutive years, and it failed to address corrective action plans issued by the RBI in 2022 and 2023. 
Serious deficiencies and non-compliances were observed in various areas of IT management, leading to frequent and significant outages in the bank's core banking system and digital channels. 
The RBI took action to prevent prolonged outages that could impact customer service and the financial ecosystem of digital banking and payment systems.

Zscaler: How an Indian-American builds cyber-shields for global giants

From a poor village in Himachal Pradesh to founding a $2-billion company, Jay Chaudhry's journey is inspiring..
"""

# Initialize EntityRuler
ruler = EntityRuler(nlp, overwrite_ents=True)

# Define patterns for stock names
patterns = [
    {"label": "STOCK", "pattern": [{"IS_UPPER": True, "OP": "+"}]}  # Match sequences of capitalized words
]

# Add patterns to the ruler
ruler.add_patterns(patterns)

# Add the ruler to the pipeline before ner
nlp.add_pipe(ruler, before='ner')

# Process the text with the modified pipeline
doc = nlp(text)

# Extract entities identified as stocks
stocks = []
for ent in doc.ents:
    if ent.label_ == "STOCK":
        stocks.append(ent.text)

print("Stock names found:", stocks)
