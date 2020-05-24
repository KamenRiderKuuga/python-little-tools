def cookieToDic(cookie):
    dic_result={}
    split_List = cookie.split(';')
    for part in split_List:
        split_part = part.split('=',1)
        dic_result[split_part[0]] = split_part[1]
    return dic_result


print(cookieToDic("_AID=12313134; _cliid=D8E_g3APoJzDaCew; scope=snsapi_userinfo; faiOpenId=oosnVwuHCYd0EFyMiLIRy88a0Vp0; hdOpenIdSign_12313134=605e55c2818bcb49b431e3f5e54f57e6; oid_12313134_235=oosnVwuHCYd0EFyMiLIRy88a0Vp0; gps_province=; gps_city="))