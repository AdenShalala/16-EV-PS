# for testing only
from MongoDB_read import read_patients_by_clinician_id

if __name__ == "__main__":
    clinician_id = "c123"
    patients = read_patients_by_clinician_id(clinician_id)
    print(f"find {len(patients)} patients")
    
    for p in patients:
        print(f"- clinicianID: {p.clinician_id}")
        print(f"  activities: {len(p.activities)}")
        
        for a in p.activities:
            print(f"  * activity type: {a.type}, start: {a.start_time}, end: {a.end_time}")
            print(f"    sensors: {len(a.sensors)}")
            
            for s in a.sensors:
                print(f"    - location: {s.location}, type: {s.type}")
                print(f"      signals: {len(s.signal)}, timestamp: {len(s.timestamp)}, POIs: {s.points_of_interest}")