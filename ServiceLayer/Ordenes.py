import httpx
codigo = "httpx.get('https://www.example.org/')"
r = eval(codigo)

print(r.text)

