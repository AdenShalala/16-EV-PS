from xml.dom.minidom import parse

def XMLInsert():
    dom = parse('DummyPatientData.xml')
    users = dom.getElementsByTagName('Users')[0]
    for user in users.getElementsByTagName('User'):
        clinician_id = user.getAttribute('ClinicianID')
        month_year_birth = user.getElementsByTagName('MonthYearOfBirth')[0].firstChild.nodeValue
        gender = user.getElementsByTagName('Gender')[0].firstChild.nodeValue
        height = user.getElementsByTagName('Height_cm')[0].firstChild.nodeValue
        weight = user.getElementsByTagName('Weight_kg')[0].firstChild.nodeValue
        amputation_type = user.getElementsByTagName('AmputationType')[0].firstChild.nodeValue
        socket_type = user.getElementsByTagName('SocketType')[0].firstChild.nodeValue
        first_fitted = user.getElementsByTagName('FirstProsthesisFitted')[0].firstChild.nodeValue
        hours_per_week = user.getElementsByTagName('FirstProsthesisFitted')[0].firstChild.nodeValue
        distance_per_week = user.getElementsByTagName('DistancePerWeek_km')[0].firstChild.nodeValue
        for activity in user.getElementsByTagName('Activity'):
            end_time = activity.getAttribute('EndTime')
            start_time = activity.getAttribute('StartTime')
            activity_type = activity.getAttribute('Type')
            for sensor in activity.getElementsByTagName('Sensor'):
                location = sensor.getAttribute('Location')
                sensor_type = sensor.getAttribute('Type')
                pressure_tolerance = sensor.getElementsByTagName('PressureTolerance')[0].firstChild.nodeValue
                signal_output = sensor.getElementsByTagName('Signal')[0].firstChild.nodeValue
                signalnums = signal_output.replace("[", "")
                signalnums = signalnums.replace("]", "")
                signalList = signalnums.split(';')
                time_stamp = sensor.getElementsByTagName('Timestamp')[0].firstChild.nodeValue
                timenums = time_stamp.replace("[", "")
                timenums = timenums.replace("]", "")
                timeList = timenums.split(" ")
                point_of_interest = sensor.getElementsByTagName('PointsOfInterest')[0].firstChild.nodeValue
                poinums = point_of_interest.replace("[", "")
                poinums = poinums.replace("]", "")
                poiList = poinums.split(" ")

XMLInsert()