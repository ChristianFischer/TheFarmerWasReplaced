#reset_world_pos()

primary = select_primary_plant()
max_sunflower_petal = 0

while True:
	move(East)
	if get_pos_x() == 0:
		move(South)
		
	if get_pos_x() == 0 and get_pos_y() == 0:
		do_shopping()
		primary = select_primary_plant()
		
	if can_harvest():
		if get_entity_type() == Entities.Sunflower:
			petals = measure()
			if petals >= max_sunflower_petal:
				max_sunflower_petal = 0
				harvest()
		else:
			harvest()

	p = get_intended_plant(primary)
	if get_entity_type() != p:
		do_plant(p)
		
		if p == Entities.Sunflower:
			petals = measure()
			max_sunflower_petal = max(max_sunflower_petal, petals)
		
	do_watering()
		
	#if get_entity_type() == None:
	#	if get_pos_x() >= 1:
	#		if get_ground_type() == Grounds.Soil:
	#			till()
	#		trade(Items.Carrot_Seed)
	#		plant(Entities.Carrots)
	#	else:
	#		plant(Entities.Grass)
	
