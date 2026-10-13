from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
import os
os.makedirs('fonts/ttf',exist_ok=True)
f=TTFont('fonts/DepartureMono-Regular.woff2'); f.flavor=None; f.save('fonts/ttf/DepartureMono-Regular.ttf')
for w in [400,500,600,700]:
    f=TTFont('fonts/JetBrainsMono-latin.woff2'); f.flavor=None
    print('axes',[a.axisTag for a in f['fvar'].axes]) if w==400 else None
    i=instancer.instantiateVariableFont(f,{'wght':w}); i.save(f'fonts/ttf/JetBrainsMono-{w}.ttf')
print(os.listdir('fonts/ttf'))
