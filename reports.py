from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from sqlalchemy.orm import joinedload
import models

def generar_reporte_pdf(db):
    personajes = (
        db.query(models.Character)
        .options(
            joinedload(models.Character.secret_identity),
            joinedload(models.Character.teams).joinedload(models.CharacterTeam.team)
        )
        .all()
    )

    nombre_archivo = "reporte_marvel.pdf"
    doc = SimpleDocTemplate(nombre_archivo, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()

    story.append(Paragraph("Reporte Marvel API", styles["Title"]))
    story.append(Spacer(1, 12))

    for c in personajes:
        identidad = c.secret_identity.real_name if c.secret_identity else "Desconocida"
        equipos = ", ".join([t.team.name for t in c.teams if t.team]) if c.teams else "Ninguno"
        story.append(Paragraph(f"<b>Personaje:</b> {c.name}", styles["Heading3"]))
        story.append(Paragraph(f"Identidad secreta: {identidad}", styles["Normal"]))
        story.append(Paragraph(f"Equipos: {equipos}", styles["Normal"]))
        if c.image_url:
            story.append(Paragraph(f"Imagen: {c.image_url}", styles["Normal"]))
        story.append(Spacer(1, 10))

    doc.build(story)
    return nombre_archivo