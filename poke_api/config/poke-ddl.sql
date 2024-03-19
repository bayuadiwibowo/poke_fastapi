CREATE TABLE public.pokemon_effect (
	id serial NOT NULL,
	loan_id text NULL,
	user_id text NULL,
	pokemon_ability_id varchar NULL,
	effect text NULL,
	"language" jsonb NULL,
	short_effect text NULL
);