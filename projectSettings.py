tok = "7283309704:AAEoH8VZqaJdw_ilXQ363LsZKK4sOZ4Cwug"
id_vladelec = "870264076" #ваш id, можно получить в любом подходяящем боте. напрмер бот - get my id
host = False

misic = {
    "1":{
        "name": "Метал",
        "subgenre": {
            "1": "блэк",
            "2": "трэш",
            "3": "кристианский",
            "4": "спид",
            "5": "хэви"
        },
        "kol": 0,
    },
    "2": {
        "name": "Поп",
        "subgenre": {
            "1": "K",
            "2": "евро",
            "3": "электро",
            "4": "J",
        },
    },
    "3": {
        "name": "Рок",
        "subgenre": {
            "1": "панк"
        }
    }
}

def money_form(mon):
    mon = str(mon)
    idd = -1
    ctr = 1
    rez = ""
    for i in range(len(mon)):
        if ctr == 4:
            ctr = 1
            rez += " "
        rez += mon[idd]
        ctr += 1
        idd -= 1

    rez = rez[::-1]
    return rez