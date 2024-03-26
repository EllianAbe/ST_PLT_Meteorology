import calendar


months = {name: number for number, name in enumerate(calendar.month_name)}

columns = {'all': ['precip', 'temp_media', 'um_relativa', 'vel_vento'],
           'only precipitation': ['precip'],
           'only temperature': ['temp_media'],
           'only humidity and wind': ['um_relativa', 'vel_vento']}
