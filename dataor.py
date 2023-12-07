def update_data():
    with open("data.txt", "r") as f:
        data = f.readlines()
        
    data = int(data[-1])
    
    data += 1
    
    with open("data.txt", "a") as f:
        f.write(f"\n{data}")