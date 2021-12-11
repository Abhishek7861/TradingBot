class Basket:
    def __init__(self,id,name,slPercent,bpPercent,active):
        self.id = id
        self.name = name
        self.slPercent = slPercent
        self.bpPercent = bpPercent
        self.active = active


    def display(self):
        print("-----------------------------------")
        print("id: ",self.id,
        "| Name: ",self.name,
        "| SL(%) : ",self.slPercent,
        "| BP(%) :",self.bpPercent,
        "| Status: ",self.active)
        print("-----------------------------------")