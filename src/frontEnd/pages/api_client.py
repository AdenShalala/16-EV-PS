import os
import httpx

API_BASE = os.getenv('SOCKETFIT_API', 'http://127.0.0.1:5000')

async def get_patients_by_clinician_id(clinician_id: str):
    url = f'{API_BASE}/patients/{clinician_id}'
    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.get(url)
        r.raise_for_status()
        return r.json()
