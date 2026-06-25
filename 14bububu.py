print ("โปรแกรมตรวจจับความเร็วรถ")

speed = int(input("ความเร็วรถ (Km/h) : "))

if speed <= 80:
    print("ปลอดภัย")
elif speed <= 100:
    print("ตักเตือน")
elif speed <= 120:
    print("เสี่ยงถูกปรับ")
else:
    print("ผิดกฎหมาย (ปรับทันที)")


print("- program by best no.14")