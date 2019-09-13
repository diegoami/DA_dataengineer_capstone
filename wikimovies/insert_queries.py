

insert_occupation =  """
INSERT INTO public.occupations (
	occupation_id,
	occupation_name
) VALUES ({}, {});
"""

insert_occupation_columns = ["occupation", "occupationLabel"]