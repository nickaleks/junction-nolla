CREATE TABLE user(
    id SERIAL NOT NULL,
    customer_id BIGINT UNIQUE
    PRIMARY KEY (id)
);

-- CREATE TABLE product(
--     id SERIAL NOT NULL,
--     ean VARCHAR, 
--     name VARCHAR, 
--     marketing_name VARCHAR, 
--     brand VARCHAR, 
--     manufacturer VARCHAR, 
--     weight double precision, 
--     nutritional_properties, 
--     cautionary_notes VARCHAR, 
--     is_alcohol BOOLEAN, 
--     alcohol_content double precision, 
--     vitamin_d double precision, 
--     enrgy_kcal, 
--     energy_kj, 
--     fiber, 
--     protein, 
--     fat, 
--     sugars,
--     carbs,
--     salt,
--     picture_url VARCHAR
-- );