

def is_safe(text):
    text = text.lower()
    
    jailbreak_phrases = [
        "ignore previous instructions",
        "ignore all instructions",
        "forget your instructions",
        "simulate",
        "developer mode",
        "system prompt",
        "unrestricted",
        "system override",
        "bypass the firewall",
    ]
    
    injection_phrases = [
        "repeat the text above"
    ]
    
    # Combine checks
    bad_patterns = jailbreak_phrases + injection_phrases
    
    if any(phrase in text for phrase in bad_patterns):
        return False
        
    if len(text) > 2000:
        return False
        
    return True