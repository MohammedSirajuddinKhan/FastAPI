from fastapi import FastAPI

app=FastAPI()

@app.get('/')
def root():
    return {"Message":"Is ts tuff..?"}

@app.get('/products/{id}')
def get_products(id:int):
    products=['tws','monitor','laptop','mouse']
    return products[id]