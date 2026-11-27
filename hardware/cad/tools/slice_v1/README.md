# น้ำหนักเส้นจาก slicer ต่อชิ้น (หุ่นโชว์ V1)
PrusaSlicer 2.7 CLI (`apt install prusa-slicer`) · ค่าตาม `public/hardware/print-settings.md` · หมุนชิ้นอัตโนมัติให้ซัพพอร์ตน้อยสุด · organic support จากเตียงเท่านั้น · ไม่มี brim/skirt
```
python3 pieces.py && python3 orient.py
python3 -c "import json,os;W=os.environ.get('SLICE_WORK','/tmp/slice_v1');[print(x['job'],'pla_black' if x['prof']=='pla_shell' and x['mat']=='PLA ดำ' else x['prof']) for x in json.load(open(W+'/jobs.json'))]" | xargs -P 2 -L 1 ./run1.sh > $SLICE_WORK/results.txt
python3 summ.py   # → cad/out/show_v1_slice_weights.json
```
ความหนาแน่น: PLA Matte 1.31 · PLA Basic ดำ 1.26 · PETG-CF 1.25 · PAHT-CF 1.06 · TPU 1.22 · PC 1.20 g/cm³ · Bambu Studio อาจต่าง ±10%
