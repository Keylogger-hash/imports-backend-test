from fastapi import FastAPI
from fastapi import Depends
from validation_models.models import ImportsCitizen,CitizensList,CitizensList, ValidationCitizen,Percentiles,BirthdaysPercentile
import fastapi_asyncpg
import random
app = FastAPI()


db = fastapi_asyncpg.configure_asyncpg(app,"postgresql://postgres:123@localhost:5432/citizens")

@db.on_init
async def initialization(conn):
    await conn.execute("SELECT 1")

@app.post('/imports')
async def imports(imports:ImportsCitizen,db=Depends(db.connection)):

    query = f"""INSERT INTO public.imports_citizens
    (import_id,citizen_id,town,street,building,apartment,name,birth_date,gender,relatives)
    VALUES($1,$2,$3,$4,$5,$6,$7,$8,$9,$10)"""
    rows = []
    systemrandom = random.SystemRandom()
    import_id = systemrandom.randint(1000000,10000000)

    for cit in imports.citizens:
        await db.execute(query,import_id,cit.citizen_id,cit.town,cit.street,cit.building,cit.apartment,cit.name,cit.birth_date,cit.gender.value,cit.relatives)

    return {"data":{"import_id":import_id}} 

@app.patch('/imports/{import_id}/citizens/{citizen_id}')
async def change_info(import_id:int, citizen_id: int):
    pass

@app.get('/imports/{import_id}/citizens')
async def citizens_list(import_id:int,db=Depends(db.connection)):
    query = f"SELECT citizen_id,town,street,building,apartment,name,birth_date,gender,relatives FROM public.imports_citizens WHERE import_id={import_id}"
    rows = await db.fetch(query)
    data = []
    for row in rows:
        data.append(ValidationCitizen(**row))
    clist = CitizensList(data=data)
    return clist

@app.get('/imports/{import_id}/citizens/birthdays')
async def citizens_birthdays(import_id:int,db=Depends(db.connection)):
    query = f"""SELECT 
	DATE_PART('year',birth_date) as year_part,
	DATE_PART('month',birth_date) as month_part,
	COUNT(*) FROM public.imports_citizens 
	WHERE import_id={import_id}
	GROUP BY DATE_PART('year',birth_date),
			 DATE_PART('month',birth_date)
	ORDER BY year_part DESC,month_part DESC;"""
    rows = await db.fetch(query)
    
    return rows


@app.get("/imports/{import_id}/towns/stat/percentile/age")
async def imports_percentile(import_id:int,db=Depends(db.connection)):
    query = f"""select 
	town, 
	ROUND(percentile_cont(0.5) 
	within group(
		order by DATE_PART('year',AGE(now(),birth_date))
	)::numeric,2) as p50,
	ROUND(percentile_cont(0.75)
	within group(
		order by DATE_PART('year',AGE(now(),birth_date))
	)::numeric,2)
		as p75,
	ROUND(percentile_cont(0.99)
	within group(
		order by DATE_PART('year',AGE(now(),birth_date))
	)::numeric,2)
		as p99
	from public.imports_citizens
	WHERE import_id={import_id}
		GROUP BY town
    """
    rows = await db.fetch(query)
    data = []
    for row in rows:
        data.append(Percentiles(**row))
    b = BirthdaysPercentile(data=data)
    return b