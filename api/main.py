from fastapi import FastAPI
from api_routes import ai_summary, statement, risk, portfolio, agent

app = FastAPI(title="SODA-Finance API")

# Register routers
app.include_router(ai_summary.router)
app.include_router(statement.router)
app.include_router(risk.router)
app.include_router(portfolio.router)
app.include_router(agent.router)

@app.get("/")
def root():
    return {"message": "SODA-Finance API is running"}
