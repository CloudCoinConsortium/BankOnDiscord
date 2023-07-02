
def getSendWalletName(input_str):
    parts = input_str.split("@")
    if len(parts) != 2:
        return input_str

    user = parts[0]
    network = parts[1]

    if network == "telegram":
        prefix = "tg_"
    elif network == "discord":
        prefix = "dsc_"
    elif network == "whatsapp":
        prefix = "wht_"
    elif network == "skype":
        prefix = "sky_"
    else:
        raise print("Invalid network specified in the input")

    return prefix + user

