def do_turn(pw):

    priority = []

    for mplanet in pw.my_planets():
        for pl in pw.not_my_planets():
            distance = pw.distance(source_planet=mplanet, destination_planet=pl)
            score = pl.growth_rate() / distance

            if pl.owner() == 0:
                score = score * 1.3

            if mplanet.num_ships() < pl.num_ships():
                score = 0

            priority.append([score, mplanet, pl, distance])

    priority.sort(key=lambda y: y[0], reverse=True)

    for target in priority:

        required_fleet_size = target[2].num_ships() + (target[3] // 1.05) * target[2].growth_rate()

        if target[1].num_ships() > required_fleet_size * 1.5:
            pw.issue_order(source_planet=target[1], destination_planet=target[2], num_ships=required_fleet_size)
            return
