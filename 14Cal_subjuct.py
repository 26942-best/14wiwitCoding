print("โปรแกรมคำนวณคะแนน 3 วิชา")

Sub_1 = int(input("คะแนนวิชาที่ 1 : "))

Sub_2 = int(input("คะแนนวิชาที่ 2 : "))

Sub_3 = int(input("คะแนนวิชาที่ 3 : "))

Total = (Sub_1 + Sub_2 + Sub_3) /3
All = Sub_1 + Sub_2 + Sub_3

print("คะแนนรวมของคุณคือ : ",All ,)
print("คะแนนเฉลี่ยของคุณคือ : ",Total ,)

if Total >= 80 :
    print("ดีเยี่ยม")
elif Total >= 60 :
    print("ผ่าน")
else:
    print("ควรปรับปรุง")
