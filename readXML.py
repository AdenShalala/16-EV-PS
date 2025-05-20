from xml.dom.minidom import parse

dom = parse('DummyPatientData.xml')
users = dom.getElementsByTagName('Users')[0]
for user in users.getElementsByTagName('User'):
    clinicianID = user.getAttribute('ClinicianID')
    birthMonth = user.getElementsByTagName('MonthYearOfBirth')[0].firstChild.nodeValue
    gender = user.getElementsByTagName('Gender')[0].firstChild.nodeValue
    height = user.getElementsByTagName('Height_cm')[0].firstChild.nodeValue
    amputationType = user.getElementsByTagName('AmputationType')[0].firstChild.nodeValue
    socketType = user.getElementsByTagName('SocketType')[0].firstChild.nodeValue
    firstFitted = user.getElementsByTagName('FirstProsthesisFitted')[0].firstChild.nodeValue
    hpWeek = user.getElementsByTagName('FirstProsthesisFitted')[0].firstChild.nodeValue
    distanceWeek = user.getElementsByTagName('DistancePerWeek_km')[0].firstChild.nodeValue
    for activity in user.getElementsByTagName('Activity'):
        actEndTime = activity.getAttribute('EndTime')
        actStartTime = activity.getAttribute('StartTime')
        actType = activity.getAttribute('Type')
        for sensor in activity.getElementsByTagName('Sensor'):
            senLoc = sensor.getAttribute('Location')
            senType = sensor.getAttribute('Type')
            pressureTol = sensor.getElementsByTagName('PressureTolerance')[0].firstChild.nodeValue
            signal = sensor.getElementsByTagName('Signal')[0].firstChild.nodeValue
            timestamp = sensor.getElementsByTagName('Timestamp')[0].firstChild.nodeValue
            poi = sensor.getElementsByTagName('PointsOfInterest')[0].firstChild.nodeValue