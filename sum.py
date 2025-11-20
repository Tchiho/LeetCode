class Func:
    def func(self, a: int, b: int, c: int):
        templist = [1,2,3,4,5,6,7,8,9]
        for i in range(0, len(templist)):
            if i <= 6:
                for j in range(i+1, len(templist)):
                    if j <= 7:
                        for k in range(j+1, len(templist)):
                            temp = templist[i] + templist[j] + templist[k]
                            # print(f"i={i},j={j},k={k},temp={temp}")
                            if temp == a:
                                print(f"a = {templist[i]} + {templist[j]} + {templist[k]}")
                            elif temp == b:   
                                print(f"b = {templist[i]} + {templist[j]} + {templist[k]}")
                            elif temp == c:
                                print(f"c = {templist[i]} + {templist[j]} + {templist[k]}")

        return  
    
if __name__ == "__main__":
    f = Func()
    f.func(15,17,13)   