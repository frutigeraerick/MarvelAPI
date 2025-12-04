from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from database import get_db
import reports, crud

router = APIRouter(tags=["Reports"])

@router.get("/report/pdf")
def api_generate_pdf(db = Depends(get_db)):
    try:
        archivo = reports.generar_reporte_pdf(db)
        return FileResponse(archivo, media_type="application/pdf", filename="reporte_marvel.pdf")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/report/stats")
def api_stats(db = Depends(get_db)):
    return crud.get_stats(db)