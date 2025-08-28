# 🐾 KittyCheck – Gatitos con Propósito

Sistema de **control y seguimiento de desparasitación felina** con cálculo de dosis por peso, registro de controles y predicción automática de la fecha del próximo control.

## ✨ Características
- Registro de gatos (nombre, edad, peso, sexo, etapa).
- Registro de desparasitantes (auto-alta si no existe, con dosis base en mg/kg).
- Cálculo de **dosis total (mg)** según peso y dosis base.
- Predicción de **próximo control** según la edad:
  - < 3 meses → cada **15 días**
  - 3–6 meses → cada **30 días**
  - > 6 meses → cada **90 días** (ajustable)
- Frontend estático servido por FastAPI.
- Alertas visuales en historial: **Rojo = vencido**, **Amarillo = próximo**, **Verde = ok**.

## 🧱 Estructura
```
kittycheck/
├─ backend/
│  └─ app/
│     ├─ main.py
│     ├─ database.py
│     ├─ models.py
│     └─ schemas.py
│  └─ requirements.txt
├─ frontend/
│  └─ index.html
└─ render.yaml
```

## 🚀 Ejecución local
Requisitos: Python 3.10+

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Abre en el navegador: `http://127.0.0.1:8000`  
Verás la API docs en: `http://127.0.0.1:8000/docs`

## 🗄️ Base de datos
Por defecto se usa **SQLite** en `kittycheck.db`.  
En producción (Render) usa una instancia de **PostgreSQL** y define `DATABASE_URL` en el servicio.

Ejemplos:
- SQLite (default): `sqlite:///./kittycheck.db`
- PostgreSQL: `postgresql://USER:PASSWORD@HOST:PORT/DBNAME`

## ☁️ Deploy en Render
1. Sube este repo a GitHub.
2. En Render, crea **New Web Service** desde el repo.
3. (Opcional) Crea **PostgreSQL on Render** y asigna su `DATABASE_URL` al servicio.
4. Render levantará la app en `https://<tu-app>.onrender.com/` y servirá el frontend.

## 📡 Endpoints
- `GET /api/cats`
- `POST /api/cats`
- `GET /api/dewormers`
- `POST /api/dewormers`
- `GET /api/controls`
- `POST /api/controls`

### Ejemplo POST /api/controls
```json
{
  "cat_name": "Luna",
  "age_months": 2,
  "weight_g": 1200,
  "sex": "H",
  "stage": "Gatito",
  "dewormer": "Fenbendazol",
  "date": "2025-08-28",
  "notes": "Primera dosis"
}
```
Si envías un desparasitante nuevo:
```json
{
  "cat_name": "Max",
  "age_months": 4,
  "weight_g": 3500,
  "sex": "M",
  "stage": "Gatito",
  "dewormer": "Milbemicina",
  "base_dose_mg_per_kg": 2.0,
  "date": "2025-08-28"
}
```