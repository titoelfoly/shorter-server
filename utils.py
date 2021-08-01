alphanumeric = {"1":'o','2':'t','3':"t",'4':"f",'5':"f",'6':"s",'7':"s",'8':"e",'9':"n",'0':"z",'.':"d"}
def slugify(t):
    slug=""
    for i in str(t):
        slug += alphanumeric[i]
    return slug
