total_kor = 0
total_eng = 0
for i in range(1, 46):
	o_k = open("../../data/Herald/sample/kor/"+str(i)+".txt", "r", encoding="UTF8")
	o_e = open("../../data/Herald/sample/eng/"+str(i)+".txt", "r", encoding="UTF8")

	o_k_ls = o_k.readlines()
	o_e_ls = o_e.readlines()

	total_kor += len(o_k_ls)
	total_eng += len(o_e_ls)

print("total kor : ",total_kor,"\ntotal eng : ",total_eng)
