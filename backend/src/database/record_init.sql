--POSTGIS INIT
CREATE EXTENSION postgis;
DROP TABLE IF EXISTS spatial_ref_sys; --drops unused tabe created by postgis which gives exception when using alembic
--SCHEMAS
CREATE SCHEMA IF NOT EXISTS public;
CREATE SCHEMA IF NOT EXISTS brownfields;
CREATE SCHEMA IF NOT EXISTS auth;
--TABLE INIT VALUES
--BROWNFIELD LOOKUPS
INSERT INTO brownfields.colors(name, hex_value)
values ('hnedá', '#964B00'),
    ('červená', '#eb4034');
INSERT INTO brownfields.ownership_types(value)
values ('Štátne'),
    ('Obecné'),
    ('Spoločné (družstvá, urbáre)'),
    ('Súkromné'),
    ('Iné');
INSERT INTO brownfields.original_functional_utilizations(value)
VALUES ('Územia priemyselnej výroby'),
    ('Územia bývania a občianskej vybavenosti'),
    (
        'Územia poľnohospodárskej a lesohospodárskej výroby'
    ),
    ('Územia ťažobných areálov'),
    ('Územia športu, rekreácie a cestovného ruchu'),
    ('Územia skládok odpadu'),
    ('Územia vojenských objektov a zariadení'),
    ('Územia dopravnej a technickej infraštruktúry'),
    ('Iné územia');
INSERT INTO brownfields.utilizations(value)
VALUES ('Úplne opustené a nevyužívané'),
    ('Málo využívané (do 30%)'),
    ('Čiastočne využívané (do 50%)'),
    (
        'Zatiaľ využívané, pripravuje sa ukončenie doterajšieho využívania'
    );
INSERT INTO brownfields.area_sizes(value)
values ('Malé (0,1 - 0,5 ha)'),
    ('Stredné (0,5 - 5 ha)'),
    ('Veľké (5 - 10 ha)'),
    ('Veľmi veľké (nad 10 ha)');
INSERT INTO brownfields.locations(value)
values ('V zastavanom území v centrálnej časti'),
    ('V zastavanom území v širšom centre'),
    ('Na okraji zastavaného územia '),
    ('V prírodnej krajine');
INSERT INTO brownfields.degradation_levels(value)
values (
        'Potenciálne rizikové lokality s predpokladom degradácie '
    ),
    (
        'Slabo degradované - Zariadenia a objekty opustené, ale zachovalé'
    ),
    (
        'Stredne degradované - Zariadenia a objekty čiastočne schátralé'
    ),
    (
        'Silne degradované - Zariadenia a objekty zdevastované'
    ),
    ('Silne degradované bez objektov');
INSERT INTO brownfields.residentional_area_categories(value)
values ('Malé obce'),
    ('Stredné a veľké obce'),
    ('Mestá a mestské aglomerácie');
INSERT INTO brownfields.settlements(value)
values ('Nezistené'),
    ('Vysporiadané s malým počtom vlastníkov'),
    ('Vysporiadané s veľkým počtom vlastníkov'),
    ('Nevysporiadané s neznámymi vlastníkmi');
INSERT INTO brownfields.infrastructure_availabilities(value)
values (
        'Dobrá dopravná dostupnosť (diaľnice, rýchlostné cesty) - verejná doprava, električková trať'
    ),
    ('Stredne dobrá dostupnosť'),
    ('Obťažná dostupnosť');
INSERT INTO brownfields.natural_and_architectural_values(value)
values (
        'Výskyt historických, architektonických a iných pamiatok a hodnôt'
    ),
    (
        'Bez historických, architektonických a iných pamiatok a hodnôt'
    );
INSERT INTO brownfields.revitalizations(value)
values (
        'možné návratenie do pôvodného stavu a obnovenie pôvodnej činnosti'
    ),
    ('čiastočné navrátenie do pôvodného stavu'),
    ('zmena typu využívania'),
    ('odstránenie objektov a realizácia zelene');
-- INSERT INTO brownfields.economic_potentials(value)
-- values ();
-- INSERT INTO brownfields.environmental_burden_inclusions(value)
-- values ();
--AUTH LOOKUPS
INSERT INTO auth.roles(name)
values ('admin'),
    ('clerk');
INSERT INTO auth.permissions(name)
values ('brownfields:create'),
    ('brownfields:read'),
    ('brownfields:update'),
    ('brownfields:delete'),
    ('users:read'),
    ('users:create'),
    ('users:update'),
    ('users:delete');
--Insert admin permissions
INSERT INTO auth.role_permissions(role_id, permission_id) (
        select roles.id as role_id,
            permissions.id as permission_id
        from auth.roles as roles
            cross join auth.permissions as permissions
        where roles.name = 'admin'
    ); --Insert clerk permissions
INSERT INTO auth.role_permissions(role_id, permission_id) (
        select roles.id as role_id,
            permissions.id as permission_id
        from auth.roles as roles
            cross join auth.permissions as permissions
        where roles.name = 'clerk'
            and permissions.name in (
                'brownfields:create',
                'brownfields:read', 
                'brownfields:update',
                'brownfields:delete'
            )
    );