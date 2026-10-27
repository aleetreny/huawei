import re
PAT=[('BOOM','Old landmines'),('DEBT','Payday just means'),('SKILLBEHIND','jargon you cannot keep up'),('ISOL','nobody asks you to lunch'),
('DIGNO','no self-respect left'),('FELLSHORT','This half-year review fell short'),('TOOFAST','You climbed too fast'),
('SENIOR','A senior colleague takes you aside'),('OLDHAND','old hand claps you'),('STANDUP','After standup your manager keeps you back'),
('PEER','diligent peer whispers'),('MENTOR','Your mentor texts'),('TALK','[Half-year talk]'),('PROMO','Promotion notice'),('SALARY','Monthly base salary')]
HR=(('smiling',0),('quietly',1),('frowning',2),('uneasy',3),('angry',4))
def tags(t):
    out=[k for k,p in PAT if p in t]
    m=re.search(r'Half-year performance bonus \((\w)\)',t)
    if m: out.append('G'+m.group(1))
    return out
def hr(t):
    m=re.search(r"An HR partner you get on with says,? (\w+)", t or "")
    if not m: return None
    for w,l in HR:
        if m.group(1).startswith(w): return l
