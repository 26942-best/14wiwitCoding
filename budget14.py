price_1 = float(input("ราคาสินค้า 1 : "))
amount_1 = int(input("จำนวนสินค้า 1 : "))
price_2 = float(input("ราคาสินค้า 2 : "))
amount_2 = int(input("จำนวนสินค้า 2 : "))
#-------------------------------------------------
total_1 = price_1 * amount_1
total_2 = price_2 * amount_2
final_total = total_1 + total_2
#-------------------------------------------------
print("ค่าใช้จ่ายทั้งหมดคือ : ",final_total ,"บาท")