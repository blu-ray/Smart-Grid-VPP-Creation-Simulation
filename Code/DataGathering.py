import requests


base_address = "http://reports.ieso.ca/public/GenOutputCapability/"

year_st = '2020'
month_st = '01'
for day in range(1, 32):
    day_st = str(day)
    if len(day_st) < 2:
        day_st = '0' + day_st

    address = base_address + f"PUB_GenOutputCapability_{year_st}{month_st}{day_st}.xml"

    r = requests.get(address)
    print(f"data_{year_st}{month_st}{day_st} Done")
    with open(f"Data\\data_{year_st}{month_st}{day_st}.xml", 'wb') as write_file:
        write_file.write(r.content)

