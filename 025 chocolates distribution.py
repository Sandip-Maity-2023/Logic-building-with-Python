child_id=(10,20,30,40,50)
chocolates_received=[12,5,3,4,6]
def calculate_total_chocolates():
    total_chocolates=sum(chocolates_received)
    return total_chocolates
def reward_child(child_id_rewarded,extra_chocolates):
         global chocolates_received
         if extra_chocolates<1:
            print("Extra_chocolates is less than 1")
    print(chocolates_received)

         if child_id_rewarded not in child_id:
            print("child_id is invalid")
    print(chocolates_received)
            return
    index=child_id.index(child_id_rewarded)
    chocolates_received[index]+=extra_chocolates
    print(chocolates_received)
    reward_child(20,2)