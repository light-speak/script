
text = "\\u0051\\u0051\\u002d\\u0032\\u0034\\u0032\\u0033\\u0034\\u0032\\u0032\\u0032\\u004e\\u0041\\u004d\\u0045\\u002d\\u0048\\u0045\\u004c\\u0047\\u0052\\u004f\\u0055\\u0050\\u002d\\u0032\\u0033\\u0032\\u0033\\u0032\\u0033\\u0032\\u0033\\u0047\\u004e\\u0041\\u004d\\u0045\\u002d\\u6d4b\\u8bd5\\u003d\\u003d\\u003d\\u0075\\u0066\\u0061\\u0067\\u0049\\u0052\\u0073\\u0058\\u006e\\u0039\\u0032\\u0030\\u0031\\u0038\\u0038\\u0033\\u0032\\u0034\\u0036\\u0039"
text = text.replace('\\\\','\\')
print(type(text))
print(repr(text))


# text = text.encode('utf-8').decode('utf-8','ignore')
text = text.encode('utf-8').decode("unicode_escape");
print(type(text))
print(text)
# text = text.decode('utf-8','ignore')
# text = repr(text)
# print(type(text))
# print(text)