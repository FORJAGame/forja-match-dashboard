# FORJA Match Dashboard

Dashboard do FORJA Match para análise dos dados coletados

## Stack

- Python
- Streamlit
- Pandas
- Plotly
- Firebase Admin SDK

## Preparar o ambiente

```powershell
pip install -r requirements.txt
```

## Rodar localmente

```powershell
streamlit run app.py
```

Se o Firebase ainda nao estiver configurado, o app usa automaticamente os dados
de exemplo em `data/sample_sessions.json`.

## Qualidade

```powershell
pytest
```
