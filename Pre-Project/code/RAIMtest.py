import data_handler as data
import Library_GNSS as GNSS
import numpy as np
pdop, sat_view, sat_tot, satinview_ecef = data.compute_satellite_data(2024, 12, 22, 19, 25, 0, 13.683529, 100.619786, 0)
#print(pdop)

#print(satinview_ecef)
origin_lat = 13.683529
origin_lon = 100.619786
origin_alt = 0
#print(pdop)
#print(len(satinview_ecef))
num_sat = len(satinview_ecef)  
print("Satellite in view: ",num_sat)   
#num_sat = 5
if num_sat >= 4:
    pdop4sat = GNSS.cal_pdop(satinview_ecef, GNSS.latlon_to_ecef(origin_lat, origin_lon, origin_alt))
    #pdop = 7
    #print(pdop) 
    if pdop4sat < 6:
        print("Position Available")
    else:
        print("PDOP too high")
        print("Position Not Available")
else:
    print("Position Not Available")

if num_sat >= 5:
    satinview_ecefgroupX_1 = GNSS.combinationX_1(satinview_ecef)
    pdopX1 = []
    for i in range (len(satinview_ecefgroupX_1)):
        pdop = GNSS.cal_pdop(satinview_ecefgroupX_1[i], GNSS.latlon_to_ecef(origin_lat, origin_lon, origin_alt))
        pdopX1.append(pdop)
    #print(len(pdopX1))
    
    #pdop = 7
    #print(pdop) 
    if max(pdopX1) < 6:
        print("RAIM FD Available")
    else:
        print("PDOP too high")
        print("RAIM FD Not Available")
else:
    print("RAIM FD Not Available")


if num_sat >= 6:
    satinview_ecefgroupX_2 = GNSS.combinationX_2(satinview_ecef)
    pdopX2 = []
    for i in range (len(satinview_ecefgroupX_2)):
        pdop = GNSS.cal_pdop(satinview_ecefgroupX_2[i], GNSS.latlon_to_ecef(origin_lat, origin_lon, origin_alt))
        pdopX2.append(pdop)
    #print(len(pdopX2))
   
    #pdop = 7
    #print(pdop) 
    if max(pdopX2) < 6:
        print("RAIM FDE Available")
    else:
        print("PDOP too high")
        print("RAIM FDE Not Available")
else:
    print("RAIM FDE Not Available")

pdopAll = pdopX1 + pdopX2
satellite_groups = satinview_ecefgroupX_1 + satinview_ecefgroupX_2

# Combine PDOP values with their corresponding satellite groups
pdop_with_satellites = list(zip(pdopAll, satellite_groups))

# Sort the combined list by PDOP values
pdop_with_satellites_sorted = sorted(pdop_with_satellites)

# Get the lowest 3 and highest 3 PDOP values with their satellite groups
lowest_3_pdop_with_satellites = pdop_with_satellites_sorted[:3]
highest_3_pdop_with_satellites = pdop_with_satellites_sorted[-3:]

print("PDOP: ", pdopAll)
print("Lowest 3 PDOP values with satellite positions: ", lowest_3_pdop_with_satellites)
print("Highest 3 PDOP values with satellite positions: ", highest_3_pdop_with_satellites)