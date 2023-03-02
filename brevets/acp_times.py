"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_acp.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow


#  You MUST provide the following two functions
#  with these signatures. You must keep
#  these signatures even if you don't use all the
#  same arguments.
#

# min speeds and max speeds for brevet distances hours minutes
Z_200 = (15, 34)
Z_400 = (15, 32)
Z_600 = (15, 30)
Z_1000 = (11.428, 28)

final_times = {
   200: (13, 30),
   300: (20, 00),
   400: (27, 00),
   600: (40, 00),
   1000: (75, 00)
}
#================= Errors ======================#
class BrevetDistERROR(Exception):
    """
    This excpetion gets raised when brevet_dist_km input val is invalid
    """
    def __init__(self, brevet_dist_km):
       self.brevet_dist_km = brevet_dist_km
   
    def __str__(self):
       return "brevet_dist_km must be either 200, 300, 400, 600, or 1000. You entered {0}".format(self.brevet_dist_km)

class ControlDistERROR(Exception):
   """
   This exception gets raised when control_dist_km input val is invalid
   """
   def __init__(self, control_dist_km):
      self.control_dist_km = control_dist_km

   def __str__(self):
      return "control_dist_km must be a value >= 0 and <= 120%% of the brevet distance. You entered {0}".format(self.control_dist_km)
   
class BrevetTypeERROR(Exception):
   """
   This exception gets raised when brevet_dist_km is not an integer
   """
   pass

#===============================================#

def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, control distance in kilometers
       brevet_dist_km: number, nominal distance of the brevet
          in kilometers, which must be one of 200, 300, 400, 600,
          or 1000 (the only official ACP brevet distances)
       brevet_start_time:  An arrow object
    Returns:
       An arrow object indicating the control open time.
       This will be in the same time zone as the brevet start time.
    """

    if (brevet_dist_km not in [200, 300, 400, 600, 1000]):
        raise BrevetDistERROR(brevet_dist_km)

    if (control_dist_km < 0 or control_dist_km > 1000):
        raise ControlDistERROR(control_dist_km)

    if (type(brevet_dist_km) != int):
        raise BrevetTypeERROR()

    control_dist_km = round(control_dist_km)
    
    def offset(control_dist_km_temp):
        """
        Offset func for recursive offset calculation.
        """
        if (control_dist_km_temp > 600):
           km_num_left = 600
           speed = Z_1000[1]

        elif (control_dist_km_temp > 400): 
            km_num_left = 400
            speed = Z_600[1]

        elif (control_dist_km_temp > 200):
            km_num_left = 200
            speed = Z_400[1]

        elif (control_dist_km_temp <= 200):
            km_num_left = 0
            speed = Z_200[1]
          
        temp_dist_km = control_dist_km_temp - km_num_left
        offset_hours = temp_dist_km // speed
        offset_min = ((temp_dist_km / speed) - offset_hours) * 60
        control_dist_km_temp = km_num_left
        return offset_hours, offset_min, control_dist_km_temp

    # Recursively Iterate  
    offset_hours = 0
    offset_min = 0
    control_dist_km_temp = control_dist_km
    while(control_dist_km_temp != 0):
        offset_hours_temp, offset_min_temp, control_dist_km_temp = offset(control_dist_km_temp)
        offset_hours += offset_hours_temp
        offset_min += offset_min_temp

    control_start_time = brevet_start_time.shift(hours=+offset_hours, minutes=+round(offset_min))
   
    return control_start_time

def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, control distance in kilometers
          brevet_dist_km: number, nominal distance of the brevet
          in kilometers, which must be one of 200, 300, 400, 600, or 1000
          (the only official ACP brevet distances)
       brevet_start_time:  An arrow object
    Returns:
       An arrow object indicating the control close time.
       This will be in the same time zone as the brevet start time.
    """
    if (brevet_dist_km not in (200, 300, 400, 600, 1000)):
        raise BrevetDistERROR(brevet_dist_km)

    if (control_dist_km < 0 or control_dist_km > (brevet_dist_km * 1.2)):
        raise ControlDistERROR(control_dist_km)

    if (type(brevet_dist_km) != int):
        raise BrevetTypeERROR()
    
    control_dist_km = round(control_dist_km)
    #=================Special Case for early control point================#
    if (control_dist_km < 60):
        
        speed = 20
        offset_hours = control_dist_km // speed
        offset_min = round(((control_dist_km / speed) - offset_hours) * 60)
        offset_hours += 1
        control_end_time = brevet_start_time.shift(hours=+offset_hours, minutes=+offset_min)
        return control_end_time
    #=====================================================================#
    
    def offset(control_dist_km_temp):
        """
        Offset func for recursive offset calculation.
        """
        if (control_dist_km_temp > 600):
           km_num_left = 600
           speed = Z_1000[0]

        elif (control_dist_km_temp > 400): 
            km_num_left = 400
            speed = Z_600[0]

        elif (control_dist_km_temp > 200):
            km_num_left = 200
            speed = Z_400[0]

        elif (control_dist_km_temp <= 200):
            km_num_left = 0
            speed = Z_200[0]
          
        temp_dist_km = control_dist_km_temp - km_num_left
        offset_hours = temp_dist_km // speed
        offset_min = ((temp_dist_km / speed) - offset_hours) * 60
        control_dist_km_temp = km_num_left
        return offset_hours, offset_min, control_dist_km_temp

    # Recursively Iterate  
    offset_hours = 0
    offset_min = 0
    control_dist_km_temp = control_dist_km
    while(control_dist_km_temp != 0):
        offset_hours_temp, offset_min_temp, control_dist_km_temp = offset(control_dist_km_temp)
        offset_hours += offset_hours_temp
        offset_min += offset_min_temp

    if (control_dist_km >= brevet_dist_km):
        control_end_time = brevet_start_time.shift(hours=+final_times[brevet_dist_km][0], minutes=+final_times[brevet_dist_km][1])
    else:
        control_end_time = brevet_start_time.shift(hours=+offset_hours, minutes=+round(offset_min))
   
    return control_end_time