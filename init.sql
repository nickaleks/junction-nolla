CREATE TABLE IF NOT EXISTS receipt(
    id SERIAL NOT NULL,
    receipt_id BIGINT,
    customer_id BIGINT,
    ean BIGINT,
    transaction_date VARCHAR,
    quantity BIGINT,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS product(
    id SERIAL NOT NULL,
    ean BIGINT UNIQUE,
    name VARCHAR,
    brand VARCHAR,
    manufacturer VARCHAR,
    weight double precision,
    n_properties VARCHAR,
    is_alcohol BOOLEAN,
    alcohol_content double precision,
    vitamin_d double precision,
    energy_kcal BIGINT,
    enerjy_kj BIGINT,
    fiber double precision,
    protein double precision,
    fats double precision,
    sugars double precision,
    salt double precision,
    carbs BIGINT,
    picture_url VARCHAR,
    category_id VARCHAR,
    subcategory_id VARCHAR,
    PRIMARY KEY (id)
); 

CREATE TABLE IF NOT EXISTS daily_goal(
    id SERIAL NOT NULL,
    calories BIGINT,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS customer (
    id SERIAL NOT NULL,
    customer_id BIGINT UNIQUE,
    name VARCHAR,
    daily_goal_id BIGINT,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS action (
    id SERIAL NOT NULL,
    customer_id BIGINT,
    action_type VARCHAR,
    action_date VARCHAR,
    purchase_id BIGINT,
    product_id BIGINT,
    amount BIGINT,
    PRIMARY KEY (id)
);

insert into customer  (customer_id, name, daily_goal_id) values (1, 'Lama Alpaka', 1);