CREATE DATABASE IF NOT EXISTS public.citizens;
CREATE TYPE  gender_type AS ENUM ('male','female');
CREATE TABLE IF NOT EXISTS public.imports_citizens (
	id SERIAL PRIMARY KEY,
 	import_id INTEGER UNIQUE CHECK(import_id>0),
	citizen_id INTEGER CHECK(citizen_id>0),
	town varchar(255) NOT NULL,
	street varchar(255) NOT NULL,
	building varchar(255) NOT NULL,
	apartment integer CHECK(apartment > 0),
	name varchar(255) NOT NULL,
	birth_date DATE,
	gender gender_type,
	relatives INTEGER ARRAY
);