

insert_occupation =  """
INSERT INTO public.occupations (
	occupation_id,
	occupation_name
) VALUES (%s, %s);
"""

insert_occupation_columns = ["occupation", "occupationLabel"]