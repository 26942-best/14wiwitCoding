name = input("คุณชื่ออะไรหรอ : ")
score = int(input("คะแนนละ? : "))
bonus = float(input("มีโบนัสไหม? : "))
total = score + bonus
print("คะแนนรวม :" , total, "คะแนน")
print("ขอบคุณ" , name,"ที่มาทำแบบทกสอบครับ🐱")

------------------------------------------------------------------

price = int(input("ราคาต่อแก้ว (บาท): "))
quantity = int(input("จำนวนแก้ว: "))
discount_percent = float(input("ส่วนลด (%): "))
total_before_discount = price * quantity
discount_amount = total_before_discount * (discount_percent / 100)
net_total = total_before_discount - discount_amount
print("ราคารวมก่อนส่วนลด:", total_before_discount, "บาท")
print("ส่วนลด:", discount_amount, "บาท")
print("ยอดที่ต้องชำระ:", net_total, "บาท")
