def find_common_characters(msg1,msg2):
    msg1=msg1.replace(" ","")
    msg2=msg2.replace(" ","")
    common_chars=set(msg1).intersection(set(msg2))  #find common characters
    if not common_chars:
        return -1
    return sorted(common_chars)

msg1="I like python"
msg2="Java is very popular language"
common_characters = find_common_characters(msg1,msg2)
print(common_characters)
