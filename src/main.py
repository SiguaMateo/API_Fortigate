try:
    from fastapi import FastAPI, HTTPException
    import httpx
    import pandas as pd
    from pathlib import Path
    from dotenv import load_dotenv
    import os
    print("Librerias importadas")
except Exception as e:
    print(f"Ocurrio un error al importar las librerias, {e}")

# Cargar variables de entorno
load_dotenv()

API_URL = os.getenv("FORTIGATE_API_URL")
API_TOKEN = os.getenv("API_TOKEN")

app = FastAPI(
    title="API Fortinet",
    description="API para monitorear la data de Fortinet",
    version="1.0.0"
)

# Ruta del archivo Excel
EXCEL_FILE = Path("fortigate_policy.xlsx")

@app.get("/")
def root():
    return {"message": "Bienvenido a la API para obtener datos de FortiGate"}

@app.get("/fetch-data")
async def fetch_data():
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    
    try:
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.get(API_URL, headers=headers)
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Error al obtener datos: {response.text}",
            )

        data = response.json().get("results", [])
        
        if not data:
            return {"message": "No hay datos disponibles"}

        # Procesar y guardar los datos en un archivo Excel
        df = pd.DataFrame(data)
        df.to_excel(EXCEL_FILE, index=False)
        return {"message": "Datos guardados exitosamente en fortigate_data.xlsx", "data_count": len(data)}

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
# if __name__ == "__main__":
#     config = uvicorn.Config("main:app", port=9994, log_level="info", reload=True)
#     server = uvicorn.Server(config)
#     server.run()