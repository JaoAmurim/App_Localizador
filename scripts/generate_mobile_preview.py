from PIL import Image, ImageDraw, ImageFont
import os

out_path = os.path.join('img', 'mobile_preview.png')
W, H = 393, 873
bg = Image.new('RGBA', (W, H), '#2f3940')

pad = 12
inner = Image.new('RGBA', (W-2*pad, H-2*pad), '#f6f7f8')
inner_draw = ImageDraw.Draw(inner)
header_h = 72
inner_draw.rectangle([0,0, W-2*pad, header_h], fill='#0A1C40')

logo_path = os.path.join('img','logo.png')
if os.path.exists(logo_path):
    try:
        logo = Image.open(logo_path).convert('RGBA')
        logo.thumbnail((56,40), Image.Resampling.LANCZOS)
        inner.paste(logo, (12, 14), logo)
    except Exception:
        pass

# Fonts fallback
try:
    font_b = ImageFont.truetype('arialbd.ttf', 20)
    font_r = ImageFont.truetype('arial.ttf', 13)
except Exception:
    font_b = ImageFont.load_default()
    font_r = ImageFont.load_default()

inner_draw.text((88, 22), 'RIOFER | NAVEGAÇÃO RÁPIDA', font=font_b, fill='white')

# page title
try:
    font_title = ImageFont.truetype('arialbd.ttf', 18)
except Exception:
    font_title = font_b
inner_draw.text((24, header_h+18), 'Selecione seu Destino', font=font_title, fill='#0A1C40')

# description wrap
desc = 'Escolha onde você quer ir: disponibilizamos a opção de abrir a rota no Google Maps ou Waze.'
lines = []
words = desc.split()
line = ''
for w in words:
    if len(line + ' ' + w) > 45:
        lines.append(line.strip())
        line = w
    else:
        line += ' ' + w
if line:
    lines.append(line.strip())

y = header_h+52
for ln in lines:
    inner_draw.text((24, y), ln, font=font_r, fill='#475157')
    y += 18

# cards
card_w = int((W-2*pad-14)/2)
card_h = 140
cy = int(y+14)
for i, title in enumerate(['MATRIZ RIOFER','RIOFER DEPÓSITO','BALANÇA RIOFER']):
    col = i % 2
    row = i // 2
    x = 12 + int(col*(card_w+14))
    y0 = cy + row*(card_h+12)
    inner_draw.rounded_rectangle([x, y0, x+card_w, y0+card_h], radius=14, fill='white', outline='#e6e9eb')
    cx_icon = x + int(card_w/2)
    inner_draw.ellipse([cx_icon-28, y0+12, cx_icon+28, y0+12+56], fill='#f4f7fb', outline='#dfe8ee')
    inner_draw.ellipse([cx_icon-6, y0+28, cx_icon+6, y0+40], fill='#FF7F00')
    try:
        fnt_title = ImageFont.truetype('arialbd.ttf', 14)
    except Exception:
        fnt_title = font_b
    inner_draw.text((x+12, y0+72), title, font=fnt_title, fill='#0A1C40')
    inner_draw.text((x+12, y0+96), 'Entrega / Recebimento' if i==0 else ('Escritórios / Recebimento' if i==1 else 'Pesagem / Saída de Cargas'), font=font_r, fill='#5f6b73')

# note (less dominant)
note_y = cy + 2*(card_h+12) + 8
inner_draw.rounded_rectangle([24, note_y, inner.size[0]-24, note_y+78], radius=10, fill='#FFB07A', outline=None)
try:
    fnt_note_b = ImageFont.truetype('arialbd.ttf', 13)
except Exception:
    fnt_note_b = font_b
inner_draw.text((44, note_y+14), 'IMPORTANTE:', font=fnt_note_b, fill='white')
inner_draw.text((44, note_y+36), 'Após a seleção, você escolherá o aplicativo (Google Maps ou Waze) para iniciar a rota.', font=font_r, fill='white')

bg.paste(inner, (pad, pad))
os.makedirs('img', exist_ok=True)
bg.save(out_path)
print('Saved:', out_path)
